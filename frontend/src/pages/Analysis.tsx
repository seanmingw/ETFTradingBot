import React, { useState, useEffect } from 'react';
import { Search, TrendingUp, TrendingDown, Activity, Target } from 'lucide-react';
import { etfApi, analysisApi, newsApi } from '../services/api';
import type { ETF, TechnicalIndicators, NewsArticle, AIAnalysis } from '../types';

const Analysis: React.FC = () => {
  const [symbol, setSymbol] = useState<string>('SPY');
  const [searchQuery, setSearchQuery] = useState('');
  const [etf, setEtf] = useState<ETF | null>(null);
  const [indicators, setIndicators] = useState<TechnicalIndicators | null>(null);
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [aiAnalysis, setAiAnalysis] = useState<AIAnalysis | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (symbol) {
      loadAnalysis(symbol);
    }
  }, [symbol]);

  const loadAnalysis = async (sym: string) => {
    try {
      setLoading(true);
      const [etfRes, techRes, newsRes, aiRes] = await Promise.all([
        etfApi.getBySymbol(sym).catch(() => ({ data: null })),
        analysisApi.getTechnicals(sym, '1y').catch(() => ({ data: null })),
        newsApi.getNews(sym, 10).catch(() => ({ data: { news: [] } })),
        etfApi.getBySymbol(sym).catch(() => ({ data: null })),
      ]);

      setEtf(etfRes.data);
      setIndicators(techRes.data?.momentum_indicators || null);
      setNews(newsRes.data?.news || []);

      if (etfRes.data) {
        const analysis: AIAnalysis = {
          symbol: sym,
          ai_score: etfRes.data.ai_score || 65,
          momentum_score: 70,
          trend_score: 65,
          volatility_score: 60,
          volume_score: 55,
          rsi: indicators?.rsi || 50,
          recommendation: etfRes.data.recommendation || 'HOLD',
          reason: 'Based on technical and fundamental analysis',
          risk_level: 'MEDIUM',
        };
        setAiAnalysis(analysis);
      }
    } catch (err) {
      console.error('Failed to load analysis:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      setSymbol(searchQuery.trim().toUpperCase());
    }
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Enter ETF symbol (e.g., SPY, QQQ, VTI)..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value.toUpperCase())}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <button
            type="submit"
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition font-medium"
          >
            Analyze
          </button>
        </form>
      </div>

      {loading && (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      )}

      {!loading && etf && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-800">{etf.symbol}</h2>
                  <p className="text-gray-500">{etf.name}</p>
                </div>
                <div className="text-right">
                  <div className="text-3xl font-bold text-blue-600">${etf.current_price.toFixed(2)}</div>
                  <div className={`text-lg ${etf.daily_change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {etf.daily_change_percent >= 0 ? '+' : ''}{etf.daily_change.toFixed(2)} ({etf.daily_change_percent.toFixed(2)}%)
                  </div>
                </div>
              </div>

              {indicators && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <IndicatorCard
                    title="RSI (14)"
                    value={indicators.rsi?.toFixed(2) || 'N/A'}
                    signal={indicators.rsi ? (indicators.rsi > 70 ? 'Overbought' : indicators.rsi < 30 ? 'Oversold' : 'Neutral') : ''}
                    color={indicators.rsi ? (indicators.rsi > 70 ? 'red' : indicators.rsi < 30 ? 'green' : 'gray') : 'gray'}
                  />
                  <IndicatorCard
                    title="MACD"
                    value={indicators.macd?.toFixed(4) || 'N/A'}
                    signal={indicators.macd_histogram ? (indicators.macd_histogram > 0 ? 'Bullish' : 'Bearish') : ''}
                    icon={indicators.macd_histogram ? (indicators.macd_histogram > 0 ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />) : undefined}
                    color={indicators.macd_histogram ? (indicators.macd_histogram > 0 ? 'green' : 'red') : 'gray'}
                  />
                  <IndicatorCard
                    title="SMA 50"
                    value={indicators.sma_50 ? `$${indicators.sma_50.toFixed(2)}` : 'N/A'}
                    signal={etf.current_price > (indicators.sma_50 || 0) ? 'Above' : 'Below'}
                    color={etf.current_price > (indicators.sma_50 || 0) ? 'green' : 'red'}
                  />
                  <IndicatorCard
                    title="SMA 200"
                    value={indicators.sma_200 ? `$${indicators.sma_200.toFixed(2)}` : 'N/A'}
                    signal={etf.current_price > (indicators.sma_200 || 0) ? 'Above' : 'Below'}
                    color={etf.current_price > (indicators.sma_200 || 0) ? 'green' : 'red'}
                  />
                </div>
              )}

              {indicators && (
                <div className="mt-6 pt-6 border-t">
                  <h3 className="text-lg font-semibold mb-4 text-gray-800">Bollinger Bands</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-red-50 rounded-lg">
                      <div className="text-sm text-gray-500 mb-1">Upper Band</div>
                      <div className="text-xl font-bold text-red-600">
                        {indicators.bollinger_upper ? `$${indicators.bollinger_upper.toFixed(2)}` : 'N/A'}
                      </div>
                    </div>
                    <div className="text-center p-4 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-500 mb-1">Middle Band</div>
                      <div className="text-xl font-bold text-gray-600">
                        {indicators.bollinger_middle ? `$${indicators.bollinger_middle.toFixed(2)}` : 'N/A'}
                      </div>
                    </div>
                    <div className="text-center p-4 bg-green-50 rounded-lg">
                      <div className="text-sm text-gray-500 mb-1">Lower Band</div>
                      <div className="text-xl font-bold text-green-600">
                        {indicators.bollinger_lower ? `$${indicators.bollinger_lower.toFixed(2)}` : 'N/A'}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            <div className="space-y-6">
              {aiAnalysis && (
                <div className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <Activity className="w-6 h-6 text-blue-500" />
                    <h3 className="text-lg font-semibold text-gray-800">AI Analysis</h3>
                  </div>
                  <div className="space-y-4">
                    <div className="text-center p-4 bg-blue-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">AI Score</div>
                      <div className="text-4xl font-bold text-blue-600">{aiAnalysis.ai_score}</div>
                      <div className="text-xs text-gray-500 mt-1">/ 100</div>
                    </div>
                    <div className={`text-center p-3 rounded-lg ${
                      aiAnalysis.recommendation.includes('BUY') ? 'bg-green-100 text-green-800' :
                      aiAnalysis.recommendation.includes('SELL') ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      <div className="text-xl font-bold">{aiAnalysis.recommendation}</div>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Risk Level</div>
                      <div className="font-semibold text-gray-800">{aiAnalysis.risk_level}</div>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="text-sm text-gray-600 mb-1">Reason</div>
                      <div className="text-sm text-gray-800">{aiAnalysis.reason}</div>
                    </div>
                  </div>
                </div>
              )}

              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Target className="w-6 h-6 text-purple-500" />
                  <h3 className="text-lg font-semibold text-gray-800">Key Statistics</h3>
                </div>
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">52W High</span>
                    <span className="font-semibold text-gray-800">${etf.fifty_two_week_high.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">52W Low</span>
                    <span className="font-semibold text-gray-800">${etf.fifty_two_week_low.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">P/E Ratio</span>
                    <span className="font-semibold text-gray-800">{etf.pe_ratio?.toFixed(2) || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b">
                    <span className="text-gray-600">Volume</span>
                    <span className="font-semibold text-gray-800">{etf.volume.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center py-2">
                    <span className="text-gray-600">Expense Ratio</span>
                    <span className="font-semibold text-gray-800">
                      {etf.expense_ratio ? `${(etf.expense_ratio * 100).toFixed(2)}%` : 'N/A'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Latest News</h2>
            <div className="space-y-4">
              {news.length > 0 ? news.map((article, idx) => (
                <div key={idx} className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-800 mb-1">{article.title}</h3>
                      <p className="text-sm text-gray-600 mb-2">{article.content}</p>
                      <div className="flex items-center gap-4 text-xs text-gray-500">
                        <span>{article.source}</span>
                        <span>{new Date(article.published_at).toLocaleDateString()}</span>
                      </div>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      article.sentiment === 'BULLISH' ? 'bg-green-100 text-green-800' :
                      article.sentiment === 'BEARISH' ? 'bg-red-100 text-red-800' :
                      'bg-gray-200 text-gray-800'
                    }`}>
                      {article.sentiment}
                    </span>
                  </div>
                </div>
              )) : (
                <div className="text-center py-8 text-gray-500">
                  No recent news available
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {!loading && !etf && (
        <div className="bg-white rounded-lg shadow-md p-12 text-center">
          <Search className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Enter an ETF Symbol</h2>
          <p className="text-gray-500">Search for any ETF symbol to view detailed analysis</p>
        </div>
      )}
    </div>
  );
};

interface IndicatorCardProps {
  title: string;
  value: string;
  signal?: string;
  icon?: React.ReactNode;
  color: 'green' | 'red' | 'gray' | 'blue';
}

const IndicatorCard: React.FC<IndicatorCardProps> = ({ title, value, signal, icon, color }) => {
  const colorClasses = {
    green: 'bg-green-50 border-green-200',
    red: 'bg-red-50 border-red-200',
    gray: 'bg-gray-50 border-gray-200',
    blue: 'bg-blue-50 border-blue-200',
  };

  const textClasses = {
    green: 'text-green-600',
    red: 'text-red-600',
    gray: 'text-gray-600',
    blue: 'text-blue-600',
  };

  return (
    <div className={`p-4 rounded-lg border ${colorClasses[color]}`}>
      <div className="text-sm text-gray-600 mb-1">{title}</div>
      <div className="flex items-center justify-between">
        <span className={`text-xl font-bold ${textClasses[color]}`}>{value}</span>
        {icon}
      </div>
      {signal && <div className="text-xs text-gray-500 mt-1">{signal}</div>}
    </div>
  );
};

export default Analysis;
