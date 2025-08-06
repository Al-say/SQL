#!/usr/bin/env python3
"""
SQL数据库管理工具 - 主应用程序入口

提供完整的数据库管理功能，包括连接管理、查询执行、模式管理等。
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.app import SQLManagerApp
from src.utils.logger import setup_logger
from src.utils.config import load_config


def main():
    """主函数 - 启动SQL管理工具"""
    try:
        # 设置日志
        logger = setup_logger()
        logger.info("启动SQL数据库管理工具...")
        
        # 加载配置
        config = load_config()
        
        # 创建并启动应用
        app = SQLManagerApp(config)
        app.run()
        
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
