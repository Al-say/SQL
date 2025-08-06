"""
数据库连接管理器

负责管理多种数据库的连接，支持MySQL、PostgreSQL、SQLite、SQL Server等。
"""

from typing import Dict, Any, Optional, TYPE_CHECKING
import json
import os
import logging

# 可选依赖导入
try:
    from sqlalchemy import create_engine, Engine
    from sqlalchemy.exc import SQLAlchemyError
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
    # 为了类型检查创建假的类型
    if TYPE_CHECKING:
        from sqlalchemy import Engine

# 使用标准库的logging而不是loguru
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """数据库连接类"""
    
    def __init__(self, name: str, engine, config: Dict[str, Any]):
        self.name = name
        self.engine = engine
        self.config = config
        self.is_connected = True
    
    def test_connection(self) -> bool:
        """测试连接是否有效"""
        if not HAS_SQLALCHEMY:
            return False
            
        try:
            with self.engine.connect() as conn:
                if HAS_SQLALCHEMY:
                    from sqlalchemy import text
                    conn.execute(text("SELECT 1"))
                else:
                    conn.execute("SELECT 1")
            return True
        except Exception:
            self.is_connected = False
            return False
    
    def close(self):
        """关闭连接"""
        if self.engine:
            self.engine.dispose()
            self.is_connected = False


class ConnectionManager:
    """数据库连接管理器"""
    
    def __init__(self):
        self.connections: Dict[str, DatabaseConnection] = {}
        self.active_connection: Optional[str] = None
    
    def add_connection(self, name: str, db_type: str, **kwargs) -> bool:
        """添加数据库连接
        
        Args:
            name: 连接名称
            db_type: 数据库类型 (mysql, postgresql, sqlite, sqlserver)
            **kwargs: 连接参数
        
        Returns:
            bool: 连接是否成功
        """
        if not HAS_SQLALCHEMY:
            logger.error("SQLAlchemy未安装，无法创建数据库连接")
            return False
            
        try:
            connection_string = self._build_connection_string(db_type, **kwargs)
            engine = create_engine(connection_string, echo=False)
            
            # 测试连接
            with engine.connect() as conn:
                from sqlalchemy import text
                conn.execute(text("SELECT 1"))
            
            # 保存连接
            config = {'type': db_type, **kwargs}
            self.connections[name] = DatabaseConnection(name, engine, config)
            
            # 如果是第一个连接，设为活动连接
            if not self.active_connection:
                self.active_connection = name
            
            logger.info(f"成功添加数据库连接: {name}")
            return True
            
        except Exception as e:
            logger.error(f"添加数据库连接失败 {name}: {e}")
            return False
    
    def _build_connection_string(self, db_type: str, **kwargs) -> str:
        """构建数据库连接字符串"""
        if db_type.lower() == 'mysql':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 3306)
            username = kwargs.get('username', 'root')
            password = kwargs.get('password', '')
            database = kwargs.get('database', '')
            return f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
        
        elif db_type.lower() == 'postgresql':
            host = kwargs.get('host', 'localhost')
            port = kwargs.get('port', 5432)
            username = kwargs.get('username', 'postgres')
            password = kwargs.get('password', '')
            database = kwargs.get('database', '')
            return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"
        
        elif db_type.lower() == 'sqlite':
            database = kwargs.get('database', ':memory:')
            return f"sqlite:///{database}"
        
        elif db_type.lower() == 'sqlserver':
            host = kwargs.get('host', 'localhost')
            username = kwargs.get('username', '')
            password = kwargs.get('password', '')
            database = kwargs.get('database', '')
            return f"mssql+pyodbc://{username}:{password}@{host}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
    
    def get_connection(self, name: Optional[str] = None) -> Optional[DatabaseConnection]:
        """获取数据库连接"""
        connection_name = name or self.active_connection
        return self.connections.get(connection_name)
    
    def set_active_connection(self, name: str) -> bool:
        """设置活动连接"""
        if name in self.connections:
            self.active_connection = name
            return True
        return False
    
    def remove_connection(self, name: str) -> bool:
        """移除数据库连接"""
        if name in self.connections:
            self.connections[name].close()
            del self.connections[name]
            
            if self.active_connection == name:
                self.active_connection = next(iter(self.connections), None)
            
            logger.info(f"已移除数据库连接: {name}")
            return True
        return False
    
    def list_connections(self) -> Dict[str, Dict[str, Any]]:
        """列出所有连接"""
        return {
            name: {
                'config': conn.config,
                'is_connected': conn.is_connected,
                'is_active': name == self.active_connection
            }
            for name, conn in self.connections.items()
        }
    
    def close_all_connections(self):
        """关闭所有连接"""
        for connection in self.connections.values():
            connection.close()
        self.connections.clear()
        self.active_connection = None
        logger.info("已关闭所有数据库连接")
    
    def save_connections(self, filepath: str):
        """保存连接配置到文件"""
        try:
            connections_config = {}
            for name, conn in self.connections.items():
                config = conn.config.copy()
                # 不保存密码等敏感信息到文件
                if 'password' in config:
                    config['password'] = '***'
                connections_config[name] = config
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(connections_config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"连接配置已保存到: {filepath}")
        except Exception as e:
            logger.error(f"保存连接配置失败: {e}")
    
    def load_connections(self, filepath: str):
        """从文件加载连接配置"""
        try:
            if not os.path.exists(filepath):
                logger.warning(f"连接配置文件不存在: {filepath}")
                return
            
            with open(filepath, 'r', encoding='utf-8') as f:
                connections_config = json.load(f)
            
            for name, config in connections_config.items():
                # 跳过包含占位符密码的连接
                if config.get('password') == '***':
                    logger.warning(f"跳过连接 {name}: 需要重新输入密码")
                    continue
                
                db_type = config.pop('type')
                self.add_connection(name, db_type, **config)
            
            logger.info(f"从文件加载连接配置: {filepath}")
        except Exception as e:
            logger.error(f"加载连接配置失败: {e}")
