"""
Data Generator - 통합 데이터 생성기
=================================

이 모듈은 전자상거래 분석을 위한 현실적인 가상 데이터를 생성합니다.
외부 API나 라이브러리에 의존하지 않고 완전히 로컬에서 동작합니다.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from pathlib import Path


class DataGenerator:
    """전자상거래 데이터 생성기"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, random_seed: int = 42):
        """데이터 생성기 초기화"""
        
        # 시드 설정
        random.seed(random_seed)
        np.random.seed(random_seed)
        
        # 기본 설정
        self.config = config if config else self._get_default_config()
        
        # 생성할 데이터 크기
        self.n_customers = self.config.get('n_customers', 1000)
        self.n_products = self.config.get('n_products', 100)
        self.n_orders = self.config.get('n_orders', 5000)
        
        # 날짜 범위
        self.start_date = datetime.strptime(
            self.config.get('start_date', '2023-01-01'), '%Y-%m-%d'
        )
        self.end_date = datetime.strptime(
            self.config.get('end_date', '2024-12-31'), '%Y-%m-%d'
        )
        
        print(f"데이터 생성기 초기화 완료")
        print(f"- 고객: {self.n_customers:,}명")
        print(f"- 상품: {self.n_products:,}개") 
        print(f"- 주문: {self.n_orders:,}건")
    
    def _get_default_config(self) -> Dict[str, Any]:
        """기본 설정을 반환합니다."""
        return {
            'n_customers': 1000,
            'n_products': 100,
            'n_orders': 5000,
            'start_date': '2023-01-01',
            'end_date': '2024-12-31'
        }
    
    def generate_customers(self) -> pd.DataFrame:
        """고객 데이터를 생성합니다."""
        print("고객 데이터 생성 중...")
        
        customers = []
        korean_surnames = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임']
        korean_names = ['민준', '서준', '예준', '도윤', '시우', '서연', '하은', '하윤', '지민', '채원']
        
        for i in range(self.n_customers):
            customer_id = f"CUST_{i+1:06d}"
            
            # 이름 생성
            surname = random.choice(korean_surnames)
            given_name = random.choice(korean_names)
            full_name = f"{surname}{given_name}"
            
            # 나이와 성별
            age = max(18, min(80, int(np.random.normal(40, 15))))
            gender = random.choice(['M', 'F'])
            
            # 지역
            regions = ['서울', '부산', '대구', '인천', '광주', '대전', '경기', '강원']
            region = random.choice(regions)
            
            # 가입일
            days_ago = random.randint(30, 1095)
            registration_date = self.end_date - timedelta(days=days_ago)
            
            # 고객 세그먼트
            segment_prob = random.random()
            if segment_prob < 0.05:
                segment = 'VIP'
            elif segment_prob < 0.20:
                segment = 'Premium'
            elif segment_prob < 0.60:
                segment = 'Regular'
            else:
                segment = 'Budget'
            
            customers.append({
                'customer_id': customer_id,
                'name': full_name,
                'age': age,
                'gender': gender,
                'region': region,
                'segment': segment,
                'registration_date': registration_date.date()
            })
        
        customers_df = pd.DataFrame(customers)
        print(f"고객 데이터 생성 완료: {len(customers_df):,}건")
        return customers_df
    
    def generate_products(self) -> pd.DataFrame:
        """상품 데이터를 생성합니다."""
        print("상품 데이터 생성 중...")
        
        products = []
        categories = ['전자기기', '패션', '생활용품', '뷰티', '가전', '스포츠']
        brands = ['삼성', '애플', 'LG', '나이키', '아디다스', '유니클로']
        
        for i in range(self.n_products):
            product_id = f"PROD_{i+1:06d}"
            
            category = random.choice(categories)
            brand = random.choice(brands)
            product_name = f"{brand} {category} 상품 {i+1}"
            
            # 가격 설정
            if category == '전자기기':
                price = random.randint(100000, 2000000)
            elif category == '가전':
                price = random.randint(50000, 3000000)
            else:
                price = random.randint(10000, 300000)
            
            # 가격을 1000원 단위로 반올림
            price = round(price / 1000) * 1000
            
            # 할인율
            discount_rate = 0
            if random.random() < 0.3:
                discount_rate = random.choice([5, 10, 15, 20, 25, 30])
            
            final_price = int(price * (1 - discount_rate / 100))
            
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'category': category,
                'brand': brand,
                'price': price,
                'discount_rate': discount_rate,
                'final_price': final_price,
                'stock': random.randint(10, 1000)
            })
        
        products_df = pd.DataFrame(products)
        print(f"상품 데이터 생성 완료: {len(products_df):,}건")
        return products_df
    
    def generate_orders(self, customers_df: pd.DataFrame, products_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """주문 및 주문 상품 데이터를 생성합니다."""
        print("주문 데이터 생성 중...")
        
        orders = []
        order_items = []
        
        for i in range(self.n_orders):
            order_id = f"ORD_{i+1:08d}"
            
            # 고객 선택
            customer = customers_df.sample(1).iloc[0]
            customer_id = customer['customer_id']
            
            # 주문 날짜
            total_days = (self.end_date - self.start_date).days
            random_days = random.randint(0, total_days)
            order_date = self.start_date + timedelta(days=random_days)
            
            # 주문할 상품 수
            num_items = np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
            
            # 상품 선택
            selected_products = products_df.sample(n=num_items)
            
            order_total = 0
            for _, product in selected_products.iterrows():
                quantity = random.randint(1, 3)
                item_total = product['final_price'] * quantity
                order_total += item_total
                
                order_items.append({
                    'order_id': order_id,
                    'product_id': product['product_id'],
                    'product_name': product['product_name'],
                    'unit_price': product['final_price'],
                    'quantity': quantity,
                    'total_price': item_total
                })
            
            # 배송비
            shipping_cost = 0 if order_total >= 50000 else 3000
            final_amount = order_total + shipping_cost
            
            # 주문 상태
            order_status = np.random.choice(['완료', '배송중', '취소'], p=[0.85, 0.1, 0.05])
            
            orders.append({
                'order_id': order_id,
                'customer_id': customer_id,
                'order_date': order_date.date(),
                'order_status': order_status,
                'subtotal': order_total,
                'shipping_cost': shipping_cost,
                'final_amount': final_amount
            })
        
        orders_df = pd.DataFrame(orders)
        order_items_df = pd.DataFrame(order_items)
        
        print(f"주문 데이터 생성 완료: {len(orders_df):,}건")
        print(f"주문 상품 데이터 생성 완료: {len(order_items_df):,}건")
        
        return orders_df, order_items_df
    
    def generate_all(self, save_to_file: bool = True) -> Dict[str, pd.DataFrame]:
        """모든 데이터를 생성합니다."""
        print("\n=== E-commerce 데이터 생성 시작 ===")
        
        # 1. 고객 데이터 생성
        customers_df = self.generate_customers()
        
        # 2. 상품 데이터 생성
        products_df = self.generate_products()
        
        # 3. 주문 데이터 생성
        orders_df, order_items_df = self.generate_orders(customers_df, products_df)
        
        # 파일 저장
        if save_to_file:
            self.save_to_files(customers_df, products_df, orders_df, order_items_df)
        
        print("\n=== 데이터 생성 완료 ===")
        
        return {
            'customers': customers_df,
            'products': products_df,
            'orders': orders_df,
            'order_items': order_items_df
        }
    
    def save_to_files(self, customers_df, products_df, orders_df, order_items_df, output_dir: str = 'data/raw'):
        """생성된 데이터를 CSV 파일로 저장합니다."""
        print(f"데이터 파일 저장 중 ({output_dir})...")
        
        # 출력 디렉토리 생성
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # CSV 파일로 저장
        customers_df.to_csv(f'{output_dir}/customers.csv', index=False, encoding='utf-8-sig')
        products_df.to_csv(f'{output_dir}/products.csv', index=False, encoding='utf-8-sig')
        orders_df.to_csv(f'{output_dir}/orders.csv', index=False, encoding='utf-8-sig')
        order_items_df.to_csv(f'{output_dir}/order_items.csv', index=False, encoding='utf-8-sig')
        
        print("파일 저장 완료 ✓")


def main():
    """메인 함수"""
    config = {
        'n_customers': 1000,
        'n_products': 100,
        'n_orders': 5000
    }
    
    generator = DataGenerator(config=config)
    data = generator.generate_all(save_to_file=True)
    print("모든 작업 완료!")


if __name__ == "__main__":
    main()
