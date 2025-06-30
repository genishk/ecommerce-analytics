"""
E-commerce Analytics Platform - Setup Configuration
==================================================

이 파일은 프로젝트를 Python 패키지로 설치하기 위한 설정 파일입니다.

설치 방법:
    pip install -e .    # 개발 모드 설치 (권장)
    pip install .       # 일반 설치

기능:
    - 프로젝트를 패키지로 설치
    - 의존성 자동 관리  
    - 명령줄 도구 등록
"""

from setuptools import setup, find_packages
import os

# README 파일 읽기
def read_readme():
    """README.md 파일 내용을 읽어옵니다."""
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "E-commerce Analytics Platform"

# requirements.txt에서 의존성 읽기
def read_requirements():
    """requirements.txt에서 필요한 패키지 목록을 읽어옵니다."""
    requirements = []
    try:
        with open("requirements.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 주석이나 빈 줄 제외
                if line and not line.startswith("#") and not line.startswith("-"):
                    # 인라인 주석 제거
                    if "#" in line:
                        line = line.split("#")[0].strip()
                    requirements.append(line)
    except FileNotFoundError:
        print("Warning: requirements.txt not found")
    return requirements

setup(
    # 기본 정보
    name="ecommerce-analytics",
    version="1.0.0",
    author="genishk",
    author_email="sk4985@columbia.edu",
    description="종합적인 전자상거래 고객 분석 및 추천 시스템",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/genishk/ecommerce-analytics",
    
    # 패키지 설정
    packages=find_packages(exclude=["tests*", "docs*", "notebooks*"]),
    include_package_data=True,
    
    # Python 버전 요구사항
    python_requires=">=3.9",
    
    # 의존성
    install_requires=read_requirements(),
    
    # 개발용 의존성 (선택사항)
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0", 
            "black>=23.11.0",
            "flake8>=6.1.0",
        ],
        "full": [
            "torch>=2.1.2",
            "torchvision>=0.16.2",
        ]
    },
    
    # 명령줄 도구 등록
    entry_points={
        "console_scripts": [
            "ecommerce-generate-data=src.data_generation.data_generator:main",
            "ecommerce-dashboard=src.dashboard.main_dashboard:main",
            "ecommerce-api=src.api.main:main",
        ],
    },
    
    # 분류자 (PyPI용)
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    
    # 키워드
    keywords="ecommerce analytics machine-learning data-science recommendation-system",
    
    # 프로젝트 URL들
    project_urls={
        "Bug Reports": "https://github.com/genishk/ecommerce-analytics/issues",
        "Documentation": "https://github.com/genishk/ecommerce-analytics/docs",
        "Source": "https://github.com/genishk/ecommerce-analytics",
    },
) 