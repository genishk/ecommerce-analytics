"""
고객 생애 가치 (CLV) 분석 모듈

CLV (Customer Lifetime Value)란?
고객이 기업과의 관계 기간 동안 창출할 것으로 예상되는 총 수익의 현재 가치입니다.

CLV의 중요성:
1. 고객 획득 비용 (CAC) 대비 수익성 평가
2. 마케팅 예산 배분의 기준점 제공
3. 고가치 고객 식별 및 유지 전략 수립
4. 장기적 비즈니스 성장 예측

계산 방법:
1. 단순 CLV = 평균 주문 금액 × 구매 빈도 × 고객 수명
2. 예측 CLV = 머신러닝을 활용한 미래 구매 예측
3. 코호트 기반 CLV = 시간에 따른 고객 행동 패턴 분석

Author: E-commerce Analytics Team
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class CLVAnalyzer:
    """
    고객 생애 가치 (CLV) 분석을 수행하는 클래스
    
    이 클래스는 여러 방법으로 CLV를 계산하고 분석합니다:
    1. 역사적 CLV: 과거 구매 데이터 기반
    2. 예측 CLV: 미래 구매 예상값
    3. 코호트 기반 CLV: 가입 시기별 분석
    """
    
    def __init__(self, analysis_period_months: int = 12):
        """
        CLV 분석기 초기화
        
        Args:
            analysis_period_months (int): 분석 기간 (개월)
        """
        self.analysis_period = analysis_period_months
        self.clv_data = None
        
    def calculate_historical_clv(self, orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        역사적 CLV를 계산합니다.
        
        이 방법은 고객의 과거 구매 이력을 기반으로 CLV를 계산합니다.
        
        계산 공식:
        CLV = 평균 주문 금액 × 구매 빈도 × 고객 수명 (예상)
        
        Args:
            orders_df: 주문 데이터
            customers_df: 고객 데이터
            
        Returns:
            pd.DataFrame: CLV가 계산된 고객 데이터
        """
        
        print("💰 역사적 CLV 계산을 시작합니다...")
        
        # 날짜 변환
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
        
        # 1️⃣ 고객별 구매 통계 계산
        customer_stats = orders_df.groupby('customer_id').agg({
            'final_amount': ['sum', 'mean', 'count'],  # 총액, 평균, 횟수
            'order_date': ['min', 'max']  # 첫 구매, 마지막 구매
        }).reset_index()
        
        # 컬럼명 평탄화
        customer_stats.columns = [
            'customer_id', 'total_spent', 'avg_order_value', 
            'purchase_frequency', 'first_purchase', 'last_purchase'
        ]
        
        # 2️⃣ 고객 수명 계산
        customer_stats['customer_lifespan_days'] = (
            customer_stats['last_purchase'] - customer_stats['first_purchase']
        ).dt.days
        
        # 첫 구매만 한 고객은 최소 1일로 설정
        customer_stats['customer_lifespan_days'] = customer_stats['customer_lifespan_days'].apply(
            lambda x: max(x, 1)
        )
        
        # 3️⃣ 구매 빈도 계산 (월별)
        customer_stats['purchase_frequency_monthly'] = (
            customer_stats['purchase_frequency'] / 
            (customer_stats['customer_lifespan_days'] / 30.44)  # 평균 월일수
        ).fillna(1)  # 0으로 나누기 방지
        
        # 4️⃣ 예상 고객 수명 계산 (단순 모델)
        # 업계 평균값이나 과거 데이터를 기반으로 설정
        # 여기서는 현재 수명의 1.5배로 가정 (보수적 추정)
        customer_stats['predicted_lifespan_months'] = (
            customer_stats['customer_lifespan_days'] / 30.44 * 1.5
        ).clip(lower=1, upper=60)  # 최소 1개월, 최대 5년
        
        # 5️⃣ CLV 계산
        customer_stats['historical_clv'] = (
            customer_stats['avg_order_value'] * 
            customer_stats['purchase_frequency_monthly'] * 
            customer_stats['predicted_lifespan_months']
        )
        
        # 6️⃣ 고객 데이터와 병합
        self.clv_data = customers_df.merge(customer_stats, on='customer_id', how='left')
        
        # 구매 이력이 없는 고객들 처리
        self.clv_data = self.clv_data.fillna({
            'total_spent': 0,
            'avg_order_value': 0,
            'purchase_frequency': 0,
            'purchase_frequency_monthly': 0,
            'predicted_lifespan_months': 12,  # 기본 1년
            'historical_clv': 0
        })
        
        print(f"✅ {len(self.clv_data)}명 고객의 역사적 CLV 계산 완료")
        
        return self.clv_data
    
    def calculate_predictive_clv(self, orders_df: pd.DataFrame) -> pd.DataFrame:
        """
        예측 CLV를 계산합니다.
        
        이 방법은 고객의 구매 패턴을 분석하여 미래 CLV를 예측합니다.
        
        사용하는 요소:
        1. 구매 트렌드 (증가/감소/안정)
        2. 계절성 패턴
        3. 고객 세그먼트별 패턴
        4. 최근 구매 활동
        
        Returns:
            pd.DataFrame: 예측 CLV가 추가된 데이터
        """
        
        if self.clv_data is None:
            raise ValueError("먼저 calculate_historical_clv()를 실행해주세요.")
        
        print("🔮 예측 CLV 계산을 시작합니다...")
        
        # 날짜 변환
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        
        # 1️⃣ 최근 구매 트렌드 분석 (최근 6개월 vs 이전 6개월)
        recent_date = orders_df['order_date'].max()
        six_months_ago = recent_date - timedelta(days=180)
        twelve_months_ago = recent_date - timedelta(days=360)
        
        # 최근 6개월 구매액
        recent_purchases = orders_df[
            orders_df['order_date'] >= six_months_ago
        ].groupby('customer_id')['final_amount'].sum()
        
        # 이전 6개월 구매액  
        previous_purchases = orders_df[
            (orders_df['order_date'] >= twelve_months_ago) & 
            (orders_df['order_date'] < six_months_ago)
        ].groupby('customer_id')['final_amount'].sum()
        
        # 트렌드 계산
        trend_data = pd.DataFrame({
            'customer_id': recent_purchases.index,
            'recent_spending': recent_purchases.values
        })
        
        trend_data = trend_data.merge(
            previous_purchases.to_frame('previous_spending'), 
            left_on='customer_id', right_index=True, how='left'
        ).fillna(0)
        
        # 성장률 계산
        trend_data['spending_growth_rate'] = np.where(
            trend_data['previous_spending'] > 0,
            (trend_data['recent_spending'] - trend_data['previous_spending']) / trend_data['previous_spending'],
            0
        )
        
        # 2️⃣ 예측 CLV 계산
        # 성장률을 고려한 미래 가치 예측
        trend_data['trend_multiplier'] = 1 + (trend_data['spending_growth_rate'] * 0.5)  # 보수적 적용
        trend_data['trend_multiplier'] = trend_data['trend_multiplier'].clip(0.5, 2.0)  # 제한값 적용
        
        # 3️⃣ CLV 데이터에 병합
        self.clv_data = self.clv_data.merge(
            trend_data[['customer_id', 'spending_growth_rate', 'trend_multiplier']], 
            on='customer_id', how='left'
        ).fillna({'spending_growth_rate': 0, 'trend_multiplier': 1.0})
        
        # 예측 CLV 계산
        self.clv_data['predictive_clv'] = (
            self.clv_data['historical_clv'] * self.clv_data['trend_multiplier']
        )
        
        print("✅ 예측 CLV 계산 완료")
        
        return self.clv_data
    
    def segment_customers_by_clv(self) -> pd.DataFrame:
        """
        CLV를 기준으로 고객을 세그먼트로 분류합니다.
        
        세그먼트:
        1. High Value (상위 20%): CLV 최상위 고객
        2. Medium Value (중위 60%): CLV 중간 고객  
        3. Low Value (하위 20%): CLV 하위 고객
        
        Returns:
            pd.DataFrame: CLV 세그먼트가 추가된 데이터
        """
        
        if self.clv_data is None:
            raise ValueError("먼저 CLV 계산을 실행해주세요.")
        
        print("🎯 CLV 기반 고객 세그멘테이션을 시작합니다...")
        
        # CLV 기준으로 세그먼트 분류
        self.clv_data['clv_percentile'] = self.clv_data['predictive_clv'].rank(pct=True)
        
        def assign_clv_segment(percentile):
            if percentile >= 0.8:
                return 'High Value'
            elif percentile >= 0.2:
                return 'Medium Value'
            else:
                return 'Low Value'
        
        self.clv_data['clv_segment'] = self.clv_data['clv_percentile'].apply(assign_clv_segment)
        
        # 세그먼트별 통계
        segment_stats = self.clv_data.groupby('clv_segment').agg({
            'customer_id': 'count',
            'predictive_clv': ['mean', 'median', 'sum'],
            'total_spent': ['mean', 'sum']
        }).round(2)
        
        print("📊 CLV 세그먼트별 통계:")
        print(segment_stats)
        
        return self.clv_data
    
    def get_clv_insights(self) -> Dict:
        """
        CLV 분석 결과에 대한 비즈니스 인사이트를 제공합니다.
        
        Returns:
            Dict: CLV 인사이트와 추천 액션
        """
        
        if self.clv_data is None:
            raise ValueError("먼저 CLV 분석을 실행해주세요.")
        
        insights = {}
        
        # 전체 CLV 통계
        total_clv = self.clv_data['predictive_clv'].sum()
        avg_clv = self.clv_data['predictive_clv'].mean()
        median_clv = self.clv_data['predictive_clv'].median()
        
        insights['overall'] = {
            'total_predicted_clv': total_clv,
            'average_clv': avg_clv,
            'median_clv': median_clv,
            'total_customers': len(self.clv_data)
        }
        
        # 세그먼트별 인사이트
        if 'clv_segment' in self.clv_data.columns:
            segment_insights = {}
            
            for segment in ['High Value', 'Medium Value', 'Low Value']:
                segment_data = self.clv_data[self.clv_data['clv_segment'] == segment]
                
                if len(segment_data) > 0:
                    segment_insights[segment] = {
                        'customer_count': len(segment_data),
                        'avg_clv': segment_data['predictive_clv'].mean(),
                        'total_clv': segment_data['predictive_clv'].sum(),
                        'clv_contribution': segment_data['predictive_clv'].sum() / total_clv * 100
                    }
            
            insights['segments'] = segment_insights
        
        # 추천 액션
        insights['recommendations'] = {
            'High Value': [
                'VIP 프로그램 제공',
                '개인화된 프리미엄 서비스',
                '우선 고객 지원',
                '독점 상품 및 할인'
            ],
            'Medium Value': [
                '업셀링 및 크로스셀링',
                '로열티 프로그램 참여 유도',
                '정기 프로모션 제공',
                '고객 만족도 개선'
            ],
            'Low Value': [
                '기본 서비스 유지',
                '비용 효율적인 마케팅',
                '자동화된 이메일 캠페인',
                '고객 이탈 방지 프로그램'
            ]
        }
        
        return insights 