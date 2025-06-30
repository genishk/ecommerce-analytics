"""
RFM 분석 모듈

RFM 분석은 고객 세그멘테이션의 가장 기본적이고 효과적인 방법 중 하나입니다.

RFM이란?
- R (Recency): 최근성 - 마지막 구매로부터 얼마나 시간이 지났는가?
- F (Frequency): 빈도 - 얼마나 자주 구매하는가?
- M (Monetary): 금액 - 얼마나 많은 돈을 쓰는가?

비즈니스 가치:
- 고객을 11개 세그먼트로 분류하여 맞춤형 마케팅 전략 수립
- 고가치 고객 식별 및 이탈 방지
- 마케팅 예산의 효율적 배분

Author: E-commerce Analytics Team
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class RFMAnalyzer:
    """
    RFM 분석을 수행하는 클래스
    
    세그먼트 정의:
    1. Champions: 최고의 고객
    2. Loyal Customers: 충성 고객
    3. Potential Loyalists: 잠재 충성 고객
    4. New Customers: 신규 고객
    5. Promising: 유망 고객
    6. Need Attention: 관심 필요
    7. About to Sleep: 이탈 위험
    8. At Risk: 위험 고객
    9. Cannot Lose Them: 놓치면 안 됨
    10. Hibernating: 휴면 고객
    11. Lost: 이탈 고객
    """
    
    def __init__(self, reference_date: Optional[datetime] = None):
        """RFM 분석기 초기화"""
        self.reference_date = reference_date or datetime.now()
        self.rfm_data = None
        self.segments = None
        
        # RFM 세그먼트 정의
        self.segment_rules = {
            'Champions': {'R': [4, 5], 'F': [4, 5], 'M': [4, 5]},
            'Loyal Customers': {'R': [3, 5], 'F': [3, 5], 'M': [3, 5]},
            'Potential Loyalists': {'R': [3, 5], 'F': [1, 3], 'M': [1, 3]},
            'New Customers': {'R': [4, 5], 'F': [1, 1], 'M': [1, 1]},
            'Promising': {'R': [3, 4], 'F': [1, 1], 'M': [1, 1]},
            'Need Attention': {'R': [2, 3], 'F': [2, 3], 'M': [2, 3]},
            'About to Sleep': {'R': [2, 3], 'F': [1, 2], 'M': [1, 2]},
            'At Risk': {'R': [1, 2], 'F': [2, 5], 'M': [2, 5]},
            'Cannot Lose Them': {'R': [1, 2], 'F': [4, 5], 'M': [4, 5]},
            'Hibernating': {'R': [1, 2], 'F': [1, 2], 'M': [1, 2]},
            'Lost': {'R': [1, 1], 'F': [1, 1], 'M': [1, 1]}
        }
    
    def calculate_rfm_scores(self, orders_df: pd.DataFrame, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        고객별 RFM 점수를 계산합니다.
        
        계산 방법:
        1. Recency: 마지막 구매일로부터 경과 일수
        2. Frequency: 총 구매 횟수  
        3. Monetary: 총 구매 금액
        4. 각 지표를 1-5점으로 스케일링 (5점이 가장 좋음)
        """
        
        print("📊 RFM 점수 계산을 시작합니다...")
        
        # 날짜 컬럼을 datetime으로 변환
        orders_df['order_date'] = pd.to_datetime(orders_df['order_date'])
        
        # 고객별 집계
        customer_rfm = orders_df.groupby('customer_id').agg({
            'order_date': 'max',      # 마지막 구매일
            'order_id': 'count',      # 구매 횟수
            'final_amount': 'sum'     # 총 구매 금액
        }).reset_index()
        
        # 컬럼명 변경
        customer_rfm.columns = ['customer_id', 'last_order_date', 'frequency', 'monetary']
        
        # Recency 계산 (기준일로부터 경과 일수)
        customer_rfm['recency'] = (self.reference_date - customer_rfm['last_order_date']).dt.days
        
        # RFM 점수화 (1-5점, 5점이 가장 좋음)
        customer_rfm['R_score'] = pd.qcut(
            customer_rfm['recency'].rank(method='first', ascending=False), 
            q=5, labels=[5, 4, 3, 2, 1]
        ).astype(int)
        
        customer_rfm['F_score'] = pd.qcut(
            customer_rfm['frequency'].rank(method='first'), 
            q=5, labels=[1, 2, 3, 4, 5]
        ).astype(int)
        
        customer_rfm['M_score'] = pd.qcut(
            customer_rfm['monetary'].rank(method='first'), 
            q=5, labels=[1, 2, 3, 4, 5]
        ).astype(int)
        
        # 복합 점수 계산
        customer_rfm['RFM_score'] = (
            customer_rfm['R_score'].astype(str) + 
            customer_rfm['F_score'].astype(str) + 
            customer_rfm['M_score'].astype(str)
        )
        
        customer_rfm['RFM_avg_score'] = (
            customer_rfm['R_score'] + 
            customer_rfm['F_score'] + 
            customer_rfm['M_score']
        ) / 3
        
        # 고객 데이터와 병합
        self.rfm_data = customers_df.merge(customer_rfm, on='customer_id', how='left')
        
        # 구매 이력이 없는 고객들 처리
        self.rfm_data = self.rfm_data.fillna({
            'recency': 999, 'frequency': 0, 'monetary': 0,
            'R_score': 1, 'F_score': 1, 'M_score': 1,
            'RFM_score': '111', 'RFM_avg_score': 1.0
        })
        
        print(f"🎉 RFM 분석 완료! 총 {len(self.rfm_data)}명의 고객 분석")
        return self.rfm_data
    
    def assign_segments(self) -> pd.DataFrame:
        """RFM 점수를 기반으로 고객 세그먼트를 할당합니다."""
        
        if self.rfm_data is None:
            raise ValueError("먼저 calculate_rfm_scores()를 실행해주세요.")
        
        print("🎯 고객 세그먼트 할당을 시작합니다...")
        
        def assign_segment(row):
            r, f, m = row['R_score'], row['F_score'], row['M_score']
            
            # 우선순위 순서로 세그먼트 확인
            segment_priority = [
                'Champions', 'Loyal Customers', 'Potential Loyalists',
                'New Customers', 'Promising', 'Cannot Lose Them',
                'At Risk', 'Need Attention', 'About to Sleep',
                'Hibernating', 'Lost'
            ]
            
            for segment in segment_priority:
                rules = self.segment_rules[segment]
                if (rules['R'][0] <= r <= rules['R'][1] and 
                    rules['F'][0] <= f <= rules['F'][1] and 
                    rules['M'][0] <= m <= rules['M'][1]):
                    return segment
            
            return 'Others'
        
        # 세그먼트 할당
        self.rfm_data['segment'] = self.rfm_data.apply(assign_segment, axis=1)
        
        # 세그먼트별 통계
        segment_stats = self.rfm_data['segment'].value_counts()
        
        print("📊 세그먼트별 고객 분포:")
        for segment, count in segment_stats.items():
            percentage = count / len(self.rfm_data) * 100
            print(f"   {segment}: {count:,}명 ({percentage:.1f}%)")
        
        self.segments = segment_stats
        return self.rfm_data
    
    def get_segment_insights(self) -> Dict:
        """각 세그먼트별 비즈니스 인사이트와 액션 플랜을 제공합니다."""
        
        segment_insights = {
            'Champions': {
                'description': '최고의 고객들 - 최근에, 자주, 많이 구매',
                'action_plan': ['프리미엄 제품 추천', 'VIP 프로그램 제공', '리퍼럴 프로그램'],
                'marketing_budget': '높음 (ROI 최고)'
            },
            'Loyal Customers': {
                'description': '정기적으로 구매하는 충성 고객',
                'action_plan': ['로열티 포인트 제공', '정기 할인 쿠폰', '신제품 우선 알림'],
                'marketing_budget': '중간-높음'
            },
            'At Risk': {
                'description': '과거 좋은 고객이었지만 이탈 위험',
                'action_plan': ['개인화된 재참여 메시지', '특별 할인', 'Win-back 캠페인'],
                'marketing_budget': '중간'
            },
            'Cannot Lose Them': {
                'description': '절대 놓치면 안 되는 고가치 고객',
                'action_plan': ['즉시 개인 연락', '프리미엄 서비스', 'VIP 관리자 배정'],
                'marketing_budget': '높음 (긴급)'
            }
        }
        
        return segment_insights 