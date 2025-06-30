"""
Logger - 로깅 시스템
=================

이 모듈은 프로젝트 전반에서 사용할 통합 로깅 시스템을 제공합니다.
파일 로깅, 콘솔 로깅, 로그 레벨 관리 등을 포함합니다.

주요 기능:
    - 콘솔 및 파일 로깅
    - 로그 레벨 관리
    - 로그 파일 로테이션
    - 모듈별 로거 생성

사용 예시:
    >>> from src.utils.logger import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("시스템 시작")
    >>> logger.error("에러 발생", extra={'details': 'error details'})
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_size: int = 10,  # MB
    backup_count: int = 5,
    console_output: bool = True,
    format_string: Optional[str] = None
) -> None:
    """
    전역 로깅 시스템을 설정합니다.
    
    Args:
        log_level (str): 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file (Optional[str]): 로그 파일 경로 (None이면 파일 로깅 비활성화)
        max_size (int): 로그 파일 최대 크기 (MB)
        backup_count (int): 백업 파일 수
        console_output (bool): 콘솔 출력 여부
        format_string (Optional[str]): 로그 포맷 문자열
    """
    
    # 로그 레벨 설정
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    log_level_numeric = level_map.get(log_level.upper(), logging.INFO)
    
    # 기본 포맷 설정
    if format_string is None:
        format_string = (
            '%(asctime)s - %(name)s - %(levelname)s - '
            '%(filename)s:%(lineno)d - %(message)s'
        )
    
    formatter = logging.Formatter(
        format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_numeric)
    
    # 기존 핸들러 제거 (중복 방지)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 콘솔 핸들러 추가
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level_numeric)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # 파일 핸들러 추가
    if log_file:
        try:
            # 로그 디렉토리 생성
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 로테이팅 파일 핸들러 생성
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=max_size * 1024 * 1024,  # MB to bytes
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(log_level_numeric)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            # 파일 로깅 실패시 경고만 출력하고 계속 진행
            print(f"Warning: 파일 로깅 설정 실패 - {e}")


def get_logger(name: str, config: Optional[Dict[str, Any]] = None) -> logging.Logger:
    """
    모듈별 로거를 생성합니다.
    
    Args:
        name (str): 로거 이름 (보통 __name__ 사용)
        config (Optional[Dict[str, Any]]): 로깅 설정 (None이면 기본값 사용)
        
    Returns:
        logging.Logger: 설정된 로거 인스턴스
        
    Examples:
        >>> logger = get_logger(__name__)
        >>> logger.info("시작")
    """
    
    # 설정이 제공되지 않은 경우 기본값 사용
    if config is None:
        config = {
            'log_level': 'INFO',
            'file_path': 'logs/app.log',
            'max_size': 10,
            'backup_count': 5,
            'console_output': True
        }
    
    # 전역 로깅이 설정되지 않았다면 설정
    if not logging.getLogger().handlers:
        setup_logging(
            log_level=config.get('log_level', 'INFO'),
            log_file=config.get('file_path'),
            max_size=config.get('max_size', 10),
            backup_count=config.get('backup_count', 5),
            console_output=config.get('console_output', True)
        )
    
    return logging.getLogger(name)


def log_function_call(func):
    """
    함수 호출을 로깅하는 데코레이터입니다.
    
    Args:
        func: 데코레이트할 함수
        
    Returns:
        함수 래퍼
        
    Examples:
        >>> @log_function_call
        >>> def my_function(x, y):
        >>>     return x + y
    """
    import functools
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        # 함수 시작 로그
        logger.debug(f"함수 시작: {func.__name__}")
        
        try:
            # 함수 실행
            result = func(*args, **kwargs)
            
            # 함수 완료 로그
            logger.debug(f"함수 완료: {func.__name__}")
            
            return result
            
        except Exception as e:
            # 에러 로그
            logger.error(f"함수 에러: {func.__name__} - {e}")
            raise
            
    return wrapper


def log_execution_time(func):
    """
    함수 실행 시간을 로깅하는 데코레이터입니다.
    
    Args:
        func: 데코레이트할 함수
        
    Returns:
        함수 래퍼
    """
    import functools
    import time
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger(func.__module__)
        
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(f"{func.__name__} 실행 시간: {execution_time:.2f}초")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} 실행 실패 ({execution_time:.2f}초) - {e}")
            raise
            
    return wrapper


class ContextualLogger:
    """
    컨텍스트 정보를 포함하는 로거 클래스입니다.
    """
    
    def __init__(self, logger: logging.Logger, context: Dict[str, Any]):
        """
        Args:
            logger (logging.Logger): 기본 로거
            context (Dict[str, Any]): 컨텍스트 정보
        """
        self.logger = logger
        self.context = context
    
    def _log_with_context(self, level: int, message: str, **kwargs):
        """컨텍스트 정보와 함께 로그를 기록합니다."""
        extra = kwargs.get('extra', {})
        extra.update(self.context)
        kwargs['extra'] = extra
        
        self.logger.log(level, message, **kwargs)
    
    def debug(self, message: str, **kwargs):
        self._log_with_context(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        self._log_with_context(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self._log_with_context(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self._log_with_context(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        self._log_with_context(logging.CRITICAL, message, **kwargs)


def get_contextual_logger(name: str, context: Dict[str, Any]) -> ContextualLogger:
    """
    컨텍스트 정보를 포함하는 로거를 생성합니다.
    
    Args:
        name (str): 로거 이름
        context (Dict[str, Any]): 컨텍스트 정보
        
    Returns:
        ContextualLogger: 컨텍스트 로거
        
    Examples:
        >>> context = {'user_id': '12345', 'session_id': 'abc123'}
        >>> logger = get_contextual_logger(__name__, context)
        >>> logger.info("사용자 로그인")
    """
    base_logger = get_logger(name)
    return ContextualLogger(base_logger, context)


def setup_structured_logging(service_name: str = "ecommerce-analytics"):
    """
    구조화된 로깅을 설정합니다 (JSON 형태).
    
    Args:
        service_name (str): 서비스 이름
    """
    import json
    
    class StructuredFormatter(logging.Formatter):
        """JSON 형태의 구조화된 로그 포맷터"""
        
        def format(self, record):
            log_data = {
                'timestamp': datetime.utcnow().isoformat(),
                'service': service_name,
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            # 추가 컨텍스트 정보가 있으면 포함
            if hasattr(record, 'extra'):
                log_data.update(record.extra)
            
            return json.dumps(log_data, ensure_ascii=False)
    
    # 기존 핸들러에 새 포맷터 적용
    formatter = StructuredFormatter()
    
    for handler in logging.getLogger().handlers:
        handler.setFormatter(formatter)


def create_performance_logger(name: str) -> logging.Logger:
    """
    성능 모니터링용 로거를 생성합니다.
    
    Args:
        name (str): 로거 이름
        
    Returns:
        logging.Logger: 성능 로거
    """
    logger = logging.getLogger(f"performance.{name}")
    
    # 성능 로그 전용 파일 핸들러
    try:
        perf_handler = logging.handlers.RotatingFileHandler(
            'logs/performance.log',
            maxBytes=50 * 1024 * 1024,  # 50MB
            backupCount=3,
            encoding='utf-8'
        )
        
        # 성능 로그 전용 포맷
        perf_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        perf_handler.setFormatter(perf_formatter)
        logger.addHandler(perf_handler)
        logger.setLevel(logging.INFO)
        
    except Exception as e:
        print(f"Warning: 성능 로거 설정 실패 - {e}")
    
    return logger


def safe_log_exception(logger: logging.Logger, exception: Exception, context: str = ""):
    """
    예외를 안전하게 로깅합니다.
    
    Args:
        logger (logging.Logger): 로거
        exception (Exception): 로깅할 예외
        context (str): 추가 컨텍스트 정보
    """
    import traceback
    
    try:
        error_msg = f"{context} - {type(exception).__name__}: {str(exception)}"
        logger.error(error_msg)
        logger.debug(traceback.format_exc())
        
    except Exception:
        # 로깅 자체가 실패하면 최소한 print
        print(f"로깅 실패 - 원본 에러: {exception}")


# 기본 로깅 설정 (모듈 import시 자동 실행)
def _initialize_default_logging():
    """기본 로깅 시스템을 초기화합니다."""
    try:
        # 환경변수에서 로그 레벨 가져오기
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # 기본 로깅 설정
        setup_logging(
            log_level=log_level,
            log_file='logs/app.log',
            console_output=True
        )
        
    except Exception as e:
        # 로깅 설정 실패시에도 모듈은 import 되어야 함
        print(f"Warning: 기본 로깅 설정 실패 - {e}")


# 모듈 import시 기본 로깅 초기화
if not logging.getLogger().handlers:
    _initialize_default_logging()


if __name__ == "__main__":
    """
    이 스크립트를 직접 실행하면 로깅 시스템 테스트를 수행합니다.
    """
    print("=== Logger 시스템 테스트 ===")
    
    # 기본 로거 테스트
    logger = get_logger(__name__)
    
    logger.debug("디버그 메시지")
    logger.info("정보 메시지")
    logger.warning("경고 메시지")
    logger.error("에러 메시지")
    
    # 컨텍스트 로거 테스트
    context = {'test_id': '12345', 'module': 'logger_test'}
    ctx_logger = get_contextual_logger(__name__, context)
    ctx_logger.info("컨텍스트 포함 메시지")
    
    # 데코레이터 테스트
    @log_execution_time
    def test_function():
        import time
        time.sleep(0.1)
        return "테스트 완료"
    
    result = test_function()
    logger.info(f"함수 결과: {result}")
    
    # 예외 로깅 테스트
    try:
        raise ValueError("테스트 예외")
    except Exception as e:
        safe_log_exception(logger, e, "테스트 중")
    
    print("=== 테스트 완료 ===") 