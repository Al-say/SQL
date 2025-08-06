"""
查询结果查看器

显示SQL查询结果，支持表格视图、图表视图、导出功能等。
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from typing import Optional
import csv

from ..database.query_executor import QueryResult


class ResultViewer:
    """查询结果查看器"""
    
    def __init__(self, parent):
        self.parent = parent
        self.current_result: Optional[QueryResult] = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """创建组件"""
        # 标题栏
        header_frame = ttk.Frame(self.parent)
        header_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(header_frame, text="查询结果", 
                 font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # 工具按钮
        self.export_btn = ttk.Button(header_frame, text="导出", 
                                    command=self.export_result, state=tk.DISABLED)
        self.export_btn.pack(side=tk.RIGHT, padx=(5, 0))
        
        self.chart_btn = ttk.Button(header_frame, text="图表", 
                                   command=self.show_chart, state=tk.DISABLED)
        self.chart_btn.pack(side=tk.RIGHT)
        
        # 选项卡控件
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 数据表格标签页
        self.create_data_tab()
        
        # 消息标签页
        self.create_message_tab()
        
        # 统计标签页
        self.create_stats_tab()
    
    def create_data_tab(self):
        """创建数据表格标签页"""
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="数据")
        
        # 创建表格
        self.tree = ttk.Treeview(self.data_frame, show='tree headings')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 垂直滚动条
        v_scrollbar = ttk.Scrollbar(self.data_frame, orient=tk.VERTICAL, 
                                   command=self.tree.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        
        # 水平滚动条
        h_scrollbar = ttk.Scrollbar(self.parent, orient=tk.HORIZONTAL, 
                                   command=self.tree.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        
        # 双击事件
        self.tree.bind('<Double-1>', self.on_cell_double_click)
    
    def create_message_tab(self):
        """创建消息标签页"""
        self.message_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.message_frame, text="消息")
        
        self.message_text = tk.Text(self.message_frame, wrap=tk.WORD, 
                                   font=("Consolas", 10))
        self.message_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        msg_scrollbar = ttk.Scrollbar(self.message_frame, orient=tk.VERTICAL,
                                     command=self.message_text.yview)
        msg_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.configure(yscrollcommand=msg_scrollbar.set)
    
    def create_stats_tab(self):
        """创建统计标签页"""
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="统计")
        
        self.stats_text = tk.Text(self.stats_frame, wrap=tk.WORD, 
                                 font=("Consolas", 10))
        self.stats_text.pack(fill=tk.BOTH, expand=True)
        
        # 滚动条
        stats_scrollbar = ttk.Scrollbar(self.stats_frame, orient=tk.VERTICAL,
                                       command=self.stats_text.yview)
        stats_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
    
    def show_result(self, result: QueryResult):
        """显示查询结果"""
        self.current_result = result
        
        # 清空现有内容
        self.clear_all_tabs()
        
        if result.success:
            if result.data is not None and not result.data.empty:
                # 显示数据
                self.show_data(result.data)
                self.show_statistics(result.data)
                self.export_btn.config(state=tk.NORMAL)
                self.chart_btn.config(state=tk.NORMAL)
                
                # 切换到数据标签页
                self.notebook.select(self.data_frame)
            else:
                # 显示执行成功但无数据的消息
                message = f"查询执行成功\\n"
                message += f"影响行数: {result.affected_rows}\\n"
                message += f"执行时间: {result.execution_time:.3f} 秒"
                self.show_message(message, "success")
                
                # 切换到消息标签页
                self.notebook.select(self.message_frame)
        else:
            # 显示错误信息
            self.show_message(f"查询执行失败:\\n{result.error}", "error")
            self.export_btn.config(state=tk.DISABLED)
            self.chart_btn.config(state=tk.DISABLED)
            
            # 切换到消息标签页
            self.notebook.select(self.message_frame)
    
    def show_data(self, data: pd.DataFrame):
        """显示数据表格"""
        # 清空现有数据
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # 设置列
        columns = list(data.columns)
        self.tree['columns'] = columns
        self.tree['show'] = 'headings'
        
        # 设置列标题和宽度
        for col in columns:
            self.tree.heading(col, text=col)
            # 根据内容调整列宽
            max_width = max(
                len(str(col)) * 10,  # 标题宽度
                max(len(str(value)) for value in data[col]) * 8 if len(data) > 0 else 50
            )
            self.tree.column(col, width=min(max_width, 200), anchor='w')
        
        # 插入数据
        for index, row in data.iterrows():
            values = [str(value) if pd.notna(value) else '' for value in row]
            self.tree.insert('', 'end', values=values)
    
    def show_message(self, message: str, msg_type: str = "info"):
        """显示消息"""
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        
        # 根据消息类型设置颜色
        if msg_type == "error":
            self.message_text.config(foreground="red")
        elif msg_type == "success":
            self.message_text.config(foreground="green")
        else:
            self.message_text.config(foreground="black")
        
        self.message_text.insert(tk.END, message)
        self.message_text.config(state=tk.DISABLED)
    
    def show_statistics(self, data: pd.DataFrame):
        """显示统计信息"""
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        
        stats_info = f"数据统计信息\\n{'='*50}\\n\\n"
        stats_info += f"总行数: {len(data)}\\n"
        stats_info += f"总列数: {len(data.columns)}\\n\\n"
        
        stats_info += "列信息:\\n"
        stats_info += f"{'列名':<20} {'类型':<15} {'非空值':<10} {'唯一值':<10}\\n"
        stats_info += f"{'-'*20} {'-'*15} {'-'*10} {'-'*10}\\n"
        
        for col in data.columns:
            col_type = str(data[col].dtype)
            non_null = data[col].count()
            unique_count = data[col].nunique()
            
            stats_info += f"{str(col):<20} {col_type:<15} {non_null:<10} {unique_count:<10}\\n"
        
        # 数值列的描述性统计
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            stats_info += f"\\n数值列统计:\\n"
            try:
                desc_stats = data[numeric_cols].describe()
                stats_info += desc_stats.to_string()
            except Exception as e:
                stats_info += f"生成统计信息时出错: {e}"
        
        self.stats_text.insert(tk.END, stats_info)
        self.stats_text.config(state=tk.DISABLED)
    
    def clear_all_tabs(self):
        """清空所有标签页内容"""
        # 清空数据表格
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree['columns'] = ()
        
        # 清空消息
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        self.message_text.config(state=tk.DISABLED)
        
        # 清空统计
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.config(state=tk.DISABLED)
    
    def on_cell_double_click(self, event):
        """单元格双击事件"""
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        
        if column:
            col_index = int(column.replace('#', '')) - 1
            if col_index >= 0:
                values = self.tree.item(item, 'values')
                if col_index < len(values):
                    cell_value = values[col_index]
                    self.show_cell_detail(cell_value)
    
    def show_cell_detail(self, value):
        """显示单元格详细内容"""
        detail_window = tk.Toplevel(self.parent)
        detail_window.title("单元格内容")
        detail_window.geometry("400x300")
        
        text_widget = tk.Text(detail_window, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(detail_window, orient=tk.VERTICAL, command=text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.configure(yscrollcommand=scrollbar.set)
        
        text_widget.insert(tk.END, str(value))
        text_widget.config(state=tk.DISABLED)
    
    def export_result(self):
        """导出查询结果"""
        if not self.current_result or not self.current_result.success or self.current_result.data is None:
            messagebox.showwarning("警告", "没有可导出的数据")
            return
        
        # 选择导出格式
        export_format = messagebox.askyesnocancel("选择格式", 
                                                 "选择导出格式:\\n是: CSV\\n否: Excel\\n取消: 取消操作")
        
        if export_format is None:  # 取消
            return
        
        # 选择文件保存位置
        if export_format:  # CSV
            filename = filedialog.asksaveasfilename(
                title="导出为CSV",
                defaultextension=".csv",
                filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    self.current_result.data.to_csv(filename, index=False, encoding='utf-8-sig')
                    messagebox.showinfo("成功", f"数据已导出到: {filename}")
                except Exception as e:
                    messagebox.showerror("错误", f"导出失败: {e}")
        else:  # Excel
            filename = filedialog.asksaveasfilename(
                title="导出为Excel",
                defaultextension=".xlsx",
                filetypes=[("Excel文件", "*.xlsx"), ("所有文件", "*.*")]
            )
            if filename:
                try:
                    self.current_result.data.to_excel(filename, index=False)
                    messagebox.showinfo("成功", f"数据已导出到: {filename}")
                except Exception as e:
                    messagebox.showerror("错误", f"导出失败: {e}")
    
    def show_chart(self):
        """显示图表"""
        if not self.current_result or not self.current_result.success or self.current_result.data is None:
            messagebox.showwarning("警告", "没有可用的数据")
            return
        
        try:
            # 简单的图表显示功能
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            # 创建图表窗口
            chart_window = tk.Toplevel(self.parent)
            chart_window.title("数据图表")
            chart_window.geometry("800x600")
            
            # 获取数值列
            numeric_cols = self.current_result.data.select_dtypes(include=['number']).columns
            
            if len(numeric_cols) == 0:
                messagebox.showinfo("提示", "没有数值列可以绘制图表")
                chart_window.destroy()
                return
            
            # 创建图表
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if len(numeric_cols) == 1:
                # 单个数值列 - 直方图
                self.current_result.data[numeric_cols[0]].hist(ax=ax, bins=20)
                ax.set_title(f'{numeric_cols[0]} 分布')
                ax.set_xlabel(numeric_cols[0])
                ax.set_ylabel('频次')
            else:
                # 多个数值列 - 折线图
                for col in numeric_cols[:5]:  # 最多显示5列
                    ax.plot(self.current_result.data.index, self.current_result.data[col], 
                           label=col, marker='o', markersize=3)
                ax.set_title('数值列趋势')
                ax.set_xlabel('索引')
                ax.set_ylabel('值')
                ax.legend()
            
            # 嵌入图表到Tkinter窗口
            canvas = FigureCanvasTkAgg(fig, chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except ImportError:
            messagebox.showerror("错误", "需要安装matplotlib库才能显示图表")
        except Exception as e:
            messagebox.showerror("错误", f"生成图表失败: {e}")
