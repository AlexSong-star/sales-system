# 外贸数字团队 - 销售管理系统

> 项目编号：PRJ-001

---

## 项目架构

| 组成部分 | 技术方案 | 访问地址 |
|---------|---------|---------|
| 前端（静态） | Vue3 + Vite + Element Plus + ECharts | https://alexsong-star.github.io/sales-system/ |
| 后端 API | FastAPI + SQLAlchemy + Railway | https://sales-system-production-0a91.up.railway.app |

## 目录结构

```
sales-system/
├── .github/workflows/deploy.yml  # GitHub Pages 自动部署
├── code/
│   ├── frontend/                  # Vue3 前端
│   └── backend/                  # FastAPI 后端（独立部署）
├── docs/
│   ├── requirement/               # 需求文档
│   └── technical/                 # 技术文档
└── README.md
```

## 部署说明

### 前端部署
- 推送 master 分支自动触发 GitHub Actions
- 构建产物部署到 `gh-pages` 分支
- 访问地址：https://alexsong-star.github.io/sales-system/

### 后端部署
- 后端部署在 Railway 平台
- 直接调用 Railway URL 提供 API 服务
- CORS 已全开放

## 团队成员分工

| 成员 | 角色 | 职责 |
|------|------|------|
| 宋强（强哥） | 产品负责人 | 拍板需求、业务决策 |
| 白展堂 | 技术负责人 | 架构设计、代码开发 |
| 吕秀才 | 核心用户 | 销售功能主要使用者 |
| 佟湘玉 | 审批/管理者 | 审核报价、订单审批 |
| 李大嘴 | 协同用户 | 跟单环节衔接 |
| 郭芙蓉 | 数据使用者 | 销售数据分析师 |

---

_最后更新：2026-04-03_
