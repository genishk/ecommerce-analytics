"""
고객 세그멘테이션 모듈

고객 세그멘테이션이란?
비슷한 특성이나 행동을 보이는 고객들을 그룹으로 나누는 분석 기법입니다.

세그멘테이션 방법:
1. 인구통계학적: 나이, 성별, 지역 등
2. 행동적: 구매 패턴, 사용 빈도 등  
3. 심리적: 라이프스타일, 가치관 등
4. 지리적: 거주 지역, 기후 등

머신러닝 기법:
- K-means 클러스터링: 거리 기반 그룹화
- 계층적 클러스터링: 트리 구조 그룹화
- DBSCAN: 밀도 기반 그룹화

비즈니스 가치:
- 맞춤형 마케팅 전략 수립
- 제품 개발 방향 결정
- 고객 서비스 개선
- 수익성 최적화

Author: E-commerce Analytics Team
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class CustomerSegmentation:
    """
    고객 세그멘테이션을 수행하는 클래스
    
    다양한 기준으로 고객을 세그먼트로 분류합니다:
    1. RFM 기반 세그멘테이션
    2. 구매 행동 기반 세그멘테이션
    3. 인구통계학적 세그멘테이션
    4. 머신러닝 기반 자동 세그멘테이션
    """
    
    def __init__(self, random_state: int = 42):
        """고객 세그멘테이션 분석기 초기화"""
        self.random_state = random_state
        self.segmented_data = None
        self.scaler = StandardScaler()
        
    def behavioral_segmentation(self, rfm_data: pd.DataFrame) -> pd.DataFrame:
        """
        구매 행동 기반 세그멘테이션을 수행합니다.
        
        사용 변수:
        - 구매 빈도 (Frequency)
        - 구매 금액 (Monetary)
        - 최근성 (Recency)
        - 평균 주문 가격
        
        Args:
            rfm_data: RFM 분석이 완료된 데이터
            
        Returns:
            pd.DataFrame: 행동 세그먼트가 추가된 데이터
        """
        
        print("🎯 구매 행동 기반 세그멘테이션을 시작합니다...")
        
        # 1️⃣ 세그멘테이션에 사용할 변수 선택
        features = ['frequency', 'monetary', 'recency']
        
        # 결측값 처리
        segmentation_data = rfm_data[features].fillna(0)
        
        # 2️⃣ 데이터 표준화
        scaled_features = self.scaler.fit_transform(segmentation_data)
        scaled_df = pd.DataFrame(scaled_features, columns=features)
        
        # 3️⃣ 최적 클러스터 수 찾기 (엘보우 방법)
        inertias = []
        silhouette_scores = []
        k_range = range(2, 8)
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=self.random_state, n_init=10)
            kmeans.fit(scaled_df)
            inertias.append(kmeans.inertia_)
            
            if k > 1:  # 실루엣 점수는 k>=2일 때만 계산 가능
                sil_score = silhouette_score(scaled_df, kmeans.labels_)
                silhouette_scores.append(sil_score)
        
        # 최적 클러스터 수 선택 (실루엣 점수가 가장 높은 k)
        optimal_k = k_range[np.argmax(silhouette_scores)]
        
        print(f"   최적 클러스터 수: {optimal_k} (실루엣 점수: {max(silhouette_scores):.3f})")
        
        # 4️⃣ 최종 클러스터링 수행
        final_kmeans = KMeans(n_clusters=optimal_k, random_state=self.random_state, n_init=10)
        cluster_labels = final_kmeans.fit_predict(scaled_df)
        
        # 5️⃣ 결과를 원본 데이터에 추가
        self.segmented_data = rfm_data.copy()
        self.segmented_data['behavioral_segment'] = cluster_labels
        
        # 6️⃣ 세그먼트별 특성 분석
        segment_profiles = self.segmented_data.groupby('behavioral_segment')[features].agg(['mean', 'count']).round(2)
        
        print("📊 세그먼트별 프로필:")
        print(segment_profiles)
        
        # 7️⃣ 세그먼트에 의미있는 이름 부여
        segment_names = self._assign_behavioral_segment_names(segment_profiles, features)
        
        # 세그먼트 이름 매핑
        self.segmented_data['behavioral_segment_name'] = self.segmented_data['behavioral_segment'].map(segment_names)
        
        print(f"✅ {optimal_k}개 행동 세그먼트 생성 완료")
        
        return self.segmented_data
    
    def _assign_behavioral_segment_names(self, profiles: pd.DataFrame, features: List[str]) -> Dict:
        """세그먼트에 의미있는 이름을 부여합니다."""
        
        segment_names = {}
        
        for segment_id in profiles.index:
            # 각 세그먼트의 평균값 추출
            freq_mean = profiles.loc[segment_id, ('frequency', 'mean')]
            monetary_mean = profiles.loc[segment_id, ('monetary', 'mean')]
            recency_mean = profiles.loc[segment_id, ('recency', 'mean')]
            
            # 전체 평균과 비교하여 이름 결정
            freq_overall = profiles[('frequency', 'mean')].mean()
            monetary_overall = profiles[('monetary', 'mean')].mean()
            recency_overall = profiles[('recency', 'mean')].mean()
            
            if freq_mean > freq_overall and monetary_mean > monetary_overall:
                if recency_mean < recency_overall:
                    segment_names[segment_id] = "VIP 고객"
                else:
                    segment_names[segment_id] = "과거 VIP"
            elif freq_mean > freq_overall:
                if recency_mean < recency_overall:
                    segment_names[segment_id] = "충성 고객"
                else:
                    segment_names[segment_id] = "이탈 위험"
            elif monetary_mean > monetary_overall:
                if recency_mean < recency_overall:
                    segment_names[segment_id] = "고액 고객"
                else:
                    segment_names[segment_id] = "휴면 고액"
            else:
                if recency_mean < recency_overall:
                    segment_names[segment_id] = "신규/일반"
                else:
                    segment_names[segment_id] = "저관여"
        
        return segment_names
    
    def demographic_segmentation(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """
        인구통계학적 세그멘테이션을 수행합니다.
        
        사용 변수:
        - 나이 (연령대)
        - 성별
        - 지역
        
        Args:
            customers_df: 고객 데이터
            
        Returns:
            pd.DataFrame: 인구통계 세그먼트가 추가된 데이터
        """
        
        print("👥 인구통계학적 세그멘테이션을 시작합니다...")
        
        if self.segmented_data is None:
            self.segmented_data = customers_df.copy()
        else:
            # 기존 데이터와 병합
            demo_cols = ['age', 'gender', 'region']
            for col in demo_cols:
                if col in customers_df.columns and col not in self.segmented_data.columns:
                    self.segmented_data = self.segmented_data.merge(
                        customers_df[['customer_id', col]], 
                        on='customer_id', 
                        how='left'
                    )
        
        # 1️⃣ 연령대 세그먼트 생성
        def assign_age_group(age):
            if age < 25:
                return "Z세대 (18-24)"
            elif age < 35:
                return "밀레니얼 (25-34)"
            elif age < 45:
                return "X세대 (35-44)"
            elif age < 55:
                return "베이비부머 초기 (45-54)"
            else:
                return "베이비부머 후기 (55+)"
        
        self.segmented_data['age_group'] = self.segmented_data['age'].apply(assign_age_group)
        
        # 2️⃣ 성별-연령대 조합 세그먼트
        self.segmented_data['gender_age_segment'] = (
            self.segmented_data['gender'] + "_" + self.segmented_data['age_group']
        )
        
        # 3️⃣ 지역-성별 조합 세그먼트
        self.segmented_data['region_gender_segment'] = (
            self.segmented_data['region'] + "_" + self.segmented_data['gender']
        )
        
        # 4️⃣ 종합 인구통계 세그먼트
        self.segmented_data['demographic_segment'] = (
            self.segmented_data['region'] + "_" + 
            self.segmented_data['gender'] + "_" + 
            self.segmented_data['age_group']
        )
        
        print("✅ 인구통계학적 세그멘테이션 완료")
        
        return self.segmented_data
    
    def get_segmentation_insights(self) -> Dict:
        """
        세그멘테이션 결과에 대한 비즈니스 인사이트를 제공합니다.
        
        Returns:
            Dict: 세그멘테이션 인사이트와 추천 액션
        """
        
        if self.segmented_data is None:
            raise ValueError("먼저 세그멘테이션을 실행해주세요.")
        
        insights = {}
        
        # 1️⃣ 행동 세그먼트 인사이트
        if 'behavioral_segment_name' in self.segmented_data.columns:
            behavioral_insights = {}
            
            for segment in self.segmented_data['behavioral_segment_name'].unique():
                segment_data = self.segmented_data[
                    self.segmented_data['behavioral_segment_name'] == segment
                ]
                
                behavioral_insights[segment] = {
                    'customer_count': len(segment_data),
                    'avg_frequency': segment_data['frequency'].mean(),
                    'avg_monetary': segment_data['monetary'].mean(),
                    'avg_recency': segment_data['recency'].mean()
                }
            
            insights['behavioral'] = behavioral_insights
        
        # 2️⃣ 인구통계 세그먼트 인사이트
        if 'age_group' in self.segmented_data.columns:
            demo_insights = {}
            
            # 연령대별 분포
            age_dist = self.segmented_data['age_group'].value_counts()
            demo_insights['age_distribution'] = age_dist.to_dict()
            
            # 성별 분포
            gender_dist = self.segmented_data['gender'].value_counts()
            demo_insights['gender_distribution'] = gender_dist.to_dict()
            
            # 지역별 분포
            region_dist = self.segmented_data['region'].value_counts()
            demo_insights['region_distribution'] = region_dist.to_dict()
            
            insights['demographic'] = demo_insights
        
        # 3️⃣ 추천 마케팅 전략
        marketing_strategies = {
            "VIP 고객": [
                "프리미엄 서비스 제공",
                "독점 상품 우선 판매",
                "개인 맞춤 서비스",
                "높은 마케팅 예산 투입"
            ],
            "충성 고객": [
                "로열티 프로그램 강화",
                "정기 프로모션 제공",
                "브랜드 앰버서더 프로그램",
                "추천 인센티브 제공"
            ],
            "신규/일반": [
                "온보딩 프로그램",
                "첫 구매 할인",
                "교육 컨텐츠 제공",
                "점진적 관계 구축"
            ]
        }
        
        insights['marketing_strategies'] = marketing_strategies
        
        return insights 