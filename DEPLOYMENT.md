# 部署说明

## GitHub仓库
**仓库地址**: https://github.com/seanmingw/ETFTradingBot

## 本地开发

### 后端启动
```bash
cd /Users/sean/Documents/etf/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### 前端启动
```bash
cd /Users/sean/Documents/etf/frontend
npm run dev
```

访问 http://localhost:3000

## Docker部署

### 使用docker-compose
```bash
cd /Users/sean/Documents/etf
docker-compose up -d
```

### 分别构建
```bash
# 后端
cd backend
docker build -t etf-backend .
docker run -p 8001:8000 etf-backend

# 前端
cd frontend
docker build -t etf-frontend .
docker run -p 3000:3000 etf-frontend
```

## 项目结构

```
/Users/sean/Documents/etf/
├── SPEC.md                 # 详细需求规格文档
├── README.md               # 项目说明
├── backend/                # Python FastAPI后端
│   ├── app/
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   ├── routers/       # API路由
│   │   └── utils/         # 工具函数
│   ├── requirements.txt   # Python依赖
│   └── run.py            # 启动脚本
└── frontend/              # React前端
    ├── src/
    │   ├── pages/        # 页面组件
    │   ├── components/   # UI组件
    │   └── services/     # API调用
    └── package.json      # Node依赖
```

## Git信息

- 分支: main
- 最新提交: 18beebf
- 提交信息: feat: Initial commit - Global ETF Trading Bot with AI analysis

## 推送记录

✅ 成功推送到 GitHub
时间: 2026-05-13
文件数: 46个
