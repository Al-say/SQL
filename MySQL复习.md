# MySQL数据库补考复习指南

## 一、选择题（40分，20题）

### 1. 基本概念
1. **数据库系统基础**
   - DB：存储在计算机内的相关数据的集合
   - DBMS：管理数据库的软件系统
   - DBS = DB + DBMS + 应用系统
   - 数据独立性：物理独立性和逻辑独立性

2. **三级模式结构**
   - 外模式：用户视图级别
   - 模式：逻辑级别，一个数据库只有一个
   - 内模式：物理存储级别
   - 两级映像：
     - 外模式/模式映像：保证数据逻辑独立性
     - 模式/内模式映像：保证数据物理独立性

3. **数据模型**
   - 层次模型：树形结构，1:n关系
   - 网状模型：网络结构，m:n关系
   - 关系模型：二维表格形式
   - 三要素：数据结构、操作、约束

### 2. 关系数据库理论
1. **关系的基本概念**
   - 关系（表）、元组（行）、属性（列）
   - 码的概念：
     - 超键：唯一标识元组的属性集
     - 候选键：最小超键
     - 主键：唯一标识选定的候选键
     - 外键：引用另一个关系主键的属性

2. **关系代数运算**
   - 集合运算：并、差、交、笛卡尔积
   - 专门运算：选择、投影、连接、除

3. **数据库完整性**
   - 实体完整性：主键非空且唯一
   - 参照完整性：外键值必须存在于主表
   - 用户定义完整性：CHECK、DEFAULT等

## 二、判断题（10分，10题）

### 关键知识点
1. **数据库设计过程**
   - 需求分析 → 概念设计 → 逻辑设计 → 物理设计
   - E-R图属于概念设计阶段
   - 三范式属于逻辑设计阶段

2. **视图的特点**
   - 是虚拟表，不存储实际数据
   - 基于基本表动态生成
   - 简化查询，提高安全性
   - 某些视图可更新（满足特定条件）

3. **事务的特性**
   - 原子性（Atomicity）：要么全执行，要么全不执行
   - 一致性（Consistency）：保持数据一致
   - 隔离性（Isolation）：事务间互不干扰
   - 持久性（Durability）：提交后永久保存

## 三、SQL语句题（25分，5题）

### 1. 条件查询
1. **比较运算符**
```sql
-- 等于、不等于
SELECT * FROM 学生 WHERE 年龄 = 20;
SELECT * FROM 学生 WHERE 系别 != '计算机';

-- 范围查询
SELECT * FROM 学生 WHERE 年龄 BETWEEN 18 AND 22;
SELECT * FROM 成绩 WHERE 分数 >= 60 AND 分数 <= 100;
```

2. **模糊查询**
```sql
-- LIKE用法
SELECT * FROM 学生 WHERE 姓名 LIKE '张%';  -- 姓张
SELECT * FROM 学生 WHERE 姓名 LIKE '_华%'; -- 第二个字是华
SELECT * FROM 课程 WHERE 课程名 LIKE '%数据库%'; -- 包含数据库
```

3. **空值查询**
```sql
-- IS NULL和IS NOT NULL
SELECT * FROM 借阅 WHERE 还书时间 IS NULL;  -- 未还书记录
SELECT * FROM 学生 WHERE 电话 IS NOT NULL;  -- 有电话记录
```

### 2. 修改数据
1. **插入数据**
```sql
-- 单行插入
INSERT INTO 学生(学号, 姓名, 年龄) 
VALUES('001', '张三', 20);

-- 多行插入
INSERT INTO 学生(学号, 姓名, 年龄) 
VALUES ('002', '李四', 19),
       ('003', '王五', 21);

-- 基于查询结果插入
INSERT INTO 优秀学生(学号, 姓名)
SELECT 学号, 姓名 
FROM 学生 
WHERE 平均成绩 >= 90;
```

2. **更新数据**
```sql
-- 单表更新
UPDATE 学生 
SET 年龄 = 年龄 + 1 
WHERE 系别 = '计算机';

-- 多表更新
UPDATE 学生 s
JOIN 成绩 c ON s.学号 = c.学号
SET c.成绩 = c.成绩 * 1.1
WHERE c.成绩 < 60;
```

3. **删除数据**
```sql
-- 条件删除
DELETE FROM 选课 
WHERE 学号 = '001' 
AND 课程号 = 'C001';

-- 截断表（删除全部数据）
TRUNCATE TABLE 临时表;
```

### 3. 视图创建和使用
```sql
-- 简单视图
CREATE VIEW 学生信息视图 AS
SELECT 学号, 姓名, 系别
FROM 学生;

-- 复杂视图
CREATE VIEW 成绩统计视图 AS
SELECT s.系别, 
       COUNT(*) as 学生数,
       AVG(c.成绩) as 平均分
FROM 学生 s
JOIN 选课 c ON s.学号 = c.学号
GROUP BY s.系别;

-- 视图更新
UPDATE 学生信息视图
SET 系别 = '信息'
WHERE 学号 = '001';
```

### 4. 分组统计
1. **基本分组**
```sql
-- 单字段分组
SELECT 系别, COUNT(*) as 人数
FROM 学生
GROUP BY 系别;

-- 多字段分组
SELECT 系别, 年级, COUNT(*) as 人数
FROM 学生
GROUP BY 系别, 年级;
```

2. **分组后过滤**
```sql
-- HAVING子句
SELECT 课程号, 
       AVG(成绩) as 平均分,
       COUNT(*) as 选课人数
FROM 选课
GROUP BY 课程号
HAVING AVG(成绩) < 60
AND COUNT(*) >= 5;
```

3. **聚合函数**
```sql
-- 常用聚合函数
SELECT 系别,
       COUNT(*) as 总人数,
       AVG(年龄) as 平均年龄,
       MAX(成绩) as 最高分,
       MIN(成绩) as 最低分,
       SUM(学分) as 总学分
FROM 学生
GROUP BY 系别;
```

### 5. 多表查询
1. **内连接**
```sql
-- 等值连接
SELECT s.姓名, c.课程名, sc.成绩
FROM 学生 s
JOIN 选课 sc ON s.学号 = sc.学号
JOIN 课程 c ON sc.课程号 = c.课程号;

-- 自然连接
SELECT 学号, 姓名, 课程名, 成绩
FROM 学生 
NATURAL JOIN 选课
NATURAL JOIN 课程;
```

2. **外连接**
```sql
-- 左外连接
SELECT s.姓名, c.课程名
FROM 学生 s
LEFT JOIN 选课 sc ON s.学号 = sc.学号
LEFT JOIN 课程 c ON sc.课程号 = c.课程号;

-- 右外连接
SELECT c.课程名, s.姓名
FROM 选课 sc
RIGHT JOIN 课程 c ON sc.课程号 = c.课程号
LEFT JOIN 学生 s ON sc.学号 = s.学号;
```

## 四、数据库设计题（15分，2题）

### 1. ER图设计要点
1. **实体的表示**
   - 矩形表示实体型
   - 椭圆表示属性
   - 菱形表示关系
   - 下划线表示主键属性

2. **联系的类型**
   - 一对一(1:1): ─┼─
   - 一对多(1:n): ─┼─<
   - 多对多(m:n): >─┼─<

3. **属性的类型**
   - 简单属性 vs 复合属性
   - 单值属性 vs 多值属性
   - 导出属性（虚线表示）

### 2. ER图转换规则
1. **实体转换**
```sql
-- 实体转换为表
CREATE TABLE 学生 (
    学号 CHAR(10) PRIMARY KEY,
    姓名 VARCHAR(20) NOT NULL,
    出生日期 DATE,
    性别 CHAR(1)
);
```

2. **一对一关系**
```sql
-- 外键方式
CREATE TABLE 学生 (
    学号 CHAR(10) PRIMARY KEY,
    姓名 VARCHAR(20)
);

CREATE TABLE 学籍档案 (
    档案号 CHAR(12) PRIMARY KEY,
    学号 CHAR(10) UNIQUE,
    入学日期 DATE,
    FOREIGN KEY (学号) REFERENCES 学生(学号)
);
```

3. **一对多关系**
```sql
-- 在"多"方加入外键
CREATE TABLE 系别 (
    系号 CHAR(6) PRIMARY KEY,
    系名 VARCHAR(40)
);

CREATE TABLE 学生 (
    学号 CHAR(10) PRIMARY KEY,
    姓名 VARCHAR(20),
    系号 CHAR(6),
    FOREIGN KEY (系号) REFERENCES 系别(系号)
);
```

4. **多对多关系**
```sql
-- 创建中间表
CREATE TABLE 学生 (
    学号 CHAR(10) PRIMARY KEY,
    姓名 VARCHAR(20)
);

CREATE TABLE 课程 (
    课程号 CHAR(8) PRIMARY KEY,
    课程名 VARCHAR(40)
);

CREATE TABLE 选课 (
    学号 CHAR(10),
    课程号 CHAR(8),
    成绩 INT,
    PRIMARY KEY (学号, 课程号),
    FOREIGN KEY (学号) REFERENCES 学生(学号),
    FOREIGN KEY (课程号) REFERENCES 课程(课程号)
);
```

## 五、关系规范化题（10分，2题）

### 1. 范式判断步骤
1. **确定码**
   - 找出所有函数依赖
   - 找出能够唯一标识元组的属性组

2. **判断范式**
   - 1NF：属性是否可分
   - 2NF：是否存在部分函数依赖
   - 3NF：是否存在传递函数依赖
   - BCNF：是否存在主属性对码的依赖

### 2. 规范化示例
原表：课程选修(学号, 姓名, 课程号, 课程名, 分数, 教师, 教师办公室)

函数依赖分析：
- 学号 → 姓名
- 课程号 → 课程名, 教师
- 教师 → 教师办公室
- (学号, 课程号) → 分数

规范化过程：
```sql
-- 学生表(2NF)
CREATE TABLE 学生 (
    学号 CHAR(10) PRIMARY KEY,
    姓名 VARCHAR(20)
);

-- 教师表(3NF)
CREATE TABLE 教师 (
    教师编号 CHAR(8) PRIMARY KEY,
    教师姓名 VARCHAR(20),
    办公室 VARCHAR(30)
);

-- 课程表(3NF)
CREATE TABLE 课程 (
    课程号 CHAR(8) PRIMARY KEY,
    课程名 VARCHAR(40),
    教师编号 CHAR(8),
    FOREIGN KEY (教师编号) REFERENCES 教师(教师编号)
);

-- 选课表(3NF)
CREATE TABLE 选课 (
    学号 CHAR(10),
    课程号 CHAR(8),
    分数 INT,
    PRIMARY KEY (学号, 课程号),
    FOREIGN KEY (学号) REFERENCES 学生(学号),
    FOREIGN KEY (课程号) REFERENCES 课程(课程号)
);
```

## 考试答题要点

### 1. 选择题技巧
- 重点关注概念之间的区别
- 理解并记忆专业术语的准确定义
- 注意题目中的关键词

### 2. SQL语句题技巧
- 仔细阅读表结构和数据要求
- 条件查询注意WHERE和HAVING的使用场景
- 多表查询先确定关联条件
- 分组统计先确定分组字段

### 3. 设计题技巧
- ER图要画得规范清晰
- 注意标注实体、属性和关系的类型
- 转换规则要准确运用

### 4. 规范化题技巧
- 完整列出所有函数依赖
- 说明判断范式的理由
- 规范化分解要完整且合理

祝考试顺利！
