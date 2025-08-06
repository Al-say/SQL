"""
SQL查询执行器

负责执行SQL查询并返回结果，支持查询历史记录和性能分析。
"""

from typing import List, Dict, Any, Optional, Tuple, TYPE_CHECKING
import time
from datetime import datetime

if TYPE_CHECKING:
    from sqlalchemy import text
    from sqlalchemy.exc import SQLAlchemyError
    import pandas as pd

from .connection_manager import ConnectionManager

# 使用标准日志库替代loguru
import logging
logger = logging.getLogger(__name__)


class QueryResult:
    """查询结果类"""
    
    def __init__(self, success: bool, data: Optional[List[Dict]] = None, 
                 error: Optional[str] = None, execution_time: float = 0.0,
                 affected_rows: int = 0):
        self.success = success
        self.data = data  # 改为List[Dict]而不是pandas DataFrame
        self.error = error
        self.execution_time = execution_time
        self.affected_rows = affected_rows
        self.timestamp = datetime.now()


class QueryHistory:
    """查询历史记录类"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    def add_query(self, sql: str, result: QueryResult, connection_name: str):
        """添加查询记录"""
        record = {
            'timestamp': result.timestamp,
            'sql': sql,
            'connection': connection_name,
            'success': result.success,
            'execution_time': result.execution_time,
            'affected_rows': result.affected_rows,
            'error': result.error
        }
        
        self.history.append(record)
        
        # 保持历史记录数量限制
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_recent_queries(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取最近的查询记录"""
        return self.history[-limit:]
    
    def search_queries(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索查询历史"""
        return [
            record for record in self.history
            if keyword.lower() in record['sql'].lower()
        ]


class QueryExecutor:
    """SQL查询执行器"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
        self.query_history = QueryHistory()
    
    def execute_query(self, sql: str, connection_name: Optional[str] = None) -> QueryResult:
        """执行SQL查询
        
        Args:
            sql: SQL查询语句
            connection_name: 连接名称，如果为None则使用活动连接
        
        Returns:
            QueryResult: 查询结果
        """
        start_time = time.time()
        
        try:
            # 获取数据库连接
            connection = self.connection_manager.get_connection(connection_name)
            if not connection:
                return QueryResult(
                    success=False,
                    error="没有可用的数据库连接"
                )
            
            # 清理SQL语句
            sql = sql.strip()
            if not sql:
                return QueryResult(
                    success=False,
                    error="SQL查询不能为空"
                )
            
            # 执行查询
            with connection.engine.connect() as conn:
                result = conn.execute(text(sql))
                
                # 检查是否是SELECT查询
                if sql.upper().strip().startswith('SELECT'):
                    # 获取查询结果
                    data = pd.DataFrame(result.fetchall(), columns=result.keys())
                    affected_rows = len(data)
                else:
                    # 非SELECT查询
                    data = None
                    affected_rows = result.rowcount if hasattr(result, 'rowcount') else 0
            
            execution_time = time.time() - start_time
            
            # 创建成功结果
            query_result = QueryResult(
                success=True,
                data=data,
                execution_time=execution_time,
                affected_rows=affected_rows
            )
            
            # 记录查询历史
            self.query_history.add_query(sql, query_result, connection.name)
            
            logger.info(f"查询执行成功，耗时: {execution_time:.3f}秒")
            return query_result
            
        except SQLAlchemyError as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            # 创建失败结果
            query_result = QueryResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
            
            # 记录查询历史
            if connection_name or self.connection_manager.active_connection:
                conn_name = connection_name or self.connection_manager.active_connection
                self.query_history.add_query(sql, query_result, conn_name)
            
            logger.error(f"查询执行失败: {error_msg}")
            return query_result
        
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"未知错误: {str(e)}"
            
            query_result = QueryResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
            
            logger.error(f"查询执行异常: {error_msg}")
            return query_result
    
    def execute_batch_queries(self, sql_statements: List[str], 
                            connection_name: Optional[str] = None) -> List[QueryResult]:
        """批量执行SQL查询
        
        Args:
            sql_statements: SQL语句列表
            connection_name: 连接名称
        
        Returns:
            List[QueryResult]: 查询结果列表
        """
        results = []
        
        for i, sql in enumerate(sql_statements):
            logger.info(f"执行第 {i+1}/{len(sql_statements)} 个查询")
            result = self.execute_query(sql, connection_name)
            results.append(result)
            
            # 如果查询失败，根据需要决定是否继续
            if not result.success:
                logger.warning(f"第 {i+1} 个查询执行失败: {result.error}")
        
        return results
    
    def get_table_info(self, table_name: str, 
                      connection_name: Optional[str] = None) -> QueryResult:
        """获取表结构信息
        
        Args:
            table_name: 表名
            connection_name: 连接名称
        
        Returns:
            QueryResult: 表结构信息
        """
        # 根据数据库类型构建不同的查询语句
        connection = self.connection_manager.get_connection(connection_name)
        if not connection:
            return QueryResult(success=False, error="没有可用的数据库连接")
        
        db_type = connection.config.get('type', '').lower()
        
        if db_type == 'mysql':
            sql = f"DESCRIBE `{table_name}`"
        elif db_type == 'postgresql':
            sql = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
            """
        elif db_type == 'sqlite':
            sql = f"PRAGMA table_info(`{table_name}`)"
        elif db_type == 'sqlserver':
            sql = f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = '{table_name}'
            ORDER BY ORDINAL_POSITION
            """
        else:
            return QueryResult(success=False, error=f"不支持的数据库类型: {db_type}")
        
        return self.execute_query(sql, connection_name)
    
    def get_database_tables(self, connection_name: Optional[str] = None) -> QueryResult:
        """获取数据库中的所有表
        
        Args:
            connection_name: 连接名称
        
        Returns:
            QueryResult: 表列表
        """
        connection = self.connection_manager.get_connection(connection_name)
        if not connection:
            return QueryResult(success=False, error="没有可用的数据库连接")
        
        db_type = connection.config.get('type', '').lower()
        
        if db_type == 'mysql':
            sql = "SHOW TABLES"
        elif db_type == 'postgresql':
            sql = """
            SELECT tablename as table_name 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
            """
        elif db_type == 'sqlite':
            sql = """
            SELECT name as table_name 
            FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        elif db_type == 'sqlserver':
            sql = """
            SELECT TABLE_NAME as table_name
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
            """
        else:
            return QueryResult(success=False, error=f"不支持的数据库类型: {db_type}")
        
        return self.execute_query(sql, connection_name)
    
    def get_query_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取查询历史"""
        return self.query_history.get_recent_queries(limit)
    
    def search_query_history(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索查询历史"""
        return self.query_history.search_queries(keyword)
