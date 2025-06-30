"""
Data Generation Package - 데이터 생성 패키지
=========================================

이 패키지는 실제같은 전자상거래 데이터를 생성하는 모듈들을 포함합니다.
외부 API에 의존하지 않고 로컬에서 완전히 동작하도록 설계되었습니다.

주요 모듈:
    - data_generator: 통합 데이터 생성기 (메인)
    - customer_generator: 고객 데이터 생성
    - product_generator: 상품 데이터 생성  
    - order_generator: 주문 데이터 생성

특징:
    - 현실적인 패턴 반영 (계절성, 트렌드)
    - 일관성 있는 데이터 관계
    - 커스터마이징 가능한 설정
    - 확장성과 재현 가능성

사용 예시:
    >>> from src.data_generation import DataGenerator
    >>> generator = DataGenerator()
    >>> data = generator.generate_all()
    >>> customers_df = data['customers']
    >>> products_df = data['products']
    >>> orders_df = data['orders']
"""

try:
    from .data_generator import DataGenerator
    
    __all__ = [
        'DataGenerator',
    ]
    
except ImportError as e:
    print(f"Warning: 데이터 생성 모듈 import 실패 - {e}")
    __all__ = [] 