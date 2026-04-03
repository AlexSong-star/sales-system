FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY code/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码（不包括init_db.py，因为Docker构建时DB不存在）
COPY code/backend/app ./app
COPY code/backend/app/__init__.py ./app/__init__.py

# 暴露端口
EXPOSE 8000

# 启动（uWSGI 或者直接uvicorn）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
