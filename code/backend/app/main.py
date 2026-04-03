from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import inquiries, customers, dashboard

# 建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="外贸销售系统 API", version="0.1.0")

# CORS - 允许所有来源（GitHub Pages + 本地开发）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(dashboard.router)
app.include_router(inquiries.router)
app.include_router(customers.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
