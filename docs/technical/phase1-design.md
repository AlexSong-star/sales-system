# 销售系统 - 技术说明文档

> 项目编号：PRJ-001
> 创建日期：2026-03-31
> 技术负责人：白展堂
> 状态：架构设计阶段

---

## 一、技术选型

### 0.1 前端设计规范（开发时必须使用）
- `frontend-design-ultimate` - 完整前端设计流程指南
- `anthropics/skills@frontend-design` - 官方设计原则和规范（222K安装量）

### 1.1 技术栈
```
前端：Vue3 + Vite + Element Plus + ECharts
后端：FastAPI
数据库：SQLite（本地开发）
部署：本地运行（后续可切换 PostgreSQL）
Python包管理：uv
```

### 1.2 为什么这样选
| 组件 | 选择 | 原因 |
|------|------|------|
| Vue3 | 前端框架 | 生态成熟，学习成本低 |
| Element Plus | UI组件库 | Vue3生态完善，中文文档友好 |
| ECharts | 图表库 | 国产，图表类型丰富 |
| FastAPI | 后端框架 | Python技术栈，高性能，自动生成API文档 |
| SQLite | 数据库 | 零配置，本地运行，后期可迁移PostgreSQL |

---

## 二、项目结构（第一期）

```
projects/sales-system/code/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI 入口
│   │   ├── config.py         # 配置
│   │   ├── database.py        # 数据库连接
│   │   ├── models/           # ORM模型
│   │   │   ├── __init__.py
│   │   │   ├── inquiry.py     # 询盘表
│   │   │   ├── reply.py       # 回复记录表
│   │   │   └── customer.py    # 客户表（预留）
│   │   ├── schemas/          # Pydantic模型
│   │   │   ├── __init__.py
│   │   │   └── inquiry.py
│   │   └── routers/          # API路由
│   │       ├── __init__.py
│   │       ├── dashboard.py   # 仪表盘API
│   │       └── inquiry.py     # 询盘管理API
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/              # API调用
    │   ├── views/            # 页面
    │   │   ├── Dashboard.vue  # 仪表盘
    │   │   └── InquiryList.vue # 询盘列表
    │   └── router/
    ├── package.json
    └── vite.config.js
```

---

## 三、数据模型（Phase 1）

### 3.1 询盘表 (inquiry)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| channel | String | 渠道：email/whatsapp/alibaba |
| customer_name | String | 客户名 |
| customer_contact | String | 联系方式（预留） |
| product | String | 询盘产品 |
| content | Text | 询盘原始内容 |
| status | String | 状态：pending/replied/following/closed/invalid |
| assigned_to | String | 负责人 |
| created_at | DateTime | 创建时间 |
| updated_at | DateTime | 更新时间 |

### 3.2 回复记录表 (reply)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| inquiry_id | Integer | 关联询盘ID |
| content | Text | 回复内容 |
| created_at | DateTime | 回复时间 |

---

## 四、API 设计（Phase 1）

### 4.1 仪表盘
- `GET /api/dashboard/stats` - 获取统计数据
- `GET /api/dashboard/trend` - 获取趋势数据
- `GET /api/dashboard/channel-distribution` - 渠道分布

### 4.2 询盘管理
- `GET /api/inquiries` - 询盘列表（支持筛选）
- `GET /api/inquiries/{id}` - 询盘详情
- `POST /api/inquiries` - 新增询盘
- `PUT /api/inquiries/{id}` - 更新询盘
- `DELETE /api/inquiries/{id}` - 删除询盘
- `POST /api/inquiries/{id}/replies` - 添加回复
- `GET /api/inquiries/{id}/replies` - 获取回复列表

---

## 五、部署方案

### 开发环境
```bash
# 后端
cd code/backend
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# 前端
cd code/frontend
npm install
npm run dev
```

### 访问地址
- 前端：http://localhost:5173
- 后端API：http://localhost:8000
- API文档：http://localhost:8000/docs

---

## 六、版本记录

| 日期 | 版本 | 内容 | 作者 |
|------|------|------|------|
| 2026-03-31 | v0.1 | 项目初始化，技术选型 | 白展堂 |
| 2026-03-31 | v0.2 | Phase1 架构设计，数据库设计 | 白展堂 |
