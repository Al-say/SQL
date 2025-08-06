"""
SQL查询编辑器

提供SQL语法高亮、自动完成、多标签页等功能的查询编辑器。
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
from typing import Callable, Optional


class QueryEditor:
    """SQL查询编辑器"""
    
    def __init__(self, parent, execute_callback: Callable):
        self.parent = parent
        self.execute_callback = execute_callback
        
        self.create_widgets()
        self.setup_syntax_highlighting()
        self.bind_events()
    
    def create_widgets(self):
        """创建编辑器组件"""
        # 标题栏
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(header_frame, text="SQL查询编辑器", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # 工具按钮
        ttk.Button(header_frame, text="执行 (F5)", 
                  command=self.execute_callback).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(header_frame, text="清空", 
                  command=self.clear_content).pack(side=tk.RIGHT)
        ttk.Button(header_frame, text="格式化", 
                  command=self.format_sql).pack(side=tk.RIGHT, padx=(0, 5))
        
        # 文本编辑器框架
        editor_frame = ttk.Frame(self.parent)
        editor_frame.pack(fill=tk.BOTH, expand=True)
        
        # 行号显示
        self.line_numbers = tk.Text(editor_frame, width=4, padx=3, takefocus=0,
                                   border=0, state='disabled', wrap='none',
                                   background='#f0f0f0', foreground='#666666')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # 主文本编辑器
        self.text_editor = tk.Text(editor_frame, wrap=tk.NONE, undo=True,
                                  font=("Consolas", 11), tabs='4c')
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(editor_frame, orient=tk.VERTICAL, 
                                   command=self.on_scrollbar)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(self.parent, orient=tk.HORIZONTAL, 
                                   command=self.text_editor.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 配置滚动
        self.text_editor.config(yscrollcommand=self.on_text_scroll,
                               xscrollcommand=h_scrollbar.set)
        v_scrollbar.config(command=self.text_editor.yview)
        
        # 状态栏
        status_frame = ttk.Frame(self.parent)
        status_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.cursor_label = ttk.Label(status_frame, text="行: 1, 列: 1")
        self.cursor_label.pack(side=tk.LEFT)
        
        self.selection_label = ttk.Label(status_frame, text="")
        self.selection_label.pack(side=tk.RIGHT)
    
    def setup_syntax_highlighting(self):
        """设置SQL语法高亮"""
        # 定义语法高亮标签
        self.text_editor.tag_configure("keyword", foreground="#0000FF", font=("Consolas", 11, "bold"))
        self.text_editor.tag_configure("function", foreground="#800080", font=("Consolas", 11, "bold"))
        self.text_editor.tag_configure("string", foreground="#008000")
        self.text_editor.tag_configure("comment", foreground="#808080", font=("Consolas", 11, "italic"))
        self.text_editor.tag_configure("number", foreground="#FF6600")
        
        # SQL关键词
        self.keywords = {
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP',
            'ALTER', 'TABLE', 'INDEX', 'VIEW', 'DATABASE', 'SCHEMA', 'PROCEDURE',
            'FUNCTION', 'TRIGGER', 'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN',
            'LIKE', 'IS', 'NULL', 'DISTINCT', 'ORDER', 'BY', 'GROUP', 'HAVING',
            'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON', 'AS',
            'UNION', 'INTERSECT', 'EXCEPT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END',
            'IF', 'BEGIN', 'COMMIT', 'ROLLBACK', 'GRANT', 'REVOKE', 'PRIMARY',
            'FOREIGN', 'KEY', 'REFERENCES', 'UNIQUE', 'CHECK', 'DEFAULT', 'AUTO_INCREMENT'
        }
        
        # SQL函数
        self.functions = {
            'COUNT', 'SUM', 'AVG', 'MAX', 'MIN', 'LENGTH', 'UPPER', 'LOWER',
            'SUBSTRING', 'CONCAT', 'NOW', 'CURDATE', 'CURTIME', 'DATE_FORMAT',
            'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND'
        }
    
    def bind_events(self):
        """绑定事件"""
        # 文本变化事件
        self.text_editor.bind('<KeyRelease>', self.on_text_change)
        self.text_editor.bind('<Button-1>', self.on_cursor_change)
        self.text_editor.bind('<KeyRelease-Return>', self.update_line_numbers)
        self.text_editor.bind('<KeyRelease-BackSpace>', self.update_line_numbers)
        
        # 滚动同步
        self.text_editor.bind('<MouseWheel>', self.sync_scroll)
        self.line_numbers.bind('<MouseWheel>', self.sync_scroll)
        
        # 快捷键
        self.text_editor.bind('<Control-a>', self.select_all)
        self.text_editor.bind('<Control-f>', self.find_text)
        self.text_editor.bind('<F5>', lambda e: self.execute_callback())
        
        # 初始化
        self.update_line_numbers()
        self.update_cursor_position()
    
    def on_scrollbar(self, *args):
        """滚动条滚动"""
        self.text_editor.yview(*args)
        self.line_numbers.yview(*args)
    
    def on_text_scroll(self, *args):
        """文本滚动"""
        self.line_numbers.yview_moveto(args[0])
        return args
    
    def sync_scroll(self, event):
        """同步滚动"""
        if event.widget == self.text_editor:
            self.line_numbers.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.widget == self.line_numbers:
            self.text_editor.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"
    
    def on_text_change(self, event):
        """文本变化事件"""
        self.highlight_syntax()
        self.update_cursor_position()
        
        # 更新行号（如果行数发生变化）
        if event.keysym in ('Return', 'BackSpace', 'Delete'):
            self.update_line_numbers()
    
    def on_cursor_change(self, event):
        """光标位置变化事件"""
        self.text_editor.after_idle(self.update_cursor_position)
    
    def highlight_syntax(self):
        """语法高亮"""
        content = self.text_editor.get(1.0, tk.END)
        
        # 清除现有标签
        for tag in ['keyword', 'function', 'string', 'comment', 'number']:
            self.text_editor.tag_remove(tag, 1.0, tk.END)
        
        # 高亮关键词
        for keyword in self.keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("keyword", start, end)
        
        # 高亮函数
        for function in self.functions:
            pattern = r'\b' + re.escape(function) + r'\b'
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("function", start, end)
        
        # 高亮字符串
        string_pattern = r"'[^']*'|\"[^\"]*\""
        for match in re.finditer(string_pattern, content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_editor.tag_add("string", start, end)
        
        # 高亮注释
        comment_patterns = [r'--[^\n]*', r'/\*.*?\*/', r'#[^\n]*']
        for pattern in comment_patterns:
            for match in re.finditer(pattern, content, re.DOTALL):
                start = f"1.0+{match.start()}c"
                end = f"1.0+{match.end()}c"
                self.text_editor.tag_add("comment", start, end)
        
        # 高亮数字
        number_pattern = r'\b\d+(\.\d+)?\b'
        for match in re.finditer(number_pattern, content):
            start = f"1.0+{match.start()}c"
            end = f"1.0+{match.end()}c"
            self.text_editor.tag_add("number", start, end)
    
    def update_line_numbers(self, event=None):
        """更新行号"""
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)
        
        line_count = int(self.text_editor.index('end-1c').split('.')[0])
        
        for i in range(1, line_count + 1):
            self.line_numbers.insert(tk.END, f"{i:>3}\n")
        
        self.line_numbers.config(state='disabled')
    
    def update_cursor_position(self):
        """更新光标位置显示"""
        cursor_pos = self.text_editor.index(tk.INSERT)
        line, col = cursor_pos.split('.')
        self.cursor_label.config(text=f"行: {line}, 列: {int(col)+1}")
        
        # 更新选择信息
        try:
            sel_start = self.text_editor.index(tk.SEL_FIRST)
            sel_end = self.text_editor.index(tk.SEL_LAST)
            selected_text = self.text_editor.get(sel_start, sel_end)
            self.selection_label.config(text=f"已选择: {len(selected_text)} 字符")
        except tk.TclError:
            self.selection_label.config(text="")
    
    def get_content(self) -> str:
        """获取编辑器内容"""
        return self.text_editor.get(1.0, tk.END + '-1c')
    
    def set_content(self, content: str):
        """设置编辑器内容"""
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, content)
        self.highlight_syntax()
        self.update_line_numbers()
    
    def get_current_query(self) -> str:
        """获取当前查询（选择的文本或全部文本）"""
        try:
            # 如果有选择的文本，返回选择的内容
            selected = self.text_editor.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected.strip():
                return selected.strip()
        except tk.TclError:
            pass
        
        # 否则返回全部内容
        return self.get_content().strip()
    
    def clear_content(self):
        """清空编辑器内容"""
        if messagebox.askyesno("确认", "确定要清空编辑器内容吗？"):
            self.text_editor.delete(1.0, tk.END)
            self.update_line_numbers()
    
    def select_all(self, event):
        """全选"""
        self.text_editor.tag_add(tk.SEL, 1.0, tk.END)
        return 'break'
    
    def find_text(self, event):
        """查找文本"""
        # TODO: 实现查找对话框
        messagebox.showinfo("提示", "查找功能开发中...")
        return 'break'
    
    def format_sql(self):
        """格式化SQL（简单实现）"""
        content = self.get_content()
        if not content.strip():
            return
        
        # 简单的SQL格式化
        formatted = content.upper()
        
        # 在关键词前后添加换行
        keywords = ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 'UNION']
        for keyword in keywords:
            formatted = formatted.replace(keyword, f'\n{keyword}')
        
        # 清理多余的空行
        lines = [line.strip() for line in formatted.split('\n') if line.strip()]
        formatted = '\n'.join(lines)
        
        self.set_content(formatted)
