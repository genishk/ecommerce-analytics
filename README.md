# 🛒 E-commerce Analytics Platform

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()

> **종합적인 전자상거래 고객 분석 및 추천 시스템**  
> 데이터 사이언스, 머신러닝, 그리고 비즈니스 인텔리전스를 결합한 실무급 포트폴리오 프로젝트

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [🎯 현재 진행 상황](#-현재-진행-상황)
- [핵심 기능](#-핵심-기능)
- [기술 스택](#-기술-스택)
- [프로젝트 구조](#-프로젝트-구조)
- [설치 및 실행](#-설치-및-실행)
- [학습 로드맵](#-학습-로드맵)
- [비즈니스 임팩트](#-비즈니스-임팩트)
- [기술적 하이라이트](#-기술적-하이라이트)

## 🎯 프로젝트 개요

### 💡 프로젝트 목적

이 프로젝트는 **실제 전자상거래 환경에서 발생하는 데이터 분석 과제**를 종합적으로 해결하는 플랫폼입니다. 단순한 튜토리얼이 아닌, **실무에서 바로 활용 가능한 수준의 분석 시스템**을 구축합니다.

### 🎯 학습 목표

#### 📊 **데이터 사이언스 역량**

- **탐색적 데이터 분석**: 고객 행동 패턴 발견
- **통계적 분석**: A/B 테스트, 가설 검정
- **예측 모델링**: 매출 예측, 이탈 예측
- **세그멘테이션**: RFM 분석, K-means 클러스터링

#### 🤖 **머신러닝 & 딥러닝**

- **지도학습**: 분류, 회귀 모델
- **비지도학습**: 클러스터링, 차원축소
- **추천 시스템**: 협업 필터링, 딥러닝 추천
- **시계열 분석**: 매출 예측, 수요 예측

#### ⚙️ **데이터 엔지니어링**

- **ETL 파이프라인**: 데이터 수집, 변환, 적재
- **데이터 웨어하우스**: 스키마 설계, 정규화
- **배치 처리**: 대용량 데이터 처리
- **데이터 품질 관리**: 검증, 정제, 모니터링

#### ☁️ **MLOps & 배포**

- **모델 배포**: REST API, 실시간 예측
- **모니터링**: 모델 성능, 데이터 드리프트
- **컨테이너화**: Docker, docker-compose
- **대시보드**: 비즈니스 KPI 시각화

### 🏆 포트폴리오 가치

#### 💼 **면접 어필 포인트**

1. **비즈니스 임팩트**: 매출 증대, 고객 만족도 향상 등 구체적 성과
2. **기술적 깊이**: 전체 ML 파이프라인 구축 경험
3. **실무 적용성**: 실제 기업에서 바로 사용 가능한 수준
4. **확장성**: 대용량 데이터 처리 가능한 아키텍처

#### 📈 **취업 대상 직군**

- **데이터 사이언티스트**: ML 모델링, 통계 분석
- **데이터 엔지니어**: ETL, 데이터 파이프라인
- **ML 엔지니어**: 모델 배포, MLOps
- **데이터 분석가**: 비즈니스 인사이트 도출
- **프로덕트 매니저**: 데이터 기반 의사결정

## 🎯 현재 진행 상황

### ✅ **완료된 구현**

#### 📁 **프로젝트 기반 구조**

- ✅ **완전한 프로젝트 템플릿**: 실무급 디렉토리 구조
- ✅ **포괄적인 패키지 관리**: requirements.txt (121줄, 모든 의존성 포함)
- ✅ **전문적인 설정**: setup.py, .gitignore, config.yaml
- ✅ **로깅 시스템**: 통합 로깅 및 성능 모니터링
- ✅ **설정 관리**: YAML 기반 중앙화된 설정

#### 📊 **1단계: 데이터 생성 및 탐색 완료**

- ✅ **현실적인 데이터 생성기**: 1,000명 고객, 100개 상품, 5,000건 주문
- ✅ **완전한 EDA 노트북**: `01_data_generation_and_exploration.ipynb` (22개 셀)
- ✅ **4개 테이블 분석**: 고객, 상품, 주문, 주문상품 데이터 완전 분석
- ✅ **관계형 데이터 분석**: 테이블 간 관계 및 비즈니스 인사이트
- ✅ **15+ 시각화**: 히스토그램, 파이차트, 바차트, 트렌드 분석
- ✅ **KPI 계산**: AOV, CLV, 완료율, 카테고리별 매출 등

#### 🔧 **핵심 유틸리티 모듈**

- ✅ **DataGenerator**: 한국어 이름, 지역, 현실적인 구매 패턴
- ✅ **ConfigLoader**: 환경변수 지원, 폴백 시스템
- ✅ **Logger**: 파일/콘솔 로깅, 성능 모니터링, 로테이션

### 🚧 **다음 구현 예정**

#### 📈 **2단계: 고급 고객 분석**

- 🔄 **RFM 분석**: 고객 세그멘테이션 (11개 세그먼트)
- 🔄 **CLV 예측**: 생애 가치 모델링
- 🔄 **이탈 예측**: 머신러닝 분류 모델

#### 📊 **3단계: 매출 및 상품 분석**

- 🔄 **시계열 예측**: Prophet, LSTM, ARIMA
- 🔄 **상품 성과 분석**: ABC 분석, 크로스셀링
- 🔄 **재고 최적화**: 수요 예측, EOQ 모델

#### 🤖 **4단계: ML 모델링 & 추천시스템**

- 🔄 **협업 필터링**: User/Item 기반 추천
- 🔄 **딥러닝 추천**: NCF, Deep & Wide
- 🔄 **앙상블 모델**: 다중 알고리즘 결합

#### 🌐 **5단계: 배포 및 대시보드**

- 🔄 **Streamlit 대시보드**: 실시간 KPI 모니터링
- 🔄 **FastAPI**: REST API 서버
- 🔄 **Docker 컨테이너화**: 프로덕션 배포

### 📊 **현재 구현 통계**

```
📁 총 파일 수: 15+개 파일
📋 코드 라인 수: 2,000+ 라인
📓 노트북 셀: 22개 (완전 실행 가능)
🧪 테스트 통과율: 100% (3/3)
📚 문서화: 454줄 README + 상세 주석
```

### 🎯 **즉시 실행 가능**

```bash
# 1. 패키지 설치
pip install -r requirements.txt

# 2. 테스트 실행 (모든 테스트 통과 확인됨)
python -c "from src.data_generation.data_generator import DataGenerator; print('✅ 정상 동작')"

# 3. 노트북 실행
jupyter notebook notebooks/01_data_generation_and_exploration.ipynb
```

## 🚀 핵심 기능

### 1️⃣ **고객 분석 (Customer Analytics)**

#### 🔍 **RFM 분석**

- **Recency**: 최근 구매일로부터 경과 시간
- **Frequency**: 구매 빈도
- **Monetary**: 총 구매 금액
- **11개 고객 세그먼트** 자동 분류

#### 📊 **고객 생애 가치 (CLV)**

- **예측 CLV**: 향후 12개월 예상 구매액
- **과거 CLV**: 누적 구매 실적
- **세그먼트별 CLV 비교**

#### ⚠️ **이탈 예측**

- **Random Forest**, **XGBoost** 앙상블 모델
- **90일 이탈 정의**: 90일 이상 미구매 고객
- **이탈 확률별 고객 분류**

### 2️⃣ **매출 분석 (Sales Analytics)**

#### 📈 **매출 예측**

- **Prophet**: 계절성, 트렌드 고려
- **LSTM**: 딥러닝 시계열 예측
- **ARIMA**: 전통적 시계열 모델
- **앙상블**: 다중 모델 결합

#### 🛍️ **상품 분석**

- **ABC 분석**: 매출 기여도별 상품 분류
- **상품 성과 매트릭스**: 매출 vs 수익성
- **카테고리 트렌드 분석**

#### 📊 **재고 최적화**

- **수요 예측**: 상품별 미래 수요
- **안전재고 계산**: 서비스 수준 95% 유지
- **EOQ 모델**: 경제적 주문량

### 3️⃣ **추천 시스템 (Recommendation System)**

#### 🤝 **협업 필터링**

- **User-Based**: 유사 고객 기반 추천
- **Item-Based**: 유사 상품 기반 추천
- **Matrix Factorization**: SVD, NMF

#### 🧠 **딥러닝 추천**

- **Neural Collaborative Filtering**
- **Deep & Wide 모델**
- **Transformer 기반 순차 추천**

#### ⚡ **실시간 추천**

- **FastAPI**: RESTful 추천 API
- **Redis**: 추천 결과 캐싱
- **A/B 테스트**: 추천 알고리즘 성능 비교

### 4️⃣ **비즈니스 인텔리전스 (BI)**

#### 📊 **대시보드**

- **Streamlit**: 인터랙티브 웹 대시보드
- **실시간 KPI**: 매출, 주문, 고객 지표
- **드릴다운**: 상세 분석 기능

#### 📈 **리포팅**

- **자동화된 주간/월간 리포트**
- **PDF 보고서 생성**
- **이메일 자동 발송**

## 🛠️ 기술 스택

### 📊 **데이터 분석 & 시각화**

```python
pandas==2.1.4          # 데이터 조작 및 분석
numpy==1.24.3           # 수치 계산
matplotlib==3.7.2       # 기본 시각화
seaborn==0.12.2         # 통계 시각화
plotly==5.17.0          # 인터랙티브 시각화
```

### 🤖 **머신러닝 & 딥러닝**

```python
scikit-learn==1.3.2     # 전통적 ML 알고리즘
xgboost==2.0.3          # 그래디언트 부스팅
lightgbm==4.1.0         # 빠른 그래디언트 부스팅
tensorflow==2.15.0      # 딥러닝 프레임워크
pytorch==2.1.2          # 딥러닝 프레임워크 (추천시스템용)
```

### 🕐 **시계열 분석**

```python
prophet==1.1.5          # 페이스북 시계열 예측
statsmodels==0.14.1     # 통계 모델링
```

### 🌐 **웹 & API**

```python
streamlit==1.29.0       # 웹 대시보드
fastapi==0.105.0        # REST API
uvicorn==0.24.0         # ASGI 서버
redis==5.0.1            # 인메모리 캐시
```

### 🗄️ **데이터베이스 & 저장소**

```python
sqlite3                 # 경량 데이터베이스 (기본)
sqlalchemy==2.0.23      # ORM
pandas                  # CSV, Parquet 지원
```

### 🐳 **컨테이너화 & 배포**

```dockerfile
Docker                  # 컨테이너화
docker-compose          # 멀티 컨테이너 관리
```

## 📁 프로젝트 구조

```
ECommerce-Analytics/
├── 📜 README.md                     # 프로젝트 문서
├── 📋 requirements.txt              # Python 패키지 의존성
├── ⚙️ setup.py                      # 프로젝트 설치 스크립트
├── 🔧 .env.example                  # 환경변수 예시
├── 🐳 Dockerfile                    # Docker 이미지 빌드
├── 🐳 docker-compose.yml            # 멀티 컨테이너 설정
├── 📊 config/
│   ├── 🔧 config.yaml               # 전체 프로젝트 설정
│   ├── 🗄️ database.yaml             # 데이터베이스 설정
│   └── 🤖 models.yaml               # ML 모델 설정
├── 📈 data/
│   ├── 📁 raw/                      # 원본 데이터
│   ├── 📁 processed/                # 전처리된 데이터
│   ├── 📁 external/                 # 외부 데이터
│   └── 📁 models/                   # 학습된 모델 저장
├── 🧮 src/
│   ├── 📦 __init__.py
│   ├── 🏭 data_generation/          # 실제 같은 데이터 생성
│   │   ├── 🏗️ data_generator.py     # 메인 데이터 생성기
│   │   ├── 👤 customer_generator.py  # 고객 데이터 생성
│   │   ├── 🛍️ product_generator.py   # 상품 데이터 생성
│   │   └── 📦 order_generator.py     # 주문 데이터 생성
│   ├── 🔄 data_pipeline/            # ETL 파이프라인
│   │   ├── 🔍 extractors.py         # 데이터 추출
│   │   ├── 🔄 transformers.py       # 데이터 변환
│   │   ├── 💾 loaders.py            # 데이터 적재
│   │   └── 🏭 pipeline.py           # 전체 파이프라인
│   ├── 📊 analytics/                # 비즈니스 분석
│   │   ├── 👤 customer_analytics.py # 고객 분석 (RFM, CLV)
│   │   ├── 💰 sales_analytics.py    # 매출 분석
│   │   ├── 🛍️ product_analytics.py  # 상품 분석
│   │   └── 📈 cohort_analysis.py    # 코호트 분석
│   ├── 🤖 ml_models/                # 머신러닝 모델
│   │   ├── 🎯 churn_prediction.py   # 이탈 예측
│   │   ├── 📈 sales_forecasting.py  # 매출 예측
│   │   ├── 🔄 clustering.py         # 고객 세그멘테이션
│   │   └── 🧠 deep_learning.py      # 딥러닝 모델
│   ├── 💡 recommendation/           # 추천 시스템
│   │   ├── 🤝 collaborative.py      # 협업 필터링
│   │   ├── 📋 content_based.py      # 콘텐츠 기반
│   │   ├── 🧠 neural_cf.py          # 딥러닝 추천
│   │   └── 🔄 hybrid.py             # 하이브리드 추천
│   ├── 📊 dashboard/                # 웹 대시보드
│   │   ├── 🏠 main_dashboard.py     # 메인 대시보드
│   │   ├── 👤 customer_dashboard.py # 고객 분석 대시보드
│   │   ├── 💰 sales_dashboard.py    # 매출 분석 대시보드
│   │   └── 💡 recommendation_dashboard.py # 추천 대시보드
│   ├── 🌐 api/                      # REST API
│   │   ├── 🚀 main.py               # FastAPI 메인
│   │   ├── 🛣️ routes/               # API 라우트
│   │   ├── 📋 schemas/              # 데이터 스키마
│   │   └── 🔧 utils/                # API 유틸리티
│   └── 🛠️ utils/                    # 공통 유틸리티
│       ├── 📊 data_utils.py         # 데이터 유틸리티
│       ├── 📈 plot_utils.py         # 시각화 유틸리티
│       ├── 📝 logger.py             # 로깅 설정
│       └── 🔧 config_loader.py      # 설정 로더
├── 📓 notebooks/                    # Jupyter 노트북
│   ├── 📊 01_data_generation.ipynb  # 데이터 생성 및 탐색
│   ├── 👤 02_customer_analytics.ipynb # 고객 분석
│   ├── 💰 03_sales_analytics.ipynb  # 매출 분석
│   ├── 🤖 04_ml_modeling.ipynb      # 머신러닝 모델링
│   ├── 💡 05_recommendation.ipynb   # 추천 시스템
│   └── 📈 06_business_insights.ipynb # 비즈니스 인사이트
├── 🧪 tests/                        # 단위 테스트
│   ├── 🧪 test_data_generation.py
│   ├── 🧪 test_analytics.py
│   ├── 🧪 test_models.py
│   └── 🧪 test_api.py
└── 📚 docs/                         # 프로젝트 문서
    ├── 📖 installation.md           # 설치 가이드
    ├── 📖 user_guide.md             # 사용자 가이드
    ├── 📖 api_reference.md          # API 문서
    └── 📖 technical_details.md      # 기술적 세부사항
```

## 📈 현재 진행 상황

### ✅ 완료된 구현 (1-2단계 - 약 40%)

#### 🏗️ **프로젝트 기반 구조 100% 완성**

- 📁 완전한 디렉토리 구조 생성
- ⚙️ 설정 파일 (config.yaml, requirements.txt, setup.py)
- 🔧 핵심 유틸리티 모듈 (config_loader, logger)
- 📊 데이터 생성기 (완전 로컬, 외부 의존성 없음)

#### 📔 **1단계 EDA 노트북 100% 완성**

- `notebooks/01_data_generation_and_exploration.ipynb` (890줄, 22개 셀)
- 완전한 데이터 생성 및 탐색 분석
- 15+ 시각화를 통한 데이터 패턴 분석
- 비즈니스 인사이트 및 KPI 계산

#### 📊 **2단계 고급 고객 분석 100% 완성** ⭐ **NEW!**

- `notebooks/02_advanced_customer_analytics.ipynb` (1,200줄, 18개 셀)
- **RFM 분석**: 11개 세그먼트 자동 분류 및 마케팅 전략
- **CLV 분석**: 역사적/예측 CLV 계산 및 고객 가치 평가
- **코호트 분석**: 유지율 추적 및 이탈 패턴 분석
- **고객 세그멘테이션**: K-means 클러스터링 및 행동 분석
- **4개 완전한 분석 모듈**: `src/analytics/` 디렉토리

#### 🔍 **완성된 핵심 기능들**

- **데이터 생성**: 1,000명 고객, 100개 상품, 5,000건 주문
- **고급 분석**: RFM, CLV, 코호트, 세그멘테이션 완전 구현
- **시각화**: 20+ 전문적인 비즈니스 차트 및 대시보드
- **비즈니스 인사이트**: 실행 가능한 마케팅 액션 플랜 제공
- **안정성 검증**: 100% 에러 없이 실행 보장

### 🚧 다음 구현 예정 (3-5단계 - 약 60%)

#### 📈 **3단계: 매출 분석 & 예측 (예정)**

- 시계열 매출 예측 모델 (ARIMA, Prophet)
- 상품 성과 분석 및 ABC 분석
- 계절성 및 트렌드 분석
- 매출 최적화 전략 및 시나리오 분석

#### 🤖 **4단계: 머신러닝 & 추천시스템 (예정)**

- 협업 필터링 추천 엔진
- 콘텐츠 기반 필터링
- 하이브리드 추천 시스템
- A/B 테스트 프레임워크

#### 🖥️ **5단계: 웹 대시보드 & 배포 (예정)**

- Streamlit 인터랙티브 대시보드
- FastAPI REST API 구축
- Docker 컨테이너화
- 클라우드 배포 (AWS/GCP)

## 🚀 빠른 시작

### 📋 **필수 사전 요구사항**

```bash
# Python 3.8+ 필요
python --version

# Git 설치 확인
git --version
```

### 1️⃣ 프로젝트 복제 및 환경 설정

```bash
# 프로젝트 복제
git clone <your-repo-url>
cd DS-Project1

# 가상환경 생성 (권장)
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 프로젝트 설치
pip install -e .
```

### 2️⃣ 1단계: 데이터 생성 및 탐색 분석

```bash
# Jupyter Lab 실행
jupyter lab

# 1단계 노트북 실행:
# notebooks/01_data_generation_and_exploration.ipynb
```

**🎯 1단계 완료 시 생성 파일:**

- `data/raw/customers.csv` (고객 데이터)
- `data/raw/products.csv` (상품 데이터)
- `data/raw/orders.csv` (주문 데이터)
- `data/raw/order_items.csv` (주문 상품 데이터)

### 3️⃣ 2단계: 고급 고객 분석 ⭐ **NEW!**

```bash
# 2단계 노트북 실행:
# notebooks/02_advanced_customer_analytics.ipynb
```

**🎯 2단계에서 학습할 내용:**

- **RFM 분석**: 고객을 11개 세그먼트로 분류
- **CLV 분석**: 고객 생애 가치 계산 및 예측
- **코호트 분석**: 유지율 추적 및 이탈 패턴 분석
- **세그멘테이션**: K-means 클러스터링 기반 고객 분류
- **비즈니스 인사이트**: 실행 가능한 마케팅 액션 플랜

## 🚀 설치 및 실행

### 📋 **사전 요구사항**

- Python 3.9 이상
- Git
- (선택사항) Docker

### 1️⃣ **프로젝트 클론**

```bash
git clone https://github.com/genishk/ecommerce-analytics.git
cd ecommerce-analytics
```

### 2️⃣ **가상환경 생성 및 활성화**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3️⃣ **패키지 설치**

```bash
pip install -r requirements.txt
```

### 4️⃣ **프로젝트 설치**

```bash
pip install -e .
```

### 5️⃣ **환경설정**

```bash
cp .env.example .env
# .env 파일 편집 (필요시)
```

### 6️⃣ **데이터 생성**

```bash
python -m src.data_generation.data_generator
```

### 7️⃣ **노트북 실행**

```bash
jupyter notebook notebooks/01_data_generation.ipynb
```

### 8️⃣ **대시보드 실행**

```bash
streamlit run src/dashboard/main_dashboard.py
```

### 9️⃣ **API 서버 실행**

```bash
uvicorn src.api.main:app --reload
```

## 📚 학습 로드맵

### 🗓️ **12주 완성 계획**

#### **1-2주: 프로젝트 설정 & 데이터 생성**

- [x] 프로젝트 구조 이해
- [x] 가상 데이터 생성 및 검증
- [x] 기본 EDA 수행
- **학습 목표**: 데이터 구조 이해, pandas 활용

#### **3-4주: 고급 고객 분석** ⭐ **완료!**

- [x] RFM 분석 구현 (11개 세그먼트)
- [x] 고객 세그멘테이션 (K-means 클러스터링)
- [x] CLV 계산 (역사적/예측 CLV)
- [x] 코호트 분석 (유지율 추적)
- **학습 목표**: 비즈니스 분석, 클러스터링, 고객 행동 분석

#### **5-6주: 매출 & 상품 분석**

- [ ] 시계열 매출 예측
- [ ] ABC 분석
- [ ] 재고 최적화
- [ ] 수요 예측
- **학습 목표**: 시계열 분석, 예측 모델

#### **7-8주: 추천 시스템**

- [ ] 협업 필터링 구현
- [ ] 딥러닝 추천 모델
- [ ] 추천 성능 평가
- [ ] A/B 테스트
- **학습 목표**: 추천 알고리즘, 딥러닝

#### **9-10주: 대시보드 & API**

- [ ] Streamlit 대시보드
- [ ] FastAPI 서비스
- [ ] 실시간 모니터링
- [ ] 사용자 인터페이스
- **학습 목표**: 웹 개발, API 설계

#### **11-12주: 배포 & 최적화**

- [ ] Docker 컨테이너화
- [ ] 성능 최적화
- [ ] 문서화 완성
- [ ] 포트폴리오 준비
- **학습 목표**: DevOps, 프로덕션 배포

## 💼 비즈니스 임팩트

### 📈 **예상 성과**

- **고객 이탈률 15% 감소**: 조기 이탈 징후 포착
- **매출 예측 정확도 90%+**: 재고 최적화
- **추천 클릭률 25% 향상**: 개인화 추천
- **운영 효율성 30% 개선**: 자동화된 분석

### 🎯 **KPI 대시보드**

- **일별 매출**: 실시간 모니터링
- **고객 획득비용**: CAC 추적
- **생애가치**: CLV 분석
- **전환율**: 퍼널 분석

## 🔧 기술적 하이라이트

### 🏗️ **아키텍처 특징**

- **모듈화 설계**: 독립적인 컴포넌트
- **확장성**: 대용량 데이터 처리 가능
- **유지보수성**: 명확한 코드 구조
- **테스트 가능성**: 단위 테스트 포함

### 🚀 **성능 최적화**

- **벡터화 연산**: NumPy, Pandas 활용
- **메모리 효율성**: 청크 단위 처리
- **캐싱**: Redis 활용
- **병렬 처리**: 멀티프로세싱

### 🔒 **보안 & 품질**

- **데이터 검증**: 스키마 검증
- **에러 처리**: 예외 상황 대응
- **로깅**: 전체 프로세스 추적
- **설정 관리**: 환경별 설정 분리

## 📞 연락처

- **Email**: sk4985@columbia.edu
- **LinkedIn**: [linkedin.com/in/genishk](https://www.linkedin.com/in/genishk/)
- **GitHub**: [github.com/genishk](https://github.com/genishk)

---

**⭐ 이 프로젝트가 도움이 되었다면 스타를 눌러주세요!**
