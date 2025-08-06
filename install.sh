#!/bin/bash

# SQL管理工具安装脚本

echo "================================="
echo "SQL管理工具安装程序"
echo "================================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
if [ -z "$python_version" ]; then
    echo "错误: 未找到Python 3"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

echo "发现Python版本: $python_version"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到pip3"
    echo "请先安装pip"
    exit 1
fi

echo "准备安装依赖包..."

# 安装基础依赖
echo "安装基础依赖..."
pip3 install --user --upgrade pip

# 尝试安装可选依赖
echo "安装可选依赖（如果失败会跳过）..."

dependencies=(
    "PyYAML"
    "pandas"
    "matplotlib"
    "SQLAlchemy"
    "PyMySQL"
    "psycopg2-binary"
    "pyodbc"
)

for dep in "${dependencies[@]}"; do
    echo "尝试安装 $dep..."
    if pip3 install --user "$dep" 2>/dev/null; then
        echo "✓ $dep 安装成功"
    else
        echo "⚠ $dep 安装失败（可选）"
    fi
done

echo ""
echo "================================="
echo "安装完成！"
echo "================================="
echo ""
echo "使用方法："
echo "1. 简化版（仅需Python标准库）:"
echo "   python3 simple_sql_manager.py"
echo ""
echo "2. 完整版（需要所有依赖）:"
echo "   python3 run.py"
echo ""
echo "3. 使用Makefile："
echo "   make run"
echo ""
echo "首次使用建议从简化版开始！"
