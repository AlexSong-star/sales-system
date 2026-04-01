# 销售系统 - 技术说明文档

> 项目编号：PRJ-001
> 创建日期：2026-03-31
> 技术负责人：白展堂
> 状态：架构设计阶段

---

## 一、技术选型

### 1.1 前端
- **框架**：Vue3 + Vite
- **UI库**：待定（倾向 Element Plus / Naive UI）
- **图表**：ECharts

### 1.2 后端
- **框架**：FastAPI
- **ORM**：SQLAlchemy
- **数据库**：SQLite（开发/本地）/ PostgreSQL（生产）

### 1.3 技术栈汇总
```
前端：Vue3 + Vite + Element Plus + ECharts
后端：FastAPI + SQLAlchemy + SQLite/PostgreSQL
Python包管理：uv
```

---

## 二、项目结构
```
projects/sales-system/
├── docs/
│   ├── requirement/     # 需求文档
│   └── technical/       # 技术文档
└── code/
    ├── backend/         # FastAPI 后端
    │   ├── app/
    │   ├── models/
    │   ├── schemas/
    │   ├── routers/
    │   └── main.py
    └── frontend/        # Vue3 前端
        ├── src/
        ├── public/
        └── package.json
```

---

## 三、数据设计

（待需求确认后补充）

---

## 四、API 设计

（待需求确认后补充）

---

## 五、界面设计

（待需求确认后补充）

---

## 六、部署方案

（待需求确认后补充）

---

## 七、版本记录

| 日期 | 版本 | 内容 | 作者 |
|------|------|------|------|
| 2026-03-31 | v0.1 | 项目初始化，技术选型 | 白展堂 |
