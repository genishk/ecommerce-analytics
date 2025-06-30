"""
Configuration Loader - 설정 파일 로더
===================================

이 모듈은 YAML 설정 파일을 안전하게 로드하고 검증하는 기능을 제공합니다.
에러 상황에서도 기본값으로 동작할 수 있도록 설계되었습니다.

주요 기능:
    - YAML 설정 파일 로드
    - 환경변수 치환
    - 기본값 제공
    - 설정 검증

사용 예시:
    >>> from src.utils.config_loader import load_config
    >>> config = load_config()
    >>> data_path = config['data']['paths']['raw']
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import warnings

# YAML 라이브러리 import (에러 대응)
try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False
    warnings.warn("PyYAML이 설치되지 않았습니다. 기본 설정을 사용합니다.")


def get_default_config() -> Dict[str, Any]:
    """
    기본 설정을 반환합니다.
    YAML 파일이 없거나 읽을 수 없을 때 사용됩니다.
    
    Returns:
        Dict[str, Any]: 기본 설정 딕셔너리
    """
    return {
        'project': {
            'name': 'E-commerce Analytics Platform',
            'version': '1.0.0',
            'description': '전자상거래 분석 플랫폼'
        },
        'environment': {
            'mode': 'development',
            'debug': True,
            'log_level': 'INFO',
            'random_seed': 42
        },
        'data': {
            'paths': {
                'raw': 'data/raw',
                'processed': 'data/processed',
                'external': 'data/external',
                'models': 'data/models'
            },
            'generation': {
                'n_customers': 1000,  # 작은 크기로 시작
                'n_products': 100,
                'n_orders': 5000,
                'start_date': '2023-01-01',
                'end_date': '2024-12-31',
                'seasonality_strength': 0.3,
                'trend_strength': 0.2
            },
            'validation': {
                'min_order_amount': 1.0,
                'max_order_amount': 10000.0,
                'max_missing_ratio': 0.05,
                'outlier_threshold': 3.0
            }
        },
        'analytics': {
            'rfm': {
                'analysis_date': 'auto',
                'quantiles': 5
            },
            'clv': {
                'prediction_period': 12,
                'discount_rate': 0.1
            },
            'churn': {
                'churn_threshold_days': 90,
                'feature_window_days': 180
            }
        },
        'machine_learning': {
            'common': {
                'train_size': 0.7,
                'val_size': 0.15,
                'test_size': 0.15,
                'cv_folds': 5
            },
            'models': {
                'random_forest': {
                    'n_estimators': 100,
                    'max_depth': 10,
                    'min_samples_split': 5
                },
                'xgboost': {
                    'n_estimators': 100,
                    'max_depth': 6,
                    'learning_rate': 0.1
                }
            }
        },
        'dashboard': {
            'streamlit': {
                'port': 8501,
                'page_title': 'E-commerce Analytics Dashboard',
                'layout': 'wide'
            }
        },
        'api': {
            'fastapi': {
                'host': 'localhost',
                'port': 8000,
                'debug': True
            }
        },
        'database': {
            'default': {
                'type': 'sqlite',
                'path': 'data/ecommerce.db'
            }
        },
        'logging': {
            'file_path': 'logs/app.log',
            'max_size': 10,
            'backup_count': 5,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    }


def find_config_file(config_name: str = 'config.yaml') -> Optional[Path]:
    """
    설정 파일을 찾습니다.
    
    Args:
        config_name (str): 설정 파일명
        
    Returns:
        Optional[Path]: 설정 파일 경로 (없으면 None)
    """
    # 현재 작업 디렉토리에서 시작
    current_dir = Path.cwd()
    
    # 가능한 경로들
    possible_paths = [
        current_dir / 'config' / config_name,
        current_dir / config_name,
        Path(__file__).parent.parent.parent / 'config' / config_name,
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_file():
            return path
            
    return None


def substitute_env_vars(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    설정값에서 환경변수를 치환합니다.
    ${VAR_NAME} 형태의 값을 환경변수로 치환합니다.
    
    Args:
        config (Dict[str, Any]): 원본 설정
        
    Returns:
        Dict[str, Any]: 환경변수가 치환된 설정
    """
    import re
    
    def replace_env_vars(value):
        if isinstance(value, str):
            # ${VAR_NAME} 패턴 찾기
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, value)
            
            for match in matches:
                env_value = os.getenv(match)
                if env_value is not None:
                    value = value.replace(f'${{{match}}}', env_value)
                    
        elif isinstance(value, dict):
            return {k: replace_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [replace_env_vars(item) for item in value]
            
        return value
    
    return replace_env_vars(config)


def validate_config(config: Dict[str, Any]) -> bool:
    """
    설정의 필수 필드들을 검증합니다.
    
    Args:
        config (Dict[str, Any]): 검증할 설정
        
    Returns:
        bool: 검증 통과 여부
    """
    required_fields = [
        'data.paths.raw',
        'data.paths.processed', 
        'data.generation.n_customers',
        'environment.random_seed'
    ]
    
    def get_nested_value(d, key_path):
        """중첩된 딕셔너리에서 값 가져오기"""
        keys = key_path.split('.')
        value = d
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return None
    
    for field in required_fields:
        if get_nested_value(config, field) is None:
            warnings.warn(f"필수 설정 필드가 없습니다: {field}")
            return False
            
    return True


def merge_configs(base_config: Dict[str, Any], 
                 override_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    두 설정을 병합합니다. override_config가 우선순위를 가집니다.
    
    Args:
        base_config (Dict[str, Any]): 기본 설정
        override_config (Dict[str, Any]): 덮어쓸 설정
        
    Returns:
        Dict[str, Any]: 병합된 설정
    """
    result = base_config.copy()
    
    for key, value in override_config.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value
            
    return result


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    설정 파일을 로드합니다.
    
    Args:
        config_path (Optional[str]): 설정 파일 경로 (None이면 자동 탐색)
        
    Returns:
        Dict[str, Any]: 로드된 설정
        
    Examples:
        >>> config = load_config()
        >>> config = load_config('custom_config.yaml')
    """
    # 기본 설정으로 시작
    config = get_default_config()
    
    if not YAML_AVAILABLE:
        print("Warning: PyYAML이 없어 기본 설정을 사용합니다.")
        return config
    
    # 설정 파일 찾기
    if config_path:
        file_path = Path(config_path)
        if not file_path.exists():
            print(f"Warning: 설정 파일 {config_path}를 찾을 수 없어 기본 설정을 사용합니다.")
            return config
    else:
        file_path = find_config_file()
        if not file_path:
            print("Warning: config.yaml 파일을 찾을 수 없어 기본 설정을 사용합니다.")
            return config
    
    # YAML 파일 로드
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml_config = yaml.safe_load(f)
            
        if yaml_config:
            # 기본 설정과 병합
            config = merge_configs(config, yaml_config)
            
            # 환경변수 치환
            config = substitute_env_vars(config)
            
            # 설정 검증
            if validate_config(config):
                print(f"설정 파일 로드 완료: {file_path}")
            else:
                print("Warning: 설정 검증 실패, 일부 기본값이 사용될 수 있습니다.")
        else:
            print("Warning: 설정 파일이 비어있어 기본 설정을 사용합니다.")
            
    except yaml.YAMLError as e:
        print(f"Warning: YAML 파싱 오류 - {e}")
        print("기본 설정을 사용합니다.")
    except FileNotFoundError:
        print(f"Warning: 설정 파일 {file_path}를 찾을 수 없습니다.")
        print("기본 설정을 사용합니다.")
    except Exception as e:
        print(f"Warning: 설정 로드 중 오류 발생 - {e}")
        print("기본 설정을 사용합니다.")
    
    return config


def save_config(config: Dict[str, Any], 
               output_path: str = 'config/config.yaml') -> bool:
    """
    설정을 YAML 파일로 저장합니다.
    
    Args:
        config (Dict[str, Any]): 저장할 설정
        output_path (str): 출력 파일 경로
        
    Returns:
        bool: 저장 성공 여부
    """
    if not YAML_AVAILABLE:
        print("Error: PyYAML이 설치되지 않아 설정을 저장할 수 없습니다.")
        return False
    
    try:
        # 출력 디렉토리 생성
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # YAML 파일로 저장
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, 
                     allow_unicode=True, indent=2)
                     
        print(f"설정 파일 저장 완료: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error: 설정 저장 실패 - {e}")
        return False


# 모듈 레벨에서 기본 설정 로드 (import 시점에 실행)
try:
    DEFAULT_CONFIG = load_config()
except Exception:
    DEFAULT_CONFIG = get_default_config()


if __name__ == "__main__":
    """
    이 스크립트를 직접 실행하면 설정 파일 테스트를 수행합니다.
    """
    print("=== Configuration Loader 테스트 ===")
    
    # 설정 로드 테스트
    config = load_config()
    print(f"프로젝트명: {config['project']['name']}")
    print(f"환경: {config['environment']['mode']}")
    print(f"데이터 경로: {config['data']['paths']['raw']}")
    
    # 설정 검증 테스트
    is_valid = validate_config(config)
    print(f"설정 검증 결과: {'통과' if is_valid else '실패'}")
    
    print("=== 테스트 완료 ===") 