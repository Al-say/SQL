-- SQL管理工具示例查询

-- 1. 基本查询示例
SELECT 
    employee_id,
    first_name,
    last_name,
    email,
    hire_date
FROM employees
WHERE department_id = 10
ORDER BY hire_date DESC;

-- 2. 连接查询示例
SELECT 
    e.first_name || ' ' || e.last_name AS full_name,
    d.department_name,
    j.job_title,
    e.salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN jobs j ON e.job_id = j.job_id
WHERE e.salary > 50000;

-- 3. 聚合查询示例
SELECT 
    d.department_name,
    COUNT(*) AS employee_count,
    AVG(e.salary) AS avg_salary,
    MAX(e.salary) AS max_salary,
    MIN(e.salary) AS min_salary
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name
HAVING COUNT(*) > 5
ORDER BY avg_salary DESC;

-- 4. 子查询示例
SELECT 
    employee_id,
    first_name,
    last_name,
    salary
FROM employees
WHERE salary > (
    SELECT AVG(salary) 
    FROM employees
)
ORDER BY salary DESC;

-- 5. 窗口函数示例（适用于支持的数据库）
SELECT 
    employee_id,
    first_name,
    last_name,
    salary,
    RANK() OVER (ORDER BY salary DESC) as salary_rank,
    ROW_NUMBER() OVER (PARTITION BY department_id ORDER BY salary DESC) as dept_rank
FROM employees;

-- 6. CTE（公共表表达式）示例
WITH high_earners AS (
    SELECT employee_id, first_name, last_name, salary
    FROM employees
    WHERE salary > 75000
),
department_stats AS (
    SELECT 
        department_id,
        COUNT(*) as total_employees,
        AVG(salary) as avg_salary
    FROM employees
    GROUP BY department_id
)
SELECT 
    he.first_name,
    he.last_name,
    he.salary,
    ds.avg_salary as dept_avg_salary
FROM high_earners he
JOIN employees e ON he.employee_id = e.employee_id
JOIN department_stats ds ON e.department_id = ds.department_id;

-- 7. 数据更新示例
UPDATE employees 
SET salary = salary * 1.1 
WHERE department_id = 20 
AND performance_rating = 'Excellent';

-- 8. 数据插入示例
INSERT INTO employees (
    employee_id, 
    first_name, 
    last_name, 
    email, 
    hire_date, 
    job_id, 
    salary, 
    department_id
) VALUES (
    1001, 
    'John', 
    'Doe', 
    'john.doe@company.com', 
    CURRENT_DATE, 
    'IT_PROG', 
    65000, 
    60
);

-- 9. 创建表示例
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget DECIMAL(15,2),
    status VARCHAR(20) DEFAULT 'Planning',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. 创建索引示例
CREATE INDEX idx_employees_department ON employees(department_id);
CREATE INDEX idx_employees_salary ON employees(salary);
CREATE INDEX idx_employees_name ON employees(last_name, first_name);
