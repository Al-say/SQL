# SQL管理工具 Makefile

.PHONY: help install run test clean dev docs

# 默认目标
help:
	@echo "SQL数据库管理工具 - 可用命令："
	@echo "  install    - 安装依赖包"
	@echo "  run        - 运行应用"
	@echo "  test       - 运行测试"
	@echo "  clean      - 清理临时文件"
	@echo "  dev        - 开发模式运行"
	@echo "  docs       - 生成文档"
	@echo "  lint       - 代码风格检查"
	@echo "  format     - 代码格式化"

# 安装依赖
install:
	@echo "安装依赖包..."
	pip install --upgrade pip
	pip install -r requirements.txt

# 运行应用
run:
	@echo "启动SQL管理工具..."
	python run.py

# 开发模式运行
dev:
	@echo "以调试模式启动..."
	python run.py --debug

# 运行测试
test:
	@echo "运行测试套件..."
	python tests/test_main.py

# 清理临时文件
clean:
	@echo "清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/

# 代码风格检查
lint:
	@echo "检查代码风格..."
	flake8 src/ tests/ --max-line-length=100

# 代码格式化
format:
	@echo "格式化代码..."
	black src/ tests/ --line-length=100

# 生成文档
docs:
	@echo "生成文档..."
	@echo "文档已位于 docs/ 目录"

# 创建示例配置
config:
	@echo "创建示例配置文件..."
	cp config/database.example.yml config/database.yml
	@echo "请编辑 config/database.yml 文件添加您的数据库连接信息"

# 安装开发依赖
install-dev: install
	@echo "安装开发依赖..."
	pip install pytest pytest-cov black flake8 mypy

# 打包应用
build:
	@echo "打包应用..."
	python setup.py sdist bdist_wheel

# 完整的开发环境设置
setup: install-dev config
	@echo "开发环境设置完成！"
	@echo "运行 'make run' 启动应用"
