"""
配置管理模块

负责加载和管理应用配置。
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger


class Config:
    """配置类"""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.data = config_data
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        data = self.data
        
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value


def load_config(config_file: Optional[str] = None) -> Config:
    """加载配置文件
    
    Args:
        config_file: 配置文件路径，如果为None则使用默认配置
    
    Returns:
        Config: 配置对象
    """
    # 默认配置
    default_config = {
        'database': {
            'max_connections': 10,
            'connection_timeout': 30,
            'query_timeout': 300
        },
        'ui': {
            'theme': 'default',
            'font_size': 11,
            'auto_save': True,
            'recent_files_limit': 10
        },
        'editor': {
            'syntax_highlighting': True,
            'auto_complete': True,
            'line_numbers': True,
            'word_wrap': False
        },
        'export': {
            'default_format': 'csv',
            'include_headers': True,
            'encoding': 'utf-8'
        },
        'logging': {
            'level': 'INFO',
            'file': 'sql_manager.log',
            'max_size': '10MB',
            'backup_count': 5
        }
    }
    
    if config_file and os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f)
            
            # 合并配置
            merged_config = merge_dict(default_config, file_config)
            logger.info(f"已加载配置文件: {config_file}")
            
        except Exception as e:
            logger.error(f"加载配置文件失败 {config_file}: {e}")
            merged_config = default_config
    else:
        merged_config = default_config
        logger.info("使用默认配置")
    
    return Config(merged_config)


def merge_dict(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """合并两个字典"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dict(result[key], value)
        else:
            result[key] = value
    
    return result


def save_config(config: Config, config_file: str):
    """保存配置到文件
    
    Args:
        config: 配置对象
        config_file: 配置文件路径
    """
    try:
        # 确保目录存在
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(config.data, f, default_flow_style=False, 
                     allow_unicode=True, indent=2)
        
        logger.info(f"配置已保存到: {config_file}")
        
    except Exception as e:
        logger.error(f"保存配置文件失败 {config_file}: {e}")


def get_config_dir() -> str:
    """获取配置目录路径"""
    home_dir = Path.home()
    config_dir = home_dir / '.sql_manager'
    config_dir.mkdir(exist_ok=True)
    return str(config_dir)


def get_default_config_file() -> str:
    """获取默认配置文件路径"""
    return os.path.join(get_config_dir(), 'config.yml')


def create_sample_config():
    """创建示例配置文件"""
    sample_config = {
        'database': {
            'max_connections': 10,
            'connection_timeout': 30,
            'query_timeout': 300,
            'auto_reconnect': True
        },
        'ui': {
            'theme': 'default',
            'font_family': 'Consolas',
            'font_size': 11,
            'auto_save': True,
            'recent_files_limit': 10,
            'window_size': '1200x800'
        },
        'editor': {
            'syntax_highlighting': True,
            'auto_complete': True,
            'line_numbers': True,
            'word_wrap': False,
            'tab_size': 4,
            'auto_indent': True
        },
        'export': {
            'default_format': 'csv',
            'include_headers': True,
            'encoding': 'utf-8',
            'date_format': '%Y-%m-%d %H:%M:%S'
        },
        'logging': {
            'level': 'INFO',
            'file': 'sql_manager.log',
            'max_size': '10MB',
            'backup_count': 5,
            'console_output': True
        }
    }
    
    config_file = os.path.join(get_config_dir(), 'config.example.yml')
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            yaml.dump(sample_config, f, default_flow_style=False, 
                     allow_unicode=True, indent=2)
        
        print(f"示例配置文件已创建: {config_file}")
        
    except Exception as e:
        print(f"创建示例配置文件失败: {e}")


if __name__ == "__main__":
    # 创建示例配置文件
    create_sample_config()
