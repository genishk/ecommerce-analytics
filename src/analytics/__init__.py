"""
고급 고객 분석 모듈

이 모듈은 전자상거래 고객 데이터를 기반으로 다양한 고급 분석을 수행합니다.

주요 기능:
- RFM 분석: 고객의 최근성, 빈도, 금액 기반 세그멘테이션
- 고객 생애 가치 (CLV) 분석: 고객의 장기적 가치 평가
- 이탈 예측: 머신러닝을 활용한 고객 이탈 가능성 예측
- 코호트 분석: 시간에 따른 고객 행동 변화 추적

Author: E-commerce Analytics Team
Version: 1.0.0
"""

from .rfm_analysis import RFMAnalyzer
from .customer_segmentation import CustomerSegmentation
from .clv_analysis import CLVAnalyzer
from .cohort_analysis import CohortAnalyzer

__all__ = [
    'RFMAnalyzer',
    'CustomerSegmentation', 
    'CLVAnalyzer',
    'CohortAnalyzer'
]

__version__ = "1.0.0" 