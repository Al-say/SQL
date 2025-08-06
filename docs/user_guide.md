# SQL管理工具使用指南

## 安装和设置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库连接

复制示例配置文件：
```bash
cp config/database.example.yml config/database.yml
```

编辑 `config/database.yml` 文件，添加您的数据库连接信息。

### 3. 运行应用

```bash
python src/main.py
```

## 主要功能

### 连接管理
- 支持多种数据库：MySQL、PostgreSQL、SQLite、SQL Server
- 可以同时管理多个数据库连接
- 连接配置可以保存和加载

### 查询编辑器
- SQL语法高亮
- 行号显示
- 自动补全（基础）
- 查询格式化
- 支持执行选中的SQL或全部SQL

### 结果查看
- 表格形式显示查询结果
- 支持数据导出（CSV、Excel）
- 基本的数据统计信息
- 简单的图表显示

### 数据库浏览
- 查看数据库中的所有表
- 查看表结构
- 快速预览表数据

## 快捷键

- `F5`: 执行当前查询
- `Ctrl+O`: 打开SQL文件
- `Ctrl+S`: 保存查询
- `Ctrl+A`: 全选文本
- `Ctrl+F`: 查找文本（开发中）

## 配置选项

应用支持通过配置文件自定义各种设置，包括：

- 数据库连接参数
- 界面主题和字体
- 编辑器行为
- 日志设置
- 导出选项

详细配置说明请参考 `config/database.example.yml` 文件。

## 故障排除

### 连接问题
1. 检查数据库服务是否运行
2. 验证连接参数（主机、端口、用户名、密码）
3. 确认网络连接
4. 检查防火墙设置

### 依赖问题
如果遇到依赖包安装问题：
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 权限问题
确保应用有权限：
- 读写日志文件
- 访问配置目录
- 连接目标数据库

## 扩展开发

### 添加新的数据库支持
1. 在 `connection_manager.py` 中添加连接字符串构建逻辑
2. 在查询执行器中添加特定的SQL语法支持
3. 更新连接对话框的数据库类型选项

### 自定义UI主题
1. 修改 `main_window.py` 中的样式设置
2. 添加新的配置选项
3. 实现主题切换功能

### 添加新的导出格式
1. 在 `result_viewer.py` 中添加导出方法
2. 更新导出对话框选项
3. 处理格式特定的配置

## 贡献

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

MIT License - 详见 LICENSE 文件。
