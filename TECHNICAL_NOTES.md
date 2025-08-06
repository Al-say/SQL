# 🔧 技术说明：可选依赖架构

## 📌 关于导入警告

您可能会在IDE中看到一些关于SQLAlchemy、pandas、matplotlib等模块的导入警告，这是**正常现象**。

### 🎯 设计原理

本项目采用**可选依赖架构**：

- **简化版**：仅使用Python标准库，零依赖
- **完整版**：可选安装额外功能包

### ⚠️ 常见警告说明

以下警告是正常的，不影响功能：

```
无法解析导入"sqlalchemy"
无法从源解析导入"pandas" 
无法从源解析导入"matplotlib.pyplot"
无法从源解析导入"yaml"
```

### ✅ 如何消除警告

#### 方法1：安装完整依赖（推荐）
```bash
pip install -r requirements-full.txt
```

#### 方法2：按需安装
```bash
# 数据库功能
pip install SQLAlchemy PyMySQL psycopg2-binary

# 数据分析功能  
pip install pandas matplotlib

# 配置文件支持
pip install PyYAML
```

#### 方法3：使用setup.py
```bash
# 完整功能
pip install -e .[full]

# 或分别安装
pip install -e .[database]  # 数据库支持
pip install -e .[analysis]  # 数据分析支持
```

### 🔍 验证安装

运行测试脚本验证：
```bash
python3 -c "
from src.database.connection_manager import ConnectionManager
from src.core.app import SQLManagerApp
print('✅ 所有模块导入成功')
"
```

### 🚀 功能对比

| 功能 | 简化版 | 完整版 |
|------|--------|--------|
| SQLite支持 | ✅ | ✅ |
| MySQL/PostgreSQL | ❌ | ✅ |
| 数据分析 | ❌ | ✅ |
| 图表显示 | ❌ | ✅ |
| YAML配置 | ❌ | ✅ |

### 📝 开发者说明

代码中的try/except导入模式：

```python
try:
    from sqlalchemy import create_engine
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False
```

这确保了：
1. 有依赖时正常工作
2. 无依赖时优雅降级
3. 明确的错误提示

### 🆘 故障排除

如果仍有问题：

1. **检查Python版本**：`python3 --version` (需要>=3.7)
2. **更新pip**：`pip install --upgrade pip`
3. **虚拟环境**：建议使用venv隔离依赖
4. **查看日志**：运行时会有详细的错误信息

### 💡 最佳实践

- **新手**：直接使用`simple_sql_manager.py`
- **进阶**：安装基础数据库依赖
- **专业**：安装完整功能包
- **开发**：使用虚拟环境 + 完整依赖
