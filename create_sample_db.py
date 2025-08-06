#!/usr/bin/env python3
"""
创建示例数据库脚本

为SQL管理工具创建一个包含示例数据的SQLite数据库。
"""

import sqlite3
import os
from datetime import date, datetime, timedelta
import random

def create_sample_database():
    """创建示例数据库"""
    db_path = "sample_database.db"
    
    # 如果文件已存在，删除它
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("创建示例数据库...")
    
    # 创建部门表
    cursor.execute("""
    CREATE TABLE departments (
        dept_id INTEGER PRIMARY KEY,
        dept_name TEXT NOT NULL,
        location TEXT,
        created_date DATE DEFAULT CURRENT_DATE
    )
    """)
    
    # 创建员工表
    cursor.execute("""
    CREATE TABLE employees (
        emp_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE,
        phone TEXT,
        hire_date DATE,
        salary REAL,
        dept_id INTEGER,
        manager_id INTEGER,
        FOREIGN KEY (dept_id) REFERENCES departments(dept_id),
        FOREIGN KEY (manager_id) REFERENCES employees(emp_id)
    )
    """)
    
    # 创建项目表
    cursor.execute("""
    CREATE TABLE projects (
        project_id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        description TEXT,
        start_date DATE,
        end_date DATE,
        budget REAL,
        status TEXT DEFAULT 'Planning'
    )
    """)
    
    # 创建员工项目关联表
    cursor.execute("""
    CREATE TABLE employee_projects (
        emp_id INTEGER,
        project_id INTEGER,
        role TEXT,
        hours_allocated REAL,
        PRIMARY KEY (emp_id, project_id),
        FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
        FOREIGN KEY (project_id) REFERENCES projects(project_id)
    )
    """)
    
    # 插入部门数据
    departments = [
        (1, 'IT部门', '北京'),
        (2, '销售部门', '上海'),
        (3, '人力资源部', '广州'),
        (4, '财务部门', '深圳'),
        (5, '研发部门', '杭州')
    ]
    
    cursor.executemany("""
    INSERT INTO departments (dept_id, dept_name, location) 
    VALUES (?, ?, ?)
    """, departments)
    
    # 插入员工数据
    employees_data = [
        (1, '张', '伟', 'zhang.wei@company.com', '13800138001', '2020-01-15', 85000, 1, None),
        (2, '李', '娜', 'li.na@company.com', '13800138002', '2020-03-20', 75000, 1, 1),
        (3, '王', '强', 'wang.qiang@company.com', '13800138003', '2021-05-10', 65000, 2, None),
        (4, '刘', '芳', 'liu.fang@company.com', '13800138004', '2021-07-01', 70000, 2, 3),
        (5, '陈', '明', 'chen.ming@company.com', '13800138005', '2019-11-30', 90000, 5, None),
        (6, '周', '丽', 'zhou.li@company.com', '13800138006', '2022-01-20', 60000, 3, None),
        (7, '吴', '涛', 'wu.tao@company.com', '13800138007', '2020-09-15', 72000, 1, 1),
        (8, '赵', '敏', 'zhao.min@company.com', '13800138008', '2021-12-01', 68000, 4, None),
        (9, '孙', '华', 'sun.hua@company.com', '13800138009', '2022-03-10', 55000, 3, 6),
        (10, '郑', '鑫', 'zheng.xin@company.com', '13800138010', '2020-06-25', 78000, 5, 5)
    ]
    
    cursor.executemany("""
    INSERT INTO employees (emp_id, first_name, last_name, email, phone, hire_date, salary, dept_id, manager_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees_data)
    
    # 插入项目数据
    projects_data = [
        (1, '客户管理系统', 'CRM系统开发项目', '2023-01-01', '2023-06-30', 500000, '进行中'),
        (2, '移动APP开发', '企业移动应用开发', '2023-03-01', '2023-09-30', 300000, '进行中'),
        (3, '数据分析平台', '大数据分析平台建设', '2023-02-15', '2023-12-31', 800000, '计划中'),
        (4, '网站重构', '公司官网重新设计', '2022-10-01', '2023-02-28', 150000, '已完成'),
        (5, 'ERP系统升级', '企业资源规划系统升级', '2023-04-01', '2023-10-31', 600000, '进行中')
    ]
    
    cursor.executemany("""
    INSERT INTO projects (project_id, project_name, description, start_date, end_date, budget, status)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, projects_data)
    
    # 插入员工项目关联数据
    employee_projects_data = [
        (1, 1, '项目经理', 40),
        (2, 1, '开发工程师', 35),
        (7, 1, '测试工程师', 30),
        (5, 2, '技术总监', 20),
        (10, 2, '开发工程师', 40),
        (1, 3, '项目经理', 25),
        (5, 3, '架构师', 30),
        (2, 4, '前端开发', 40),
        (7, 4, '测试工程师', 25),
        (1, 5, '项目经理', 20),
        (5, 5, '技术顾问', 15)
    ]
    
    cursor.executemany("""
    INSERT INTO employee_projects (emp_id, project_id, role, hours_allocated)
    VALUES (?, ?, ?, ?)
    """, employee_projects_data)
    
    # 提交事务
    conn.commit()
    
    print(f"示例数据库创建完成: {db_path}")
    print("\\n数据库包含以下表：")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        print(f"  - {table[0]}")
    
    # 显示一些统计信息
    cursor.execute("SELECT COUNT(*) FROM employees")
    emp_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM departments")
    dept_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM projects")
    proj_count = cursor.fetchone()[0]
    
    print(f"\\n数据统计：")
    print(f"  - 部门数量: {dept_count}")
    print(f"  - 员工数量: {emp_count}")
    print(f"  - 项目数量: {proj_count}")
    
    conn.close()
    return db_path

if __name__ == "__main__":
    create_sample_database()
    print("\\n可以使用以下命令启动SQL管理工具:")
    print("python3 simple_sql_manager.py")
    print("\\n然后打开 sample_database.db 文件进行测试！")
