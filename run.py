#!/usr/bin/env python3
"""
SQL管理工具快速启动脚本

这是一个简化的启动脚本，提供基本的命令行选项。
"""

import sys
import os
import argparse
from pathlib import Path

# 添加源代码路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SQL数据库管理工具')
    parser.add_argument('--config', '-c', help='配置文件路径')
    parser.add_argument('--debug', '-d', action='store_true', help='启用调试模式')
    parser.add_argument('--version', '-v', action='version', version='SQL Manager v1.0.0')
    
    args = parser.parse_args()
    
    try:
        # 导入并启动应用
        from src.main import main as app_main
        
        # 设置调试模式
        if args.debug:
            os.environ['SQL_MANAGER_DEBUG'] = '1'
        
        # 设置配置文件
        if args.config:
            os.environ['SQL_MANAGER_CONFIG'] = args.config
        
        print("启动SQL管理工具...")
        app_main()
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包：pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
