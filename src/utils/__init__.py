"""
E-commerce Analytics Platform - Utilities Package
===============================================

이 패키지는 프로젝트 전반에서 사용되는 공통 유틸리티들을 제공합니다.

주요 모듈:
    - config_loader: YAML 설정 파일 로드
    - logger: 로깅 시스템 설정
    - data_utils: 데이터 처리 유틸리티
    - plot_utils: 시각화 유틸리티

사용 예시:
    >>> from src.utils import load_config, get_logger
    >>> from src.utils.data_utils import validate_dataframe
    >>> from src.utils.plot_utils import save_plot
"""

# 핵심 유틸리티 함수들을 패키지 레벨에서 import
try:
    from .config_loader import load_config
    from .logger import get_logger, setup_logging
    
    __all__ = [
        'load_config',
        'get_logger', 
        'setup_logging',
    ]
    
except ImportError as e:
    print(f"Warning: 유틸리티 모듈 import 실패 - {e}")
    __all__ = [] 