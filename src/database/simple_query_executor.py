"""
简化版查询执行器

避免复杂依赖，仅使用Python标准库。
"""

from typing import List, Dict, Any, Optional, Tuple
import time
import sqlite3
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class SimpleQueryResult:
    """简化查询结果类"""
    
    def __init__(self, success: bool, data: Optional[List[Dict]] = None, 
                 error: Optional[str] = None, execution_time: float = 0.0,
                 affected_rows: int = 0):
        self.success = success
        self.data = data or []
        self.error = error
        self.execution_time = execution_time
        self.affected_rows = affected_rows
        self.timestamp = datetime.now()


class SimpleQueryHistory:
    """简化查询历史记录类"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.max_history = 1000
    
    def add_query(self, sql: str, result: SimpleQueryResult, connection_name: str):
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


class SimpleQueryExecutor:
    """简化SQL查询执行器"""
    
    def __init__(self):
        self.query_history = SimpleQueryHistory()
    
    def execute_sqlite_query(self, sql: str, db_path: str) -> SimpleQueryResult:
        """执行SQLite查询"""
        start_time = time.time()
        
        try:
            # 清理SQL语句
            sql = sql.strip()
            if not sql:
                return SimpleQueryResult(
                    success=False,
                    error="SQL查询不能为空"
                )
            
            # 连接数据库
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # 执行查询
            cursor.execute(sql)
            
            # 检查是否是SELECT查询
            if sql.upper().strip().startswith('SELECT'):
                # 获取查询结果
                rows = cursor.fetchall()
                data = [dict(row) for row in rows]
                affected_rows = len(data)
            else:
                # 非SELECT查询
                conn.commit()
                data = []
                affected_rows = cursor.rowcount
            
            conn.close()
            execution_time = time.time() - start_time
            
            # 创建成功结果
            query_result = SimpleQueryResult(
                success=True,
                data=data,
                execution_time=execution_time,
                affected_rows=affected_rows
            )
            
            # 记录查询历史
            self.query_history.add_query(sql, query_result, db_path)
            
            logger.info(f"查询执行成功，耗时: {execution_time:.3f}秒")
            return query_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = str(e)
            
            # 创建失败结果
            query_result = SimpleQueryResult(
                success=False,
                error=error_msg,
                execution_time=execution_time
            )
            
            # 记录查询历史
            self.query_history.add_query(sql, query_result, db_path)
            
            logger.error(f"查询执行失败: {error_msg}")
            return query_result
    
    def get_table_info(self, table_name: str, db_path: str) -> SimpleQueryResult:
        """获取表结构信息"""
        sql = f"PRAGMA table_info(`{table_name}`)"
        return self.execute_sqlite_query(sql, db_path)
    
    def get_database_tables(self, db_path: str) -> SimpleQueryResult:
        """获取数据库中的所有表"""
        sql = """
        SELECT name as table_name 
        FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
        """
        return self.execute_sqlite_query(sql, db_path)
    
    def get_query_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取查询历史"""
        return self.query_history.get_recent_queries(limit)
