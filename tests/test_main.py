"""
SQL管理工具测试套件

基本的单元测试和集成测试。
"""

import unittest
import sys
import os
from pathlib import Path

# 添加源代码路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.database.connection_manager import ConnectionManager
from src.database.query_executor import QueryExecutor, QueryResult
from src.utils.config import Config


class TestConnectionManager(unittest.TestCase):
    """连接管理器测试"""
    
    def setUp(self):
        """测试前设置"""
        self.manager = ConnectionManager()
    
    def tearDown(self):
        """测试后清理"""
        self.manager.close_all_connections()
    
    def test_sqlite_connection(self):
        """测试SQLite连接"""
        success = self.manager.add_connection(
            "test_sqlite", 
            "sqlite", 
            database=":memory:"
        )
        self.assertTrue(success)
        self.assertIn("test_sqlite", self.manager.connections)
    
    def test_connection_list(self):
        """测试连接列表"""
        self.manager.add_connection("test1", "sqlite", database=":memory:")
        self.manager.add_connection("test2", "sqlite", database=":memory:")
        
        connections = self.manager.list_connections()
        self.assertEqual(len(connections), 2)
        self.assertIn("test1", connections)
        self.assertIn("test2", connections)
    
    def test_active_connection(self):
        """测试活动连接"""
        self.manager.add_connection("test", "sqlite", database=":memory:")
        self.assertEqual(self.manager.active_connection, "test")
        
        self.manager.add_connection("test2", "sqlite", database=":memory:")
        self.manager.set_active_connection("test2")
        self.assertEqual(self.manager.active_connection, "test2")


class TestQueryExecutor(unittest.TestCase):
    """查询执行器测试"""
    
    def setUp(self):
        """测试前设置"""
        self.manager = ConnectionManager()
        self.manager.add_connection("test", "sqlite", database=":memory:")
        self.executor = QueryExecutor(self.manager)
    
    def tearDown(self):
        """测试后清理"""
        self.manager.close_all_connections()
    
    def test_create_table(self):
        """测试创建表"""
        sql = """
        CREATE TABLE test_table (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
        """
        result = self.executor.execute_query(sql)
        self.assertTrue(result.success)
    
    def test_insert_data(self):
        """测试插入数据"""
        # 先创建表
        create_sql = """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT
        )
        """
        self.executor.execute_query(create_sql)
        
        # 插入数据
        insert_sql = "INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')"
        result = self.executor.execute_query(insert_sql)
        self.assertTrue(result.success)
        self.assertEqual(result.affected_rows, 1)
    
    def test_select_data(self):
        """测试查询数据"""
        # 准备数据
        self.executor.execute_query("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                price REAL
            )
        """)
        
        self.executor.execute_query("INSERT INTO products (name, price) VALUES ('Apple', 1.5)")
        self.executor.execute_query("INSERT INTO products (name, price) VALUES ('Banana', 0.8)")
        
        # 查询数据
        result = self.executor.execute_query("SELECT * FROM products")
        self.assertTrue(result.success)
        self.assertIsNotNone(result.data)
        self.assertEqual(len(result.data), 2)
    
    def test_invalid_sql(self):
        """测试无效SQL"""
        result = self.executor.execute_query("INVALID SQL STATEMENT")
        self.assertFalse(result.success)
        self.assertIsNotNone(result.error)
    
    def test_query_history(self):
        """测试查询历史"""
        self.executor.execute_query("SELECT 1")
        self.executor.execute_query("SELECT 2")
        
        history = self.executor.get_query_history(limit=10)
        self.assertEqual(len(history), 2)


class TestConfig(unittest.TestCase):
    """配置测试"""
    
    def test_config_creation(self):
        """测试配置创建"""
        config_data = {
            'database': {'timeout': 30},
            'ui': {'theme': 'dark'}
        }
        config = Config(config_data)
        
        self.assertEqual(config.get('database.timeout'), 30)
        self.assertEqual(config.get('ui.theme'), 'dark')
        self.assertIsNone(config.get('nonexistent.key'))
    
    def test_config_default_values(self):
        """测试配置默认值"""
        config = Config({})
        
        self.assertEqual(config.get('missing.key', 'default'), 'default')
        self.assertEqual(config.get('another.missing', 42), 42)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTest(unittest.makeSuite(TestConnectionManager))
    test_suite.addTest(unittest.makeSuite(TestQueryExecutor))
    test_suite.addTest(unittest.makeSuite(TestConfig))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("运行SQL管理工具测试套件...")
    success = run_tests()
    
    if success:
        print("\\n✅ 所有测试通过！")
        sys.exit(0)
    else:
        print("\\n❌ 有测试失败！")
        sys.exit(1)
