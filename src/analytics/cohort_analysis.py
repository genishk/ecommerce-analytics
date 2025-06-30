"""
코호트 분석 모듈

코호트 분석이란?
동일한 시점에 특정 행동을 한 고객 그룹(코호트)의 시간에 따른 행동 변화를 추적하는 분석 방법입니다.

주요 활용:
1. 고객 유지율 (Retention Rate) 분석
2. 고객 이탈 패턴 파악
3. 제품/서비스 개선 효과 측정
4. 마케팅 캠페인 효과 분석

코호트 유형:
1. 가입 코호트: 가입 시점 기준
2. 첫 구매 코호트: 첫 구매 시점 기준
3. 행동 코호트: 특정 행동 기준

비즈니스 가치:
- 고객 생애주기 이해
- 이탈 시점 예측
- 제품 개선 우선순위 결정
- 고객 유지 전략 수립

Author: E-commerce Analytics Team
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class CohortAnalyzer:
    """
    코호트 분석을 수행하는 클래스
    
    이 클래스는 다양한 코호트 분석을 제공합니다:
    1. 가입 기반 코호트 분석
    2. 첫 구매 기반 코호트 분석
    3. 매출 기반 코호트 분석
    4. 고객 유지율 분석
    """
    
    def __init__(self, period_type: str = 'monthly'):
        """
        코호트 분석기 초기화
        
        Args:
            period_type (str): 분석 주기 ('monthly', 'weekly', 'daily')
        """
        self.period_type = period_type
        self.cohort_data = None
        self.retention_table = None
        
    def create_signup_cohorts(self, customers_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
        """
        가입 시점 기반 코호트를 생성합니다.
        
        이 분석은 같은 시기에 가입한 고객들의 구매 행동을 추적합니다.
        
        Args:
            customers_df: 고객 데이터 (customer_id, signup_date 포함)
            orders_df: 주문 데이터 (customer_id, order_date 포함)
            
        Returns:
            pd.DataFrame: 코호트 분석 결과
        """
        
        print(f"📅 가입 기반 {self.period_type} 코호트 분석을 시작합니다...")
        
        # 날짜 컬럼 변환
        customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        
        # 1️⃣ 가입 코호트 (년-월) 생성
        if self.period_type == 'monthly':
            customers_df['cohort_group'] = customers_df['signup_date'].dt.to_period('M')
            orders_df['order_period'] = orders_df['order_date'].dt.to_period('M')
        elif self.period_type == 'weekly':
            customers_df['cohort_group'] = customers_df['signup_date'].dt.to_period('W')
            orders_df['order_period'] = orders_df['order_date'].dt.to_period('W')
        else:  # daily
            customers_df['cohort_group'] = customers_df['signup_date'].dt.to_period('D')
            orders_df['order_period'] = orders_df['order_date'].dt.to_period('D')
        
        # 2️⃣ 고객-주문 데이터 병합
        cohort_data = orders_df.merge(
            customers_df[['customer_id', 'cohort_group']], 
            on='customer_id', 
            how='left'
        )
        
        # 3️⃣ 코호트별 기간 계산
        def get_period_number(row):
            """가입 코호트로부터 몇 번째 기간인지 계산"""
            if pd.isna(row['cohort_group']) or pd.isna(row['order_period']):
                return np.nan
            return (row['order_period'] - row['cohort_group']).n
        
        cohort_data['period_number'] = cohort_data.apply(get_period_number, axis=1)
        
        # 4️⃣ 코호트별 고객 수 계산
        cohort_sizes = customers_df.groupby('cohort_group')['customer_id'].nunique().reset_index()
        cohort_sizes.columns = ['cohort_group', 'total_customers']
        
        # 5️⃣ 각 기간별 활성 고객 수 계산
        cohort_table = cohort_data.groupby(['cohort_group', 'period_number'])['customer_id'].nunique().reset_index()
        cohort_table.columns = ['cohort_group', 'period_number', 'active_customers']
        
        # 6️⃣ 코호트 크기와 병합
        cohort_table = cohort_table.merge(cohort_sizes, on='cohort_group')
        
        # 7️⃣ 유지율 계산
        cohort_table['retention_rate'] = cohort_table['active_customers'] / cohort_table['total_customers']
        
        self.cohort_data = cohort_table
        
        print(f"✅ {len(cohort_sizes)} 개 코호트 분석 완료")
        
        return cohort_table
    
    def create_retention_table(self) -> pd.DataFrame:
        """
        유지율 테이블을 생성합니다.
        
        이 테이블은 각 코호트의 시간대별 유지율을 매트릭스 형태로 표시합니다.
        
        Returns:
            pd.DataFrame: 유지율 매트릭스
        """
        
        if self.cohort_data is None:
            raise ValueError("먼저 create_signup_cohorts()를 실행해주세요.")
        
        print("📊 유지율 테이블을 생성합니다...")
        
        # 피벗 테이블로 유지율 매트릭스 생성
        retention_table = self.cohort_data.pivot_table(
            index='cohort_group',
            columns='period_number', 
            values='retention_rate',
            fill_value=0
        )
        
        self.retention_table = retention_table
        
        print(f"✅ {retention_table.shape[0]} x {retention_table.shape[1]} 유지율 테이블 생성 완료")
        
        return retention_table
    
    def analyze_revenue_cohorts(self, customers_df: pd.DataFrame, orders_df: pd.DataFrame) -> pd.DataFrame:
        """
        매출 기반 코호트 분석을 수행합니다.
        
        이 분석은 각 코호트의 시간대별 매출 기여도를 분석합니다.
        
        Args:
            customers_df: 고객 데이터
            orders_df: 주문 데이터 (final_amount 포함)
            
        Returns:
            pd.DataFrame: 매출 코호트 분석 결과
        """
        
        print("💰 매출 기반 코호트 분석을 시작합니다...")
        
        # 날짜 컬럼 변환
        customers_df['signup_date'] = pd.to_datetime(customers_df['signup_date'])
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        
        # 코호트 그룹 생성
        if self.period_type == 'monthly':
            customers_df['cohort_group'] = customers_df['signup_date'].dt.to_period('M')
            orders_df['order_period'] = orders_df['order_date'].dt.to_period('M')
        
        # 고객-주문 데이터 병합
        revenue_cohort_data = orders_df.merge(
            customers_df[['customer_id', 'cohort_group']], 
            on='customer_id', 
            how='left'
        )
        
        # 기간 번호 계산
        def get_period_number(row):
            if pd.isna(row['cohort_group']) or pd.isna(row['order_period']):
                return np.nan
            return (row['order_period'] - row['cohort_group']).n
        
        revenue_cohort_data['period_number'] = revenue_cohort_data.apply(get_period_number, axis=1)
        
        # 코호트별 매출 집계
        revenue_table = revenue_cohort_data.groupby(['cohort_group', 'period_number']).agg({
            'final_amount': ['sum', 'mean'],
            'customer_id': 'nunique'
        }).reset_index()
        
        # 컬럼명 정리
        revenue_table.columns = [
            'cohort_group', 'period_number', 
            'total_revenue', 'avg_revenue_per_order', 'active_customers'
        ]
        
        # 고객당 평균 매출 계산
        revenue_table['avg_revenue_per_customer'] = (
            revenue_table['total_revenue'] / revenue_table['active_customers']
        )
        
        print("✅ 매출 코호트 분석 완료")
        
        return revenue_table
    
    def get_cohort_insights(self) -> Dict:
        """
        코호트 분석 결과에 대한 비즈니스 인사이트를 제공합니다.
        
        Returns:
            Dict: 코호트 분석 인사이트와 추천 액션
        """
        
        if self.retention_table is None:
            raise ValueError("먼저 create_retention_table()을 실행해주세요.")
        
        insights = {}
        
        # 1️⃣ 전체 유지율 트렌드
        # 첫 번째 기간(0) 유지율은 항상 100%이므로 1번째 기간부터 분석
        if self.retention_table.shape[1] > 1:
            # 1개월 후 평균 유지율
            month_1_retention = self.retention_table[1].mean()
            
            # 3개월 후 평균 유지율 (데이터가 있는 경우)
            month_3_retention = self.retention_table[3].mean() if 3 in self.retention_table.columns else None
            
            # 6개월 후 평균 유지율 (데이터가 있는 경우)
            month_6_retention = self.retention_table[6].mean() if 6 in self.retention_table.columns else None
            
            insights['retention_trends'] = {
                '1_month_retention': month_1_retention,
                '3_month_retention': month_3_retention,
                '6_month_retention': month_6_retention
            }
        
        # 2️⃣ 코호트별 성과 분석
        # 가장 최근 코호트와 가장 오래된 코호트 비교
        cohort_performance = {}
        
        for cohort in self.retention_table.index:
            cohort_data = self.retention_table.loc[cohort]
            # NaN이 아닌 값들만 선택
            valid_data = cohort_data.dropna()
            
            if len(valid_data) > 1:  # 최소 2개 기간 데이터 필요
                cohort_performance[str(cohort)] = {
                    'initial_retention': valid_data.iloc[1] if len(valid_data) > 1 else None,
                    'avg_retention': valid_data[1:].mean(),  # 0번째 제외하고 평균
                    'retention_decline': (valid_data.iloc[1] - valid_data.iloc[-1]) if len(valid_data) > 1 else None
                }
        
        insights['cohort_performance'] = cohort_performance
        
        # 3️⃣ 비즈니스 인사이트
        business_insights = []
        
        if month_1_retention:
            if month_1_retention >= 0.5:
                business_insights.append("👍 1개월 유지율이 양호합니다 (50% 이상)")
            elif month_1_retention >= 0.3:
                business_insights.append("⚠️ 1개월 유지율이 보통입니다 (30-50%)")
            else:
                business_insights.append("🚨 1개월 유지율이 낮습니다 (30% 미만)")
        
        if month_3_retention and month_1_retention:
            retention_drop = month_1_retention - month_3_retention
            if retention_drop <= 0.2:
                business_insights.append("👍 유지율 감소폭이 안정적입니다")
            else:
                business_insights.append("⚠️ 유지율이 급격히 감소하고 있습니다")
        
        insights['business_insights'] = business_insights
        
        # 4️⃣ 추천 액션
        recommendations = []
        
        if month_1_retention and month_1_retention < 0.4:
            recommendations.extend([
                "신규 고객 온보딩 프로세스 개선",
                "첫 구매 후 후속 서비스 강화",
                "고객 만족도 조사 및 피드백 수집"
            ])
        
        if month_3_retention and month_3_retention < 0.2:
            recommendations.extend([
                "중기 고객 유지 프로그램 개발",
                "개인화된 마케팅 캠페인 강화",
                "로열티 프로그램 도입 검토"
            ])
        
        recommendations.extend([
            "코호트별 맞춤형 마케팅 전략 수립",
            "이탈 위험 고객 조기 발견 시스템 구축",
            "고객 생애주기별 서비스 개선"
        ])
        
        insights['recommendations'] = recommendations
        
        return insights
    
    def calculate_ltv_by_cohort(self, revenue_cohort_data: pd.DataFrame) -> pd.DataFrame:
        """
        코호트별 고객 생애 가치(LTV)를 계산합니다.
        
        Args:
            revenue_cohort_data: 매출 코호트 분석 결과
            
        Returns:
            pd.DataFrame: 코호트별 LTV 데이터
        """
        
        print("💎 코호트별 LTV 계산을 시작합니다...")
        
        # 코호트별 누적 매출 계산
        ltv_data = revenue_cohort_data.groupby('cohort_group').apply(
            lambda x: x.sort_values('period_number').assign(
                cumulative_revenue_per_customer=x.sort_values('period_number')['avg_revenue_per_customer'].cumsum()
            )
        ).reset_index(drop=True)
        
        # 코호트별 최종 LTV (마지막 기간의 누적 매출)
        final_ltv = ltv_data.groupby('cohort_group')['cumulative_revenue_per_customer'].last().reset_index()
        final_ltv.columns = ['cohort_group', 'ltv']
        
        print("✅ 코호트별 LTV 계산 완료")
        
        return ltv_data, final_ltv 