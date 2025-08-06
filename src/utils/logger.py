"""
日志管理模块

配置和管理应用日志系统。
"""

import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(log_file: Optional[str] = None, 
                log_level: str = "INFO",
                max_size: str = "10MB",
                backup_count: int = 5,
                console_output: bool = True) -> logging.Logger:
    """设置日志系统
    
    Args:
        log_file: 日志文件路径
        log_level: 日志级别
        max_size: 日志文件最大大小
        backup_count: 备份文件数量
        console_output: 是否输出到控制台
    
    Returns:
        logging.Logger: 配置好的日志器
    """
    # 创建日志器
    logger = logging.getLogger('sql_manager')
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        try:
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            # 解析文件大小
            size_bytes = parse_size(max_size)
            
            # 创建轮转文件处理器
            file_handler = RotatingFileHandler(
                log_file, 
                maxBytes=size_bytes, 
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except Exception as e:
            print(f"设置文件日志失败: {e}")
    
    return logger


def parse_size(size_str: str) -> int:
    """解析大小字符串为字节数
    
    Args:
        size_str: 大小字符串，如 "10MB", "1GB"
    
    Returns:
        int: 字节数
    """
    size_str = size_str.upper().strip()
    
    # 单位映射
    units = {
        'B': 1,
        'KB': 1024,
        'MB': 1024 * 1024,
        'GB': 1024 * 1024 * 1024
    }
    
    # 提取数字和单位
    for unit, multiplier in units.items():
        if size_str.endswith(unit):
            number_str = size_str[:-len(unit)].strip()
            try:
                number = float(number_str)
                return int(number * multiplier)
            except ValueError:
                break
    
    # 如果解析失败，返回默认值 10MB
    return 10 * 1024 * 1024


def get_log_file_path() -> str:
    """获取默认日志文件路径"""
    home_dir = Path.home()
    log_dir = home_dir / '.sql_manager' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return str(log_dir / 'sql_manager.log')


class SQLManagerLogger:
    """SQL管理器日志类"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def debug(self, message: str):
        """调试日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """信息日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """严重错误日志"""
        self.logger.critical(message)
    
    def query_log(self, sql: str, execution_time: float, success: bool, error: Optional[str] = None):
        """查询日志"""
        status = "SUCCESS" if success else "FAILED"
        message = f"[QUERY] {status} - Time: {execution_time:.3f}s - SQL: {sql[:100]}..."
        
        if success:
            self.info(message)
        else:
            self.error(f"{message} - Error: {error}")
    
    def connection_log(self, action: str, connection_name: str, success: bool, error: Optional[str] = None):
        """连接日志"""
        status = "SUCCESS" if success else "FAILED"
        message = f"[CONNECTION] {action} - {connection_name} - {status}"
        
        if success:
            self.info(message)
        else:
            self.error(f"{message} - Error: {error}")


# 全局日志器实例
_global_logger: Optional[SQLManagerLogger] = None


def get_logger() -> SQLManagerLogger:
    """获取全局日志器实例"""
    global _global_logger
    
    if _global_logger is None:
        standard_logger = setup_logger(
            log_file=get_log_file_path(),
            console_output=True
        )
        _global_logger = SQLManagerLogger(standard_logger)
    
    return _global_logger


# 便捷函数
def log_debug(message: str):
    """记录调试信息"""
    get_logger().debug(message)


def log_info(message: str):
    """记录信息"""
    get_logger().info(message)


def log_warning(message: str):
    """记录警告"""
    get_logger().warning(message)


def log_error(message: str):
    """记录错误"""
    get_logger().error(message)


def log_query(sql: str, execution_time: float, success: bool, error: Optional[str] = None):
    """记录查询日志"""
    get_logger().query_log(sql, execution_time, success, error)


def log_connection(action: str, connection_name: str, success: bool, error: Optional[str] = None):
    """记录连接日志"""
    get_logger().connection_log(action, connection_name, success, error)
