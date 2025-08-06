# 🚀 SQL数据库管理工具 - 安装指南

本工具提供两个版本和多种安装方式，您可以根据需求选择：

## 📦 版本说明

### 🔰 简化版 (推荐新手)
- **文件**: `simple_sql_manager.py`
- **依赖**: 仅Python标准库
- **支持**: SQLite数据库
- **优点**: 零配置，开箱即用

### 🚀 完整版 (推荐专业用户)
- **文件**: `run.py` + `src/` 目录
- **依赖**: 可选依赖包
- **支持**: MySQL, PostgreSQL, SQLite, SQL Server
- **优点**: 功能完整，扩展性强

## 🛠️ 安装方式

### 方式1: 简化版（最简单）

```bash
# 1. 克隆项目
git clone https://github.com/Al-say/SQL.git
cd SQL

# 2. 直接运行（无需安装依赖）
python3 simple_sql_manager.py
```

### 方式2: 完整版基础安装

```bash
# 1. 克隆项目
git clone https://github.com/Al-say/SQL.git
cd SQL

# 2. 安装基础数据库依赖
pip install SQLAlchemy

# 3. 选择性安装数据库驱动
pip install PyMySQL          # MySQL支持
pip install psycopg2-binary  # PostgreSQL支持  
pip install pyodbc           # SQL Server支持

# 4. 运行
python3 run.py
```

### 方式3: 使用setup.py安装

```bash
# 1. 克隆项目
git clone https://github.com/Al-say/SQL.git
cd SQL

# 2. 选择安装模式

# 基础安装（仅标准库）
pip install -e .

# 数据库功能
pip install -e .[database]

# 数据分析功能  
pip install -e .[analysis]

# 完整功能
pip install -e .[full]

# 开发依赖
pip install -e .[dev]

# 3. 运行
python3 run.py
```

### 方式4: 使用requirements文件

```bash
# 1. 克隆项目
git clone https://github.com/Al-say/SQL.git
cd SQL

# 2. 安装完整依赖
pip install -r requirements-full.txt

# 3. 运行
python3 run.py
```

## 🎯 推荐安装路径

### 新手用户
```bash
git clone https://github.com/Al-say/SQL.git
cd SQL
python3 simple_sql_manager.py
```

### 专业用户
```bash
git clone https://github.com/Al-say/SQL.git
cd SQL
pip install -e .[database]
python3 run.py
```

### 开发者
```bash
git clone https://github.com/Al-say/SQL.git
cd SQL
pip install -e .[full,dev]
python3 run.py
```

## 🔧 故障排除

### 常见问题

1. **ImportError: No module named 'tkinter'**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install python3-tk
   
   # CentOS/RHEL
   sudo yum install tkinter
   
   # macOS (使用Homebrew)
   brew install python-tk
   ```

2. **SQLAlchemy导入警告**
   - 这是正常的，表示您使用的是简化版
   - 要使用完整功能，请安装SQLAlchemy：`pip install SQLAlchemy`

3. **数据库连接失败**
   - 检查数据库服务是否运行
   - 确认连接参数正确
   - 安装对应的数据库驱动

## 📝 验证安装

### 验证简化版
```bash
python3 simple_sql_manager.py
# 应该打开GUI界面
```

### 验证完整版
```bash
python3 -c "import src.database.connection_manager; print('安装成功')"
python3 run.py
# 应该打开GUI界面
```

## 🆘 获取帮助

如果遇到问题，请：
1. 检查Python版本：`python3 --version` (需要>=3.7)
2. 查看错误日志
3. 在GitHub上提交Issue: https://github.com/Al-say/SQL/issues

## 🔄 更新

```bash
cd SQL
git pull origin master
# 如果有新依赖，重新安装
pip install -e .[full] --upgrade
```
