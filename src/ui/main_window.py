"""
主窗口界面

SQL管理工具的主要用户界面，提供查询编辑器、结果显示、连接管理等功能。
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any, TYPE_CHECKING

# 可选依赖导入
if TYPE_CHECKING:
    import pandas as pd

from ..database.connection_manager import ConnectionManager
from ..database.query_executor import QueryExecutor
from ..utils.config import Config
from .connection_dialog import ConnectionDialog
from .query_editor import QueryEditor
from .result_viewer import ResultViewer


class MainWindow:
    """主窗口类"""
    
    def __init__(self, connection_manager: ConnectionManager, 
                 query_executor: QueryExecutor, config: Config):
        self.connection_manager = connection_manager
        self.query_executor = query_executor
        self.config = config
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("SQL数据库管理工具")
        self.root.geometry("1200x800")
        
        # 设置窗口图标（如果有的话）
        try:
            # self.root.iconbitmap("icon.ico")
            pass
        except:
            pass
        
        self.setup_ui()
        self.setup_menu()
        
        # 加载保存的连接
        self.load_saved_connections()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建工具栏
        self.create_toolbar(main_frame)
        
        # 创建分隔面板
        paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # 左侧面板 - 数据库浏览器
        left_frame = ttk.Frame(paned_window)
        paned_window.add(left_frame, weight=1)
        self.create_database_browser(left_frame)
        
        # 右侧面板
        right_frame = ttk.Frame(paned_window)
        paned_window.add(right_frame, weight=3)
        
        # 右侧垂直分隔面板
        right_paned = ttk.PanedWindow(right_frame, orient=tk.VERTICAL)
        right_paned.pack(fill=tk.BOTH, expand=True)
        
        # 查询编辑器
        editor_frame = ttk.Frame(right_paned)
        right_paned.add(editor_frame, weight=1)
        self.query_editor = QueryEditor(editor_frame, self.execute_query)
        
        # 结果查看器
        result_frame = ttk.Frame(right_paned)
        right_paned.add(result_frame, weight=1)
        self.result_viewer = ResultViewer(result_frame)
        
        # 状态栏
        self.create_status_bar()
    
    def create_toolbar(self, parent):
        """创建工具栏"""
        toolbar = ttk.Frame(parent)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # 连接管理按钮
        ttk.Button(toolbar, text="新建连接", 
                  command=self.new_connection).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="管理连接", 
                  command=self.manage_connections).pack(side=tk.LEFT, padx=(0, 5))
        
        # 分隔符
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 查询按钮
        ttk.Button(toolbar, text="执行查询 (F5)", 
                  command=self.execute_query).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="停止查询", 
                  command=self.stop_query).pack(side=tk.LEFT, padx=(0, 5))
        
        # 分隔符
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        # 文件操作按钮
        ttk.Button(toolbar, text="打开SQL文件", 
                  command=self.open_sql_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="保存查询", 
                  command=self.save_query).pack(side=tk.LEFT, padx=(0, 5))
        
        # 连接选择下拉框
        ttk.Label(toolbar, text="活动连接:").pack(side=tk.RIGHT, padx=(5, 0))
        self.connection_var = tk.StringVar()
        self.connection_combo = ttk.Combobox(toolbar, textvariable=self.connection_var,
                                           state="readonly", width=20)
        self.connection_combo.pack(side=tk.RIGHT, padx=(5, 0))
        self.connection_combo.bind("<<ComboboxSelected>>", self.on_connection_changed)
    
    def create_database_browser(self, parent):
        """创建数据库浏览器"""
        # 标题
        ttk.Label(parent, text="数据库浏览器", font=("Arial", 12, "bold")).pack(pady=(0, 5))
        
        # 树形视图
        self.db_tree = ttk.Treeview(parent)
        self.db_tree.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.db_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.db_tree.configure(yscrollcommand=scrollbar.set)
        
        # 右键菜单
        self.create_tree_context_menu()
        
        # 双击事件
        self.db_tree.bind("<Double-1>", self.on_tree_double_click)
    
    def create_tree_context_menu(self):
        """创建树形视图右键菜单"""
        self.tree_menu = tk.Menu(self.root, tearoff=0)
        self.tree_menu.add_command(label="刷新", command=self.refresh_database_tree)
        self.tree_menu.add_command(label="查看表结构", command=self.view_table_structure)
        self.tree_menu.add_command(label="查看表数据", command=self.view_table_data)
        
        self.db_tree.bind("<Button-3>", self.show_tree_context_menu)
    
    def create_status_bar(self):
        """创建状态栏"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.status_bar, text="就绪")
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # 执行时间标签
        self.time_label = ttk.Label(self.status_bar, text="")
        self.time_label.pack(side=tk.RIGHT, padx=5)
    
    def setup_menu(self):
        """设置菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="打开SQL文件...", command=self.open_sql_file)
        file_menu.add_command(label="保存查询...", command=self.save_query)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        
        # 连接菜单
        connection_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="连接", menu=connection_menu)
        connection_menu.add_command(label="新建连接...", command=self.new_connection)
        connection_menu.add_command(label="管理连接...", command=self.manage_connections)
        connection_menu.add_separator()
        connection_menu.add_command(label="刷新数据库", command=self.refresh_database_tree)
        
        # 查询菜单
        query_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="查询", menu=query_menu)
        query_menu.add_command(label="执行查询", command=self.execute_query, accelerator="F5")
        query_menu.add_command(label="停止查询", command=self.stop_query)
        query_menu.add_separator()
        query_menu.add_command(label="查询历史...", command=self.show_query_history)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于...", command=self.show_about)
        
        # 绑定快捷键
        self.root.bind("<F5>", lambda e: self.execute_query())
        self.root.bind("<Control-o>", lambda e: self.open_sql_file())
        self.root.bind("<Control-s>", lambda e: self.save_query())
    
    def new_connection(self):
        """新建数据库连接"""
        dialog = ConnectionDialog(self.root, self.connection_manager)
        if dialog.result:
            self.update_connection_list()
            self.refresh_database_tree()
    
    def manage_connections(self):
        """管理数据库连接"""
        # TODO: 实现连接管理对话框
        messagebox.showinfo("提示", "连接管理功能开发中...")
    
    def execute_query(self):
        """执行SQL查询"""
        sql = self.query_editor.get_current_query()
        if not sql.strip():
            messagebox.showwarning("警告", "请输入SQL查询语句")
            return
        
        # 更新状态
        self.status_label.config(text="正在执行查询...")
        self.root.update()
        
        # 执行查询
        result = self.query_executor.execute_query(sql)
        
        # 显示结果
        self.result_viewer.show_result(result)
        
        # 更新状态
        if result.success:
            self.status_label.config(text=f"查询执行成功，影响行数: {result.affected_rows}")
            self.time_label.config(text=f"执行时间: {result.execution_time:.3f}秒")
        else:
            self.status_label.config(text="查询执行失败")
            self.time_label.config(text="")
    
    def stop_query(self):
        """停止查询"""
        # TODO: 实现查询停止功能
        messagebox.showinfo("提示", "停止查询功能开发中...")
    
    def open_sql_file(self):
        """打开SQL文件"""
        filename = filedialog.askopenfilename(
            title="打开SQL文件",
            filetypes=[("SQL文件", "*.sql"), ("所有文件", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.query_editor.set_content(content)
                self.status_label.config(text=f"已打开文件: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"打开文件失败: {e}")
    
    def save_query(self):
        """保存查询"""
        content = self.query_editor.get_content()
        if not content.strip():
            messagebox.showwarning("警告", "没有可保存的内容")
            return
        
        filename = filedialog.asksaveasfilename(
            title="保存SQL文件",
            defaultextension=".sql",
            filetypes=[("SQL文件", "*.sql"), ("所有文件", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_label.config(text=f"已保存文件: {filename}")
            except Exception as e:
                messagebox.showerror("错误", f"保存文件失败: {e}")
    
    def update_connection_list(self):
        """更新连接列表"""
        connections = list(self.connection_manager.connections.keys())
        self.connection_combo['values'] = connections
        if connections and not self.connection_var.get():
            self.connection_var.set(connections[0])
    
    def on_connection_changed(self, event):
        """连接改变事件"""
        connection_name = self.connection_var.get()
        if connection_name:
            self.connection_manager.set_active_connection(connection_name)
            self.refresh_database_tree()
    
    def refresh_database_tree(self):
        """刷新数据库树"""
        # 清空现有内容
        for item in self.db_tree.get_children():
            self.db_tree.delete(item)
        
        # 获取当前连接
        connection = self.connection_manager.get_connection()
        if not connection:
            return
        
        # 获取表列表
        result = self.query_executor.get_database_tables()
        if result.success and result.data is not None:
            # 添加数据库节点
            db_node = self.db_tree.insert("", "end", text=connection.name, 
                                         values=("database",), open=True)
            
            # 添加表节点
            for _, row in result.data.iterrows():
                table_name = row.iloc[0]  # 第一列是表名
                self.db_tree.insert(db_node, "end", text=table_name, 
                                   values=("table", table_name))
    
    def on_tree_double_click(self, event):
        """树形视图双击事件"""
        item = self.db_tree.selection()[0]
        values = self.db_tree.item(item, "values")
        
        if len(values) >= 2 and values[0] == "table":
            table_name = values[1]
            self.view_table_data_preview(table_name)
    
    def show_tree_context_menu(self, event):
        """显示树形视图右键菜单"""
        item = self.db_tree.identify_row(event.y)
        if item:
            self.db_tree.selection_set(item)
            self.tree_menu.post(event.x_root, event.y_root)
    
    def view_table_structure(self):
        """查看表结构"""
        selection = self.db_tree.selection()
        if selection:
            item = selection[0]
            values = self.db_tree.item(item, "values")
            if len(values) >= 2 and values[0] == "table":
                table_name = values[1]
                result = self.query_executor.get_table_info(table_name)
                self.result_viewer.show_result(result)
    
    def view_table_data(self):
        """查看表数据"""
        selection = self.db_tree.selection()
        if selection:
            item = selection[0]
            values = self.db_tree.item(item, "values")
            if len(values) >= 2 and values[0] == "table":
                table_name = values[1]
                sql = f"SELECT * FROM `{table_name}` LIMIT 1000"
                self.query_editor.set_content(sql)
                self.execute_query()
    
    def view_table_data_preview(self, table_name: str):
        """预览表数据"""
        sql = f"SELECT * FROM `{table_name}` LIMIT 100"
        result = self.query_executor.execute_query(sql)
        self.result_viewer.show_result(result)
    
    def show_query_history(self):
        """显示查询历史"""
        # TODO: 实现查询历史对话框
        messagebox.showinfo("提示", "查询历史功能开发中...")
    
    def show_about(self):
        """显示关于对话框"""
        messagebox.showinfo("关于", 
                           "SQL数据库管理工具 v1.0\n\n"
                           "一个功能完整的数据库管理工具\n"
                           "支持MySQL、PostgreSQL、SQLite、SQL Server")
    
    def load_saved_connections(self):
        """加载保存的连接"""
        try:
            config_file = "connections.json"
            self.connection_manager.load_connections(config_file)
            self.update_connection_list()
            self.refresh_database_tree()
        except Exception as e:
            print(f"加载连接配置失败: {e}")
    
    def save_connections_on_exit(self):
        """退出时保存连接"""
        try:
            config_file = "connections.json"
            self.connection_manager.save_connections(config_file)
        except Exception as e:
            print(f"保存连接配置失败: {e}")
    
    def run(self):
        """运行主窗口"""
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 启动GUI事件循环
        self.root.mainloop()
    
    def on_closing(self):
        """窗口关闭事件"""
        self.save_connections_on_exit()
        self.root.destroy()
    
    def close(self):
        """关闭窗口"""
        if self.root:
            self.root.destroy()
