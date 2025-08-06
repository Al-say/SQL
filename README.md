# SQL数据库管理工具

一个功能完整的SQL数据库管理工具，提供数据库连接、查询执行、模式管理和数据可视化功能。

## 🚀 快速开始

### 方式1: 简化版（推荐初学者）
仅使用Python标准库，支持SQLite数据库：
```bash
python3 simple_sql_manager.py
```

### 方式2: 完整版
支持多种数据库类型：
```bash
# 1. 运行安装脚本
./install.sh

# 2. 启动应用
python3 run.py
# 或使用 make 命令
make run
```

## 🎯 功能特性

### 简化版功能
- ✅ SQLite数据库支持
- ✅ SQL查询编辑器
- ✅ 查询结果显示
- ✅ 数据库结构浏览
- ✅ 结果导出（CSV）
- ✅ SQL文件导入

### 完整版功能
- 🔗 多数据库连接支持 (MySQL, PostgreSQL, SQLite, SQL Server)
- 📝 SQL查询编辑器与语法高亮
- 📊 查询结果可视化
- 🗄️ 数据库模式管理
- 📈 性能监控与分析
- 💾 查询历史记录
- 🔒 安全连接管理
- 📁 数据导入导出

## 📁 项目结构

```
sql-manager/
├── simple_sql_manager.py  # 简化版启动文件
├── run.py                 # 完整版启动文件
├── install.sh            # 安装脚本
├── src/                  # 源代码
│   ├── core/            # 核心功能模块
│   ├── database/        # 数据库连接与操作
│   ├── ui/              # 用户界面
│   └── utils/           # 工具函数
├── config/              # 配置文件
├── tests/               # 测试文件
├── docs/                # 文档
└── examples/            # 示例代码
```

## 🛠️ 安装说明

### 系统要求
- Python 3.7+
- tkinter（通常随Python安装）

### 依赖安装

**简化版**：无需额外依赖

**完整版**：
```bash
# 自动安装
./install.sh

# 或手动安装
pip install -r requirements.txt
```

## 📖 使用指南

### 简化版使用
1. 运行 `python3 simple_sql_manager.py`
2. 点击"新建数据库"或"打开数据库"
3. 在SQL编辑器中输入查询
4. 按F5或点击"执行查询"

### 完整版使用
1. 复制配置文件：`cp config/database.example.yml config/database.yml`
2. 编辑配置文件添加数据库连接信息
3. 运行 `python3 run.py`
4. 在界面中管理数据库连接

## 🎨 界面截图

### 主界面
- 左侧：数据库结构树
- 右上：SQL查询编辑器
- 右下：查询结果显示

### 功能菜单
- 文件：新建/打开数据库、导入/导出
- 查询：执行查询、清空编辑器
- 帮助：关于信息

## 🧪 测试

```bash
# 运行测试
make test
# 或
python tests/test_main.py
```

## 📚 技术栈

### 核心技术
- **编程语言**: Python 3.7+
- **GUI框架**: Tkinter
- **数据库**: SQLite (简化版)

### 完整版技术栈
- **数据库驱动**: SQLAlchemy, PyMySQL, psycopg2, sqlite3
- **数据处理**: pandas
- **数据可视化**: matplotlib
- **配置管理**: PyYAML
- **测试框架**: unittest

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/new-feature`
3. 提交更改：`git commit -am 'Add new feature'`
4. 推送分支：`git push origin feature/new-feature`
5. 创建 Pull Request

## 📝 开发计划

- [ ] 添加更多数据库类型支持
- [ ] 实现查询历史功能
- [ ] 添加数据可视化图表
- [ ] 支持SQL语法提示
- [ ] 添加数据库备份功能

## 🐛 故障排除

### 常见问题
1. **启动失败**：确保Python版本≥3.7
2. **依赖错误**：使用简化版或重新安装依赖
3. **数据库连接失败**：检查配置文件和网络连接

### 获取帮助
- 查看 `docs/user_guide.md` 获取详细使用说明
- 提交 Issue 报告问题
- 参考 `examples/` 目录的示例

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

感谢所有贡献者和使用者的支持！
