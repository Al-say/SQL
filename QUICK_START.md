# 🚀 SQL管理工具 - 快速启动指南

## 立即开始（30秒体验）

### 1️⃣ 启动应用
```bash
python3 simple_sql_manager.py
```

### 2️⃣ 打开示例数据库
- 点击菜单 "文件" → "打开数据库"
- 选择 `sample_database.db` 文件
- 看到数据库结构出现在左侧面板

### 3️⃣ 执行第一个查询
在SQL编辑器中输入：
```sql
SELECT * FROM employees LIMIT 5;
```
按 `F5` 或点击 "执行查询"

### 4️⃣ 浏览数据库
- 双击左侧的表名查看数据
- 右键点击表名选择"查看表结构"

## 🎯 常用查询示例

### 基础查询
```sql
-- 查看所有员工
SELECT * FROM employees;

-- 查看部门信息
SELECT * FROM departments;
```

### 进阶查询
```sql
-- 员工薪资统计
SELECT 
    dept_name,
    COUNT(*) as 员工数量,
    ROUND(AVG(salary), 2) as 平均薪资,
    MAX(salary) as 最高薪资
FROM employees e
JOIN departments d ON e.dept_id = d.dept_id
GROUP BY dept_name
ORDER BY 平均薪资 DESC;
```

### 复杂查询
```sql
-- 项目参与情况
SELECT 
    p.project_name as 项目名称,
    e.first_name || ' ' || e.last_name as 员工姓名,
    ep.role as 角色,
    ep.hours_allocated as 分配工时,
    d.dept_name as 部门
FROM employee_projects ep
JOIN employees e ON ep.emp_id = e.emp_id
JOIN projects p ON ep.project_id = p.project_id
JOIN departments d ON e.dept_id = d.dept_id
ORDER BY p.project_name, ep.hours_allocated DESC;
```

## 🛠️ 功能快捷键

| 功能 | 快捷键 | 说明 |
|------|--------|------|
| 执行查询 | `F5` | 执行当前SQL查询 |
| 新建数据库 | - | 菜单：文件 → 新建数据库 |
| 打开数据库 | - | 菜单：文件 → 打开数据库 |
| 导出结果 | - | 菜单：文件 → 导出结果 |
| 查看表数据 | 双击表名 | 在左侧数据库结构树中 |
| 查看表结构 | 右键表名 | 选择"查看表结构" |

## 💡 使用技巧

### 查询技巧
1. **选择性执行**: 选中部分SQL代码，按F5只执行选中部分
2. **结果导出**: 查询完成后，菜单选择"导出结果"保存为CSV
3. **SQL格式化**: 保持查询语句整洁，便于阅读和维护

### 数据浏览
1. **快速预览**: 双击表名自动生成SELECT查询
2. **表结构**: 右键表名查看列信息和数据类型
3. **数据筛选**: 使用WHERE子句筛选特定数据

### 数据管理
1. **备份数据**: 定期导出重要数据
2. **版本控制**: 保存重要的SQL查询到.sql文件
3. **数据验证**: 使用聚合函数验证数据完整性

## 🎓 学习路径

### 初学者
1. 先熟悉基本的SELECT查询
2. 学习WHERE条件筛选
3. 掌握ORDER BY排序
4. 了解聚合函数(COUNT, SUM, AVG等)

### 进阶用户
1. 学习表连接(JOIN)
2. 掌握子查询
3. 了解窗口函数
4. 学习数据修改(INSERT, UPDATE, DELETE)

### 高级用户
1. 优化查询性能
2. 设计数据库模式
3. 学习事务管理
4. 掌握索引使用

## 🆘 故障排除

### 常见问题
**Q: 启动失败显示模块未找到**
A: 确保使用Python 3.7+: `python3 --version`

**Q: 无法打开数据库文件**
A: 检查文件权限，确保有读写权限

**Q: 查询执行缓慢**
A: 大量数据时使用LIMIT限制结果数量

**Q: 中文显示乱码**
A: 确保数据库文件使用UTF-8编码

### 获取帮助
- 查看项目文档：`docs/user_guide.md`
- 参考示例查询：`examples/sample_queries.sql`
- 项目总结：`PROJECT_SUMMARY.md`

---

**🎉 现在开始探索您的数据库吧！**
