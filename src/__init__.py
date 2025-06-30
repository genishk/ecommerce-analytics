"""
E-commerce Analytics Platform - Main Package
===========================================

이 패키지는 전자상거래 데이터 분석 및 머신러닝을 위한 
종합적인 도구들을 제공합니다.

주요 모듈:
    - data_generation: 실제 같은 가상 데이터 생성
    - analytics: 고객, 매출, 상품 분석  
    - ml_models: 머신러닝 모델링
    - recommendation: 추천 시스템
    - dashboard: 웹 대시보드
    - api: REST API 서비스
    - utils: 공통 유틸리티

사용 예시:
    >>> from src.data_generation import DataGenerator
    >>> from src.analytics import CustomerAnalytics
    >>> from src.utils import load_config
    
    >>> config = load_config()
    >>> generator = DataGenerator(config)
    >>> data = generator.generate_all()
"""

__version__ = "1.0.0"
__author__ = "genishk"
__email__ = "sk4985@columbia.edu"

# 패키지 레벨 imports
try:
    from . import utils
    from .utils.config_loader import load_config
    from .utils.logger import get_logger
    
    # 기본 설정 로드
    try:
        config = load_config()
        logger = get_logger(__name__)
        logger.info(f"E-commerce Analytics Platform v{__version__} 초기화 완료")
    except Exception as e:
        # 설정 파일이 없어도 패키지는 import 되어야 함
        config = None
        logger = None
        print(f"Warning: 설정 로드 실패 - {e}")
        
except ImportError as e:
    # 의존성이 없어도 패키지는 import 되어야 함
    print(f"Warning: 일부 모듈 import 실패 - {e}")
    config = None
    logger = None

# 패키지 메타데이터
__all__ = [
    'config',
    'logger',
    'load_config',
    'get_logger',
] 