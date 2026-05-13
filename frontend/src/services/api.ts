import axios from 'axios';
import type { ETF, PriceData, TechnicalIndicators, NewsArticle, TradeRequest, TradeResponse, Position, PortfolioSummary, AIAnalysis } from '../types';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

export const etfApi = {
  getAll: (region?: string) => api.get<ETF[]>('/etf/list', { params: { region } }),
  getBySymbol: (symbol: string) => api.get<ETF>(`/etf/${symbol}`),
  search: (query: string, region?: string) => api.get<ETF[]>('/etf/search/', { params: { q: query, region } }),
  getIndicators: (symbol: string, period?: string) => api.get<TechnicalIndicators>(`/etf/${symbol}/indicators`, { params: { period } }),
};

export const analysisApi = {
  predict: (symbol: string, days?: number) => api.get('/analysis/predict', { params: { symbol, days } }),
  recommend: (region?: string, limit?: number) => api.post('/analysis/recommend', { region }, { params: { limit } }),
  getTechnicals: (symbol: string, period?: string) => api.get(`/analysis/technicals/${symbol}`, { params: { period } }),
};

export const newsApi = {
  getNews: (symbol: string, limit?: number) => api.get<{ symbol: string; news: NewsArticle[] }>(`/news/${symbol}`, { params: { limit } }),
  getSentiment: (symbol: string) => api.get(`/news/sentiment/${symbol}`),
};

export const tradeApi = {
  execute: (trade: TradeRequest) => api.post<TradeResponse>('/trades/', trade),
  getTrades: (limit?: number) => api.get<TradeResponse[]>('/trades/', { params: { limit } }),
  getPositions: () => api.get<Position[]>('/trades/positions'),
  getPortfolio: () => api.get<PortfolioSummary>('/trades/portfolio'),
};

export default api;
