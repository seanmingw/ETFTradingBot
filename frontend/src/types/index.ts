export interface ETF {
  symbol: string;
  name: string;
  category?: string;
  region?: string;
  expense_ratio?: number;
  aum?: number;
  current_price: number;
  daily_change: number;
  daily_change_percent: number;
  volume: number;
  pe_ratio?: number;
  fifty_two_week_high: number;
  fifty_two_week_low: number;
  ai_score?: number;
  recommendation?: string;
}

export interface PriceData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface TechnicalIndicators {
  sma_5?: number;
  sma_20?: number;
  sma_50?: number;
  sma_200?: number;
  ema_12?: number;
  ema_26?: number;
  macd?: number;
  macd_signal?: number;
  macd_histogram?: number;
  rsi?: number;
  bollinger_upper?: number;
  bollinger_middle?: number;
  bollinger_lower?: number;
  vwap?: number;
}

export interface NewsArticle {
  id?: number;
  symbol: string;
  title: string;
  content?: string;
  source: string;
  url?: string;
  sentiment: string;
  sentiment_score?: number;
  published_at: string;
}

export interface TradeRequest {
  symbol: string;
  action: 'buy' | 'sell';
  quantity: number;
  order_type?: 'market' | 'limit';
  limit_price?: number;
  strategy?: string;
}

export interface TradeResponse {
  id: number;
  symbol: string;
  action: string;
  quantity: number;
  price: number;
  commission: number;
  total_amount: number;
  strategy: string;
  status: string;
  created_at: string;
}

export interface Position {
  id?: number;
  symbol: string;
  quantity: number;
  avg_cost: number;
  current_price: number;
  market_value: number;
  unrealized_pnl: number;
  unrealized_pnl_percent: number;
}

export interface PortfolioSummary {
  total_value: number;
  total_cost: number;
  total_pnl: number;
  total_pnl_percent: number;
  day_pnl: number;
  day_pnl_percent: number;
  positions: Position[];
  cash: number;
  buying_power: number;
}

export interface AIAnalysis {
  symbol: string;
  ai_score: number;
  momentum_score: number;
  trend_score: number;
  volatility_score: number;
  volume_score: number;
  rsi: number;
  recommendation: string;
  reason: string;
  risk_level: string;
}
