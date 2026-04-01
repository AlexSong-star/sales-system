from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import inquiries, customers, dashboard

# 建表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="外贸销售系统 API", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
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
