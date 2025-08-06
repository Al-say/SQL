"""
数据库连接配置对话框

用于配置新的数据库连接，支持多种数据库类型。
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any

from ..database.connection_manager import ConnectionManager


class ConnectionDialog:
    """数据库连接配置对话框"""
    
    def __init__(self, parent, connection_manager: ConnectionManager):
        self.parent = parent
        self.connection_manager = connection_manager
        self.result = False
        
        # 创建对话框窗口
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("新建数据库连接")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.center_window()
        
        # 初始化变量
        self.init_variables()
        
        # 创建界面
        self.create_widgets()
        
        # 绑定事件
        self.bind_events()
        
        # 等待对话框关闭
        self.dialog.wait_window()
    
    def center_window(self):
        """居中显示窗口"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"400x500+{x}+{y}")
    
    def init_variables(self):
        """初始化变量"""
        self.name_var = tk.StringVar()
        self.db_type_var = tk.StringVar(value="mysql")
        self.host_var = tk.StringVar(value="localhost")
        self.port_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.database_var = tk.StringVar()
        self.file_var = tk.StringVar()
    
    def create_widgets(self):
        """创建界面组件"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="配置数据库连接", 
                               font=("Arial", 14, "bold"))
        title_label.pack(pady=(0, 20))
        
        # 连接名称
        ttk.Label(main_frame, text="连接名称:").pack(anchor=tk.W)
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).pack(fill=tk.X, pady=(0, 10))
        
        # 数据库类型
        ttk.Label(main_frame, text="数据库类型:").pack(anchor=tk.W)
        db_type_frame = ttk.Frame(main_frame)
        db_type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.db_type_combo = ttk.Combobox(db_type_frame, textvariable=self.db_type_var,
                                         values=["mysql", "postgresql", "sqlite", "sqlserver"],
                                         state="readonly", width=37)
        self.db_type_combo.pack(fill=tk.X)
        
        # 连接参数框架
        self.params_frame = ttk.LabelFrame(main_frame, text="连接参数")
        self.params_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 创建初始参数界面
        self.create_connection_params()
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="测试连接", 
                  command=self.test_connection).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="取消", 
                  command=self.cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="确定", 
                  command=self.ok).pack(side=tk.RIGHT)
    
    def bind_events(self):
        """绑定事件"""
        self.db_type_combo.bind("<<ComboboxSelected>>", self.on_db_type_changed)
        self.dialog.bind("<Return>", lambda e: self.ok())
        self.dialog.bind("<Escape>", lambda e: self.cancel())
    
    def on_db_type_changed(self, event):
        """数据库类型改变事件"""
        self.create_connection_params()
    
    def create_connection_params(self):
        """创建连接参数界面"""
        # 清空现有组件
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        
        db_type = self.db_type_var.get()
        
        if db_type == "sqlite":
            self.create_sqlite_params()
        else:
            self.create_server_params(db_type)
    
    def create_sqlite_params(self):
        """创建SQLite参数界面"""
        ttk.Label(self.params_frame, text="数据库文件:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        
        file_frame = ttk.Frame(self.params_frame)
        file_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Entry(file_frame, textvariable=self.file_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="浏览...", 
                  command=self.browse_file).pack(side=tk.RIGHT, padx=(5, 0))
    
    def create_server_params(self, db_type: str):
        """创建服务器类型数据库参数界面"""
        # 主机地址
        ttk.Label(self.params_frame, text="主机地址:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        ttk.Entry(self.params_frame, textvariable=self.host_var, width=40).pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # 端口号
        ttk.Label(self.params_frame, text="端口号:").pack(anchor=tk.W, padx=10)
        port_entry = ttk.Entry(self.params_frame, textvariable=self.port_var, width=40)
        port_entry.pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # 设置默认端口
        default_ports = {
            "mysql": "3306",
            "postgresql": "5432",
            "sqlserver": "1433"
        }
        self.port_var.set(default_ports.get(db_type, ""))
        
        # 用户名
        ttk.Label(self.params_frame, text="用户名:").pack(anchor=tk.W, padx=10)
        ttk.Entry(self.params_frame, textvariable=self.username_var, width=40).pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # 密码
        ttk.Label(self.params_frame, text="密码:").pack(anchor=tk.W, padx=10)
        ttk.Entry(self.params_frame, textvariable=self.password_var, 
                 show="*", width=40).pack(fill=tk.X, padx=10, pady=(0, 5))
        
        # 数据库名
        ttk.Label(self.params_frame, text="数据库名:").pack(anchor=tk.W, padx=10)
        ttk.Entry(self.params_frame, textvariable=self.database_var, width=40).pack(fill=tk.X, padx=10, pady=(0, 10))
    
    def browse_file(self):
        """浏览SQLite文件"""
        from tkinter import filedialog
        filename = filedialog.askopenfilename(
            title="选择SQLite数据库文件",
            filetypes=[("SQLite数据库", "*.db *.sqlite *.sqlite3"), ("所有文件", "*.*")]
        )
        if filename:
            self.file_var.set(filename)
    
    def get_connection_params(self) -> Dict[str, Any]:
        """获取连接参数"""
        db_type = self.db_type_var.get()
        
        if db_type == "sqlite":
            return {
                "database": self.file_var.get()
            }
        else:
            params = {
                "host": self.host_var.get(),
                "username": self.username_var.get(),
                "password": self.password_var.get(),
                "database": self.database_var.get()
            }
            
            # 添加端口号（如果不为空）
            port = self.port_var.get().strip()
            if port:
                try:
                    params["port"] = int(port)
                except ValueError:
                    raise ValueError("端口号必须是数字")
            
            return params
    
    def validate_input(self) -> bool:
        """验证输入"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("错误", "请输入连接名称")
            return False
        
        if name in self.connection_manager.connections:
            messagebox.showerror("错误", "连接名称已存在")
            return False
        
        db_type = self.db_type_var.get()
        
        if db_type == "sqlite":
            if not self.file_var.get().strip():
                messagebox.showerror("错误", "请选择数据库文件")
                return False
        else:
            if not self.host_var.get().strip():
                messagebox.showerror("错误", "请输入主机地址")
                return False
            
            if not self.username_var.get().strip():
                messagebox.showerror("错误", "请输入用户名")
                return False
        
        return True
    
    def test_connection(self):
        """测试连接"""
        if not self.validate_input():
            return
        
        try:
            name = "测试连接"
            db_type = self.db_type_var.get()
            params = self.get_connection_params()
            
            # 临时创建连接进行测试
            from ..database.connection_manager import ConnectionManager
            temp_manager = ConnectionManager()
            
            if temp_manager.add_connection(name, db_type, **params):
                messagebox.showinfo("成功", "连接测试成功！")
                temp_manager.close_all_connections()
            else:
                messagebox.showerror("错误", "连接测试失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"连接测试失败: {e}")
    
    def ok(self):
        """确定按钮"""
        if not self.validate_input():
            return
        
        try:
            name = self.name_var.get().strip()
            db_type = self.db_type_var.get()
            params = self.get_connection_params()
            
            if self.connection_manager.add_connection(name, db_type, **params):
                self.result = True
                self.dialog.destroy()
            else:
                messagebox.showerror("错误", "添加连接失败")
                
        except Exception as e:
            messagebox.showerror("错误", f"添加连接失败: {e}")
    
    def cancel(self):
        """取消按钮"""
        self.dialog.destroy()
