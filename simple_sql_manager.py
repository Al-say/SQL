#!/usr/bin/env python3
"""
SQL管理工具 - 简化启动版本

提供基本的SQL查询和数据库管理功能，无需复杂依赖。
"""

import sys
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from typing import List, Dict, Any, Optional
import os
from pathlib import Path


class SimpleQueryResult:
    """简单查询结果类"""
    
    def __init__(self, success: bool, data: Optional[List[Dict]] = None, 
                 error: Optional[str] = None, affected_rows: int = 0):
        self.success = success
        self.data = data or []
        self.error = error
        self.affected_rows = affected_rows


class SimpleSQLManager:
    """简化的SQL管理工具"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("SQL管理工具 - 简化版")
        self.root.geometry("1000x700")
        
        self.connection = None
        self.db_path = None
        
        self.setup_ui()
        self.bind_events()
    
    def setup_ui(self):
        """设置用户界面"""
        # 菜单栏
        self.create_menu()
        
        # 工具栏
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(toolbar, text="打开数据库", command=self.open_database).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="新建数据库", command=self.create_database).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="执行查询 (F5)", command=self.execute_query).pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_label = ttk.Label(toolbar, text="未连接数据库")
        self.status_label.pack(side=tk.RIGHT)
        
        # 主面板
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # 左侧 - 数据库结构
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="数据库结构", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        
        # 右侧面板
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=3)
        
        # 查询编辑器
        query_frame = ttk.LabelFrame(right_frame, text="SQL查询编辑器")
        query_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.query_text = tk.Text(query_frame, height=8, font=("Consolas", 11))
        self.query_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 结果显示
        result_frame = ttk.LabelFrame(right_frame, text="查询结果")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # 结果表格
        self.result_tree = ttk.Treeview(result_frame, show='headings')
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        result_scroll_y = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        result_scroll_y.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.result_tree.configure(yscrollcommand=result_scroll_y.set)
        
        result_scroll_x = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL, command=self.result_tree.xview)
        result_scroll_x.pack(fill=tk.X)
        self.result_tree.configure(xscrollcommand=result_scroll_x.set)
        
        # 状态栏
        self.status_bar = ttk.Label(self.root, text="就绪", relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        # 右键菜单
        self.create_context_menus()
    
    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建数据库...", command=self.create_database)
        file_menu.add_command(label="打开数据库...", command=self.open_database)
        file_menu.add_separator()
        file_menu.add_command(label="导入SQL...", command=self.import_sql)
        file_menu.add_command(label="导出结果...", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 查询菜单
        query_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查询", menu=query_menu)
        query_menu.add_command(label="执行查询", command=self.execute_query, accelerator="F5")
        query_menu.add_command(label="清空编辑器", command=self.clear_editor)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self.show_about)
    
    def create_context_menus(self):
        """创建右键菜单"""
        # 表树右键菜单
        self.tree_menu = tk.Menu(self.root, tearoff=0)
        self.tree_menu.add_command(label="查看表数据", command=self.view_table_data)
        self.tree_menu.add_command(label="查看表结构", command=self.view_table_structure)
        self.tree_menu.add_command(label="刷新", command=self.refresh_database_structure)
        
        self.tree.bind("<Button-3>", self.show_tree_menu)
    
    def bind_events(self):
        """绑定事件"""
        self.root.bind("<F5>", lambda e: self.execute_query())
        self.tree.bind("<Double-1>", self.on_tree_double_click)
    
    def create_database(self):
        """创建新数据库"""
        filename = filedialog.asksaveasfilename(
            title="创建SQLite数据库",
            defaultextension=".db",
            filetypes=[("SQLite数据库", "*.db"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                # 创建新的SQLite数据库
                conn = sqlite3.connect(filename)
                conn.close()
                
                # 打开新创建的数据库
                self.open_database_file(filename)
                messagebox.showinfo("成功", f"数据库已创建: {filename}")
                
            except Exception as e:
                messagebox.showerror("错误", f"创建数据库失败: {e}")
    
    def open_database(self):
        """打开数据库"""
        filename = filedialog.askopenfilename(
            title="打开SQLite数据库",
            filetypes=[("SQLite数据库", "*.db *.sqlite *.sqlite3"), ("所有文件", "*.*")]
        )
        
        if filename:
            self.open_database_file(filename)
    
    def open_database_file(self, filename: str):
        """打开数据库文件"""
        try:
            if self.connection:
                self.connection.close()
            
            self.connection = sqlite3.connect(filename)
            self.connection.row_factory = sqlite3.Row  # 使结果可以按列名访问
            self.db_path = filename
            
            self.status_label.config(text=f"已连接: {os.path.basename(filename)}")
            self.status_bar.config(text=f"数据库: {filename}")
            
            self.refresh_database_structure()
            
        except Exception as e:
            messagebox.showerror("错误", f"打开数据库失败: {e}")
    
    def refresh_database_structure(self):
        """刷新数据库结构"""
        if not self.connection:
            return
        
        # 清空树
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # 获取所有表
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = cursor.fetchall()
            
            # 添加表到树中
            for table in tables:
                table_name = table[0]
                self.tree.insert("", "end", text=table_name, values=(table_name, "table"))
            
        except Exception as e:
            messagebox.showerror("错误", f"刷新数据库结构失败: {e}")
    
    def execute_query(self):
        """执行SQL查询"""
        if not self.connection:
            messagebox.showwarning("警告", "请先连接数据库")
            return
        
        sql = self.query_text.get(1.0, tk.END).strip()
        if not sql:
            messagebox.showwarning("警告", "请输入SQL查询")
            return
        
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            
            # 检查是否是SELECT查询
            if sql.upper().strip().startswith('SELECT'):
                results = cursor.fetchall()
                self.display_results(results, cursor.description)
                self.status_bar.config(text=f"查询成功，返回 {len(results)} 行")
            else:
                self.connection.commit()
                affected = cursor.rowcount
                self.clear_results()
                self.status_bar.config(text=f"执行成功，影响 {affected} 行")
                
                # 如果是DDL语句，刷新数据库结构
                if any(sql.upper().strip().startswith(cmd) for cmd in ['CREATE', 'DROP', 'ALTER']):
                    self.refresh_database_structure()
            
        except Exception as e:
            messagebox.showerror("查询错误", str(e))
            self.status_bar.config(text="查询失败")
    
    def display_results(self, results: List, description):
        """显示查询结果"""
        # 清空现有结果
        self.clear_results()
        
        if not results:
            return
        
        # 设置列
        columns = [desc[0] for desc in description]
        self.result_tree['columns'] = columns
        self.result_tree['show'] = 'headings'
        
        # 设置列标题
        for col in columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=100, anchor='w')
        
        # 插入数据
        for row in results:
            self.result_tree.insert('', 'end', values=list(row))
    
    def clear_results(self):
        """清空查询结果"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        self.result_tree['columns'] = ()
    
    def show_tree_menu(self, event):
        """显示表树右键菜单"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.tree_menu.post(event.x_root, event.y_root)
    
    def on_tree_double_click(self, event):
        """表树双击事件"""
        self.view_table_data()
    
    def view_table_data(self):
        """查看表数据"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            table_name = self.tree.item(item, "text")
            sql = f"SELECT * FROM `{table_name}` LIMIT 100"
            self.query_text.delete(1.0, tk.END)
            self.query_text.insert(1.0, sql)
            self.execute_query()
    
    def view_table_structure(self):
        """查看表结构"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            table_name = self.tree.item(item, "text")
            sql = f"PRAGMA table_info(`{table_name}`)"
            self.query_text.delete(1.0, tk.END)
            self.query_text.insert(1.0, sql)
            self.execute_query()
    
    def clear_editor(self):
        """清空编辑器"""
        self.query_text.delete(1.0, tk.END)
    
    def import_sql(self):
        """导入SQL文件"""
        filename = filedialog.askopenfilename(
            title="导入SQL文件",
            filetypes=[("SQL文件", "*.sql"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.query_text.delete(1.0, tk.END)
                self.query_text.insert(1.0, content)
                self.status_bar.config(text=f"已导入: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"导入文件失败: {e}")
    
    def export_results(self):
        """导出查询结果"""
        if not self.result_tree.get_children():
            messagebox.showwarning("警告", "没有可导出的结果")
            return
        
        filename = filedialog.asksaveasfilename(
            title="导出查询结果",
            defaultextension=".csv",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    
                    # 写入标题
                    columns = self.result_tree['columns']
                    writer.writerow(columns)
                    
                    # 写入数据
                    for item in self.result_tree.get_children():
                        values = self.result_tree.item(item, 'values')
                        writer.writerow(values)
                
                messagebox.showinfo("成功", f"结果已导出到: {filename}")
                
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {e}")
    
    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo("关于", 
                           "SQL管理工具 - 简化版\\n\\n"
                           "版本: 1.0.0\\n"
                           "支持SQLite数据库管理\\n\\n"
                           "功能特性:\\n"
                           "• SQLite数据库连接\\n"
                           "• SQL查询执行\\n"
                           "• 表结构浏览\\n"
                           "• 结果导出")
    
    def run(self):
        """运行应用"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """关闭应用"""
        if self.connection:
            self.connection.close()
        self.root.destroy()


def main():
    """主函数"""
    print("启动SQL管理工具...")
    app = SimpleSQLManager()
    app.run()


if __name__ == "__main__":
    main()
