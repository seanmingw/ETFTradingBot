# 全球股市ETF自动化交易程序 - 需求规格文档

## 1. 项目概述

### 项目名称
Global ETF Trading Bot (全球ETF智能交易机器人)

### 核心功能
基于AI分析的全球股市ETF自动化交易系统，能够：
- 智能筛选和推荐ETF
- 分析历史走势
- 关联最新新闻
- 执行自动化交易

### 目标用户
- 有一定投资经验的用户
- 希望自动化投资ETF的投资者
- 需要全球化资产配置的用户

## 2. 技术架构

### 技术栈
- **后端**: Python 3.9+
- **数据库**: SQLite (轻量级), Redis (缓存)
- **Web框架**: FastAPI
- **数据获取**: yfinance, requests
- **AI/ML**: transformers, scikit-learn
- **前端**: React + TypeScript
- **交易API**: Alpaca API / Interactive Brokers

### 项目结构
```
etf-trading-bot/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── etf.py
│   │   │   ├── trade.py
│   │   │   └── news.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── etf_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── news_service.py
│   │   │   ├── trading_service.py
│   │   │   └── analysis_service.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── etf.py
│   │   │   ├── trades.py
│   │   │   ├── analysis.py
│   │   │   └── news.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── market_data.py
│   │       └── indicators.py
│   ├── tests/
│   │   ├── test_etf_service.py
│   │   ├── test_ai_service.py
│   │   └── test_trading.py
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ETFSelector.tsx
│   │   │   ├── PriceChart.tsx
│   │   │   ├── NewsFeed.tsx
│   │   │   ├── TradePanel.tsx
│   │   │   └── Dashboard.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Trading.tsx
│   │   │   └── Analysis.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
└── docker-compose.yml
```

## 3. 功能规格

### 3.1 ETF数据管理

#### 支持的全球ETF市场
- **美国**: SPY, QQQ, VTI, IWM, EFA, EEM, VWO, GLD, TLT等
- **欧洲**: VGK, IEFA, EZU等
- **亚洲**: MCHI, EWY, EWT等
- **行业ETF**: XLK, XLF, XLE, XLV等

#### 数据字段
- ETF代码 (symbol)
- 名称 (name)
- 当前价格
- 日涨跌幅
- 52周最高/最低
- 成交量
- 资产管理规模 (AUM)
- 费用率 (expense_ratio)
- 地区分类
- 行业分类

### 3.2 AI分析引擎

#### ETF智能选择算法
```python
基于多因子分析的ETF推荐系统：

因子权重:
- 动量因子 (30%): 近3-6个月价格走势
- 价值因子 (25%): PE, PB估值指标
- 质量因子 (20%): 跟踪误差, 流动性
- 趋势因子 (15%): 50日/200日均线位置
- 波动率因子 (10%): 历史波动率, 夏普比率
```

#### AI模型
- 使用transformers进行新闻情感分析
- 使用scikit-learn进行趋势预测
- 使用LSTM进行价格预测

### 3.3 历史走势分析

#### 图表类型
- K线图
- 均线图 (MA5, MA20, MA50, MA200)
- 布林带
- MACD
- RSI
- 成交量图

#### 技术指标计算
- 移动平均线 (SMA, EMA)
- 相对强弱指数 (RSI)
- MACD
- 布林带
- 随机指标 (KDJ)
- 成交量加权平均价 (VWAP)

### 3.4 新闻分析系统

#### 新闻来源
- Yahoo Finance
- Reuters
- Bloomberg
- 财经媒体API

#### 新闻分析内容
- 情感分析 (看涨/看跌/中性)
- 关键词提取
- 相关性评分
- 发布时间

### 3.5 自动化交易

#### 交易策略
```python
策略类型:
1. 趋势跟踪策略
   - 入场: 价格突破20日均线 + 放量
   - 止损: 2%回撤
   - 止盈: 8%盈利或跌破均线

2. 均值回归策略
   - 入场: 价格触及布林带下轨
   - 止损: 1.5%回撤
   - 止盈: 5%盈利

3. 配对交易策略
   - 监控高度相关的ETF
   - 当价差偏离历史均值时入场
```

#### 订单类型
- 市价单 (Market Order)
- 限价单 (Limit Order)
- 止损单 (Stop Loss)
- 止盈单 (Take Profit)

### 3.6 Web界面功能

#### 首页/仪表盘
- 总资产概览
- 今日盈亏
- 持仓ETF列表
- 推荐ETF展示
- 快速交易入口

#### ETF选择页面
- ETF筛选器 (地区, 行业, 费用率)
- AI推荐列表
- 个股详情
- 相关新闻
- 历史走势图表

#### 交易页面
- 当前持仓
- 挂单列表
- 交易历史
- 快速买卖面板

#### 分析页面
- 自选ETF对比
- 技术指标展示
- AI预测结果
- 新闻情感分析

## 4. 数据库设计

### ETF信息表
```sql
CREATE TABLE etf_info (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100),
    category VARCHAR(50),
    region VARCHAR(50),
    expense_ratio DECIMAL(5,4),
    aum BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 历史价格表
```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    open DECIMAL(10,4),
    high DECIMAL(10,4),
    low DECIMAL(10,4),
    close DECIMAL(10,4),
    volume BIGINT,
    UNIQUE(symbol, date)
);
```

### 新闻表
```sql
CREATE TABLE news (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10),
    title VARCHAR(200),
    content TEXT,
    source VARCHAR(50),
    url VARCHAR(300),
    sentiment VARCHAR(20),
    sentiment_score DECIMAL(5,4),
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 交易记录表
```sql
CREATE TABLE trades (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    action VARCHAR(10) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10,4),
    commission DECIMAL(10,4),
    total_amount DECIMAL(12,4),
    strategy VARCHAR(50),
    status VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 持仓表
```sql
CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    quantity INTEGER NOT NULL,
    avg_cost DECIMAL(10,4),
    current_price DECIMAL(10,4),
    unrealized_pnl DECIMAL(12,4),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 5. API接口设计

### ETF接口
```
GET  /api/etf/list                    # 获取ETF列表
GET  /api/etf/{symbol}                # 获取单个ETF详情
GET  /api/etf/search?q={query}        # 搜索ETF
POST /api/etf/recommend                # AI推荐ETF
GET  /api/etf/compare?symbols={list}   # 对比ETF
```

### 价格接口
```
GET  /api/price/{symbol}              # 获取实时价格
GET  /api/price/{symbol}/history?period={period}  # 获取历史价格
GET  /api/price/{symbol}/indicators   # 获取技术指标
```

### 新闻接口
```
GET  /api/news/{symbol}              # 获取ETF相关新闻
GET  /api/news/sentiment/{symbol}     # 获取新闻情感分析
```

### 交易接口
```
GET  /api/trades                     # 获取交易记录
POST /api/trades                     # 创建交易订单
GET  /api/trades/{id}                # 获取订单详情
DELETE /api/trades/{id}              # 取消订单
GET  /api/positions                  # 获取持仓
```

### 分析接口
```
POST /api/analysis/predict           # AI价格预测
GET  /api/analysis/technicals/{symbol}  # 技术分析
GET  /api/analysis/sentiment/{symbol}   # 情感分析
```

## 6. 用户交互流程

### ETF选择流程
1. 用户进入ETF选择页面
2. 选择筛选条件 (地区/行业/风险偏好)
3. 系统返回符合条件的ETF列表
4. 用户点击某个ETF查看详情
5. 显示历史走势、技术指标、相关新闻
6. AI给出分析建议和评分

### 交易执行流程
1. 用户选择要交易的ETF
2. 选择买入/卖出
3. 输入数量
4. 选择订单类型 (市价/限价)
5. 确认订单信息
6. 执行交易
7. 更新持仓

### 自动交易流程
1. 系统每日定时扫描市场
2. AI分析各ETF的信号
3. 根据策略执行交易
4. 设置止损止盈
5. 记录交易日志
6. 发送通知

## 7. 风险控制

### 仓位管理
- 单个ETF最大仓位: 20%
- 单日最大交易次数: 10次
- 总仓位控制: 最大80%

### 止损机制
- 单笔交易最大亏损: 3%
- 日内最大亏损: 5%
- 总资产回撤限制: 15%

### 风控措施
- 交易前风险评估
- 实时持仓监控
- 异常交易检测
- 自动熔断机制

## 8. 性能要求

- 页面加载时间: < 2秒
- API响应时间: < 500ms
- 数据更新频率: 实时价格, 15分钟新闻更新
- 系统可用性: 99.9%

## 9. 扩展性设计

- 支持插件式数据源
- 支持自定义交易策略
- 支持多交易所对接
- 支持量化回测

## 10. 开发优先级

### Phase 1 - 基础功能 (MVP)
1. ETF数据获取和展示
2. 历史价格图表
3. 简单的筛选功能
4. 基础交易界面

### Phase 2 - 智能功能
1. AI推荐算法
2. 新闻情感分析
3. 技术指标计算
4. 基础风控

### Phase 3 - 自动化交易
1. 交易策略实现
2. 自动化执行
3. 实时监控
4. 通知系统

### Phase 4 - 高级功能
1. 高级AI预测
2. 组合优化
3. 绩效分析
4. 回测系统
