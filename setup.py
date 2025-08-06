#!/usr/bin/env python3
"""
SQL数据库管理工具安装脚本
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# 读取requirements文件
def read_requirements(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f 
                   if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        return []

setup(
    name="sql-manager",
    version="1.0.0",
    description="SQL数据库管理工具",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    author="Al-say",
    author_email="your-email@example.com",
    url="https://github.com/Al-say/SQL",
    packages=find_packages(),
    python_requires=">=3.7",
    
    # 基础依赖（空，只需要标准库）
    install_requires=[],
    
    # 可选依赖
    extras_require={
        'full': [
            'SQLAlchemy>=1.4.0',
            'PyMySQL>=1.0.0',
            'psycopg2-binary>=2.9.0',
            'pyodbc>=4.0.30',
            'PyYAML>=6.0',
            'pandas>=1.3.0',
            'numpy>=1.21.0',
            'matplotlib>=3.4.0',
            'plotly>=5.0.0',
            'seaborn>=0.11.0',
            'python-dotenv>=0.19.0',
            'click>=8.0.0',
            'rich>=10.0.0',
            'tabulate>=0.8.9',
            'cryptography>=3.4.0',
            'python-dateutil>=2.8.0',
        ],
        'database': [
            'SQLAlchemy>=1.4.0',
            'PyMySQL>=1.0.0',
            'psycopg2-binary>=2.9.0',
            'pyodbc>=4.0.30',
        ],
        'analysis': [
            'pandas>=1.3.0',
            'numpy>=1.21.0',
            'matplotlib>=3.4.0',
            'plotly>=5.0.0',
            'seaborn>=0.11.0',
        ],
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'black>=21.0.0',
            'flake8>=3.9.0',
            'mypy>=0.910',
        ]
    },
    
    # 入口点
    entry_points={
        'console_scripts': [
            'sql-manager=src.main:main',
        ],
    },
    
    # 包含的数据文件
    package_data={
        '': ['*.md', '*.txt', '*.yml', '*.yaml', '*.json', '*.example'],
    },
    
    # 项目分类
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    
    # 关键词
    keywords="sql database management gui tkinter mysql postgresql sqlite",
    
    # 项目链接
    project_urls={
        'Bug Reports': 'https://github.com/Al-say/SQL/issues',
        'Source': 'https://github.com/Al-say/SQL',
        'Documentation': 'https://github.com/Al-say/SQL/blob/master/README.md',
    },
)
