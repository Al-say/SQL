"""
SQL管理工具核心应用类

管理整个应用的生命周期，协调各个模块之间的交互。
"""

import sys
from typing import Dict, Any
from loguru import logger

from ..database.connection_manager import ConnectionManager
from ..database.query_executor import QueryExecutor
from ..ui.main_window import MainWindow
from ..utils.config import Config


class SQLManagerApp:
    """SQL管理工具主应用类"""
    
    def __init__(self, config: Config):
        """初始化应用
        
        Args:
            config: 应用配置对象
        """
        self.config = config
        self.connection_manager = ConnectionManager()
        self.query_executor = QueryExecutor(self.connection_manager)
        self.main_window = None
        
        logger.info("SQL管理工具初始化完成")
    
    def run(self):
        """启动应用"""
        try:
            logger.info("启动用户界面...")
            
            # 创建主窗口
            self.main_window = MainWindow(
                connection_manager=self.connection_manager,
                query_executor=self.query_executor,
                config=self.config
            )
            
            # 启动GUI事件循环
            self.main_window.run()
            
        except Exception as e:
            logger.error(f"应用运行失败: {e}")
            raise
    
    def shutdown(self):
        """关闭应用"""
        logger.info("正在关闭应用...")
        
        # 关闭所有数据库连接
        if self.connection_manager:
            self.connection_manager.close_all_connections()
        
        # 关闭主窗口
        if self.main_window:
            self.main_window.close()
        
        logger.info("应用已关闭")
