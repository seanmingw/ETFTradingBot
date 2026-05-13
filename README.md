# Global ETF Trading Bot

基于AI的全球股市ETF自动化交易程序

## 功能特性

- **智能ETF筛选**: AI驱动的ETF推荐系统，基于多因子分析
- **历史走势分析**: 完整的技术指标分析（RSI, MACD, 布林带等）
- **新闻情感分析**: 实时新闻获取与情感分析
- **自动化交易**: 支持市价单、限价单、止损单
- **实时监控**: 持仓管理、盈亏追踪
- **风险控制**: 仓位管理、止损机制

## 技术栈

- **后端**: Python 3.9+, FastAPI
- **数据库**: SQLite
- **数据获取**: yfinance
- **前端**: React 18, TypeScript, Tailwind CSS
- **图表**: Recharts

## 快速开始

### 1. 安装后端依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 安装前端依赖

```bash
cd frontend
npm install
```

### 3. 启动后端服务

```bash
cd backend
python run.py
```

后端服务将在 http://localhost:8000 启动

### 4. 启动前端服务

```bash
cd frontend
npm run dev
```

前端服务将在 http://localhost:3000 启动

## API接口

### ETF接口

- `GET /api/etf/list` - 获取ETF列表
- `GET /api/etf/{symbol}` - 获取单个ETF详情
- `GET /api/etf/search/?q={query}` - 搜索ETF
- `POST /api/etf/screen` - 筛选ETF
- `GET /api/etf/{symbol}/indicators` - 获取技术指标

### 分析接口

- `POST /api/analysis/recommend` - AI推荐ETF
- `POST /api/analysis/predict` - 价格预测
- `GET /api/analysis/{symbol}` - 综合分析
- `GET /api/analysis/technicals/{symbol}` - 技术分析

### 交易接口

- `POST /api/trades/` - 执行交易
- `GET /api/trades/` - 获取交易记录
- `GET /api/trades/positions` - 获取持仓
- `GET /api/trades/portfolio` - 获取投资组合

### 新闻接口

- `GET /api/news/{symbol}` - 获取新闻
- `GET /api/news/sentiment/{symbol}` - 情感分析

## 支持的ETF

### 美国ETF
- SPY, QQQ, VTI, IWM (宽基指数)
- EFA, EEM, VWO (国际市场)
- GLD, TLT, AGG (商品债券)
- XLK, XLF, XLE, XLV (行业ETF)

### 欧洲ETF
- VGK, IEFA, EZU, FEZ

### 亚洲ETF
- MCHI, EWY, EWT, INDA, EWJ

## AI评分系统

AI评分基于多因子模型：

- **动量因子 (30%)**: 近3-6个月价格走势
- **趋势因子 (25%)**: 均线位置和趋势强度
- **波动率因子 (20%)**: 历史波动率评估
- **成交量因子 (15%)**: 成交量趋势分析
- **RSI因子 (10%)**: 相对强弱指数

## 交易策略

1. **趋势跟踪策略**: 价格突破均线时入场
2. **均值回归策略**: 价格触及布林带边界时操作
3. **动量策略**: 基于RSI和MACD信号

## 环境变量

```env
SECRET_KEY=your-secret-key
ALPACA_API_KEY=your-alpaca-key
ALPACA_API_SECRET=your-alpaca-secret
NEWS_API_KEY=your-news-api-key
```

## 注意事项

⚠️ 本程序仅供学习和研究使用
⚠️ 实际交易前请充分了解相关风险
⚠️ 建议先使用模拟账户测试

## License

MIT License
