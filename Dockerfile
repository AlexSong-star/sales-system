FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY code/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码
COPY code/backend/ .

# 初始化数据库
RUN python init_db.py

# 暴露端口
EXPOSE 8000

# 启动
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
