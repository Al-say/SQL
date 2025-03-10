# 数据库原理试卷三

## 一、单选题（共20题，每题2分，共40分）

1. 在数据库系统中，数据的物理独立性是通过（）实现的。
   - A. 外模式/模式映像
   - B. 模式/内模式映像
   - C. 内模式/存储映像
   - D. 模式/外模式映像

2. 在数据库设计过程中，（）阶段的主要任务是进行需求分析。
   - A. 概念设计
   - B. 逻辑设计
   - C. 需求分析
   - D. 物理设计

3. 关系模式R中，如果属性组X可以唯一标识一个元组，则X是R的（）。
   - A. 主属性
   - B. 外键
   - C. 候选码
   - D. 主码

4. 下列关于事务的说法中，错误的是（）。
   - A. 事务具有原子性
   - B. 事务可以部分提交
   - C. 事务具有持久性
   - D. 事务具有隔离性

5. 在数据库并发控制中，（）是用来防止读取不一致数据的机制。
   - A. 共享锁
   - B. 排他锁
   - C. 死锁检测
   - D. 日志记录

6. MySQL中，以下哪个命令用于备份数据库（）。
   - A. mysqldump
   - B. mysql
   - C. mysqlshow
   - D. mysqlimport

7. 关系数据库中的完整性约束不包括（）。
   - A. 实体完整性
   - B. 参照完整性
   - C. 用户定义完整性
   - D. 事务完整性

8. 以下哪个不是MySQL支持的存储引擎（）。
   - A. InnoDB
   - B. MyISAM
   - C. Oracle
   - D. Memory

9. 在E-R图中，（）用来表示实体之间的联系。
   - A. 矩形
   - B. 椭圆
   - C. 菱形
   - D. 三角形

10. 关系代数中，投影运算的结果（）。
    - A. 垂直分割关系
    - B. 水平分割关系
    - C. 连接两个关系
    - D. 合并两个关系

11. 下列哪个不是合法的SQL聚集函数（）。
    - A. COUNT
    - B. SUM 
    - C. MEDIAN
    - D. AVG

12. 在视图中不能使用的SQL语句是（）。
    - A. SELECT
    - B. CREATE INDEX
    - C. UPDATE
    - D. DELETE

13. 数据库恢复技术中，（）用于保证数据库的可靠性。
    - A. 并发控制
    - B. 日志文件
    - C. 存储过程
    - D. 触发器

14. 以下哪种操作会导致表中的数据发生改变（）。
    - A. SELECT
    - B. GRANT
    - C. MERGE
    - D. CREATE INDEX

15. 关系数据库规范化的主要目的是（）。
    - A. 提高查询效率
    - B. 减少数据冗余
    - C. 增加数据安全性
    - D. 提高并发性能

16. 以下哪个语句用于回滚事务（）。
    - A. COMMIT
    - B. ROLLBACK
    - C. SAVEPOINT
    - D. BEGIN

17. 在SQL中，GROUP BY子句后面不能使用（）。
    - A. HAVING
    - B. WHERE
    - C. ORDER BY
    - D. LIMIT

18. 数据库的（）是指数据的逻辑结构及其联系的集合。
    - A. 外模式
    - B. 概念模式
    - C. 内模式
    - D. 物理模式

19. 以下哪个不是触发器的触发事件（）。
    - A. INSERT
    - B. SELECT
    - C. UPDATE
    - D. DELETE

20. 在创建索引时，（）类型的字段最适合建立索引。
    - A. 频繁更新的字段
    - B. 大文本字段
    - C. 经常用于查询条件的字段
    - D. 取值范围很小的字段

## 二、判断题（共10题，每题1分，共10分）

1. 数据库的逻辑独立性是通过模式/内模式映像实现的。（）

2. 存储过程可以接收参数并返回多个值。（）

3. 主键约束和唯一约束都可以保证字段值的唯一性。（）

4. 视图是一个虚拟表，它所包含的数据都来自于定义视图的查询。（）

5. 在关系数据库中，任何表都必须有主键。（）

6. BCNF范式一定是3NF范式，但3NF范式不一定是BCNF范式。（）

7. MySQL中的InnoDB存储引擎支持事务处理。（）

8. 数据库备份是指将数据库中的数据复制到其他存储介质上。（）

9. 在SQL中，子查询可以嵌套在另一个子查询中。（）

10. 数据库索引会提高查询速度，但会降低更新速度。（）

## 三、SQL查询题（共5题，每题4分，共20分）

有以下关系模式：
```sql
学生(学号，姓名，性别，年龄，专业)
课程(课程号，课程名，学分，教师)
成绩(学号，课程号，成绩)
```

请写出下列查询的SQL语句：

1. 查询"计算机科学"专业学生的学号、姓名和平均成绩。

2. 查询至少选修了3门课程的学生姓名。

3. 查询没有不及格课程的学生姓名和平均成绩。

4. 查询选修了全部课程的学生姓名。

5. 创建一个视图，显示每个专业的学生人数和平均年龄。

## 四、数据库设计题（20分）

设计一个在线购物系统的数据库，要求：

1. 分析系统的主要实体和联系（5分）
2. 画出E-R图（8分）
3. 将E-R图转换为关系模式，并说明主外键（7分）

系统需求：
- 顾客可以注册账号，包含用户名、密码、姓名、联系方式、送货地址等信息
- 商品信息包括商品编号、名称、价格、库存量、类别等
- 每个订单包含订单编号、下单时间、总金额、支付状态、配送状态等
- 需要记录订单中包含的商品及其数量
- 顾客可以对购买过的商品进行评价

## 五、关系规范化题（10分）

给定关系模式R(A, B, C, D, E)，其函数依赖集为：
F={AB→C, C→D, D→E, B→D}

1. 求出R的候选码（4分）
2. 判断R的范式级别（2分）
3. 将R无损分解为3NF模式（4分）
