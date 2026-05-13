import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, DollarSign, Activity, BarChart3 } from 'lucide-react';
import { etfApi, analysisApi, tradeApi } from '../services/api';
import type { ETF, PortfolioSummary, AIAnalysis } from '../types';

const Dashboard: React.FC = () => {
  const [etfs, setEtfs] = useState<ETF[]>([]);
  const [recommended, setRecommended] = useState<AIAnalysis[]>([]);
  const [portfolio, setPortfolio] = useState<PortfolioSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [etfRes, recRes, portRes] = await Promise.all([
        etfApi.getAll('US').catch(() => ({ data: [] })),
        analysisApi.recommend('US', 8).catch(() => ({ data: { recommendations: [] } })),
        tradeApi.getPortfolio().catch(() => null),
      ]);

      setEtfs(etfRes.data || []);
      setRecommended(recRes.data?.recommendations || []);
      setPortfolio(portRes);
    } catch (err) {
      setError('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          title="Total Value"
          value={portfolio ? `$${portfolio.total_value.toLocaleString(undefined, { minimumFractionDigits: 2 })}` : '$0.00'}
          icon={<DollarSign className="w-8 h-8" />}
          color="blue"
        />
        <StatCard
          title="Total P&L"
          value={portfolio ? `${portfolio.total_pnl >= 0 ? '+' : ''}$${portfolio.total_pnl.toFixed(2)}` : '$0.00'}
          subValue={portfolio ? `${portfolio.total_pnl_percent >= 0 ? '+' : ''}${portfolio.total_pnl_percent.toFixed(2)}%` : '0.00%'}
          icon={portfolio && portfolio.total_pnl >= 0 ? <TrendingUp className="w-8 h-8" /> : <TrendingDown className="w-8 h-8" />}
          color={portfolio && portfolio.total_pnl >= 0 ? 'green' : 'red'}
        />
        <StatCard
          title="Cash Available"
          value={portfolio ? `$${portfolio.cash.toLocaleString(undefined, { minimumFractionDigits: 2 })}` : '$0.00'}
          icon={<Activity className="w-8 h-8" />}
          color="purple"
        />
        <StatCard
          title="Positions"
          value={portfolio?.positions.length || 0}
          subValue={`${portfolio?.positions.length || 0} ETFs`}
          icon={<BarChart3 className="w-8 h-8" />}
          color="orange"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">AI Recommended ETFs</h2>
          <div className="space-y-3">
            {recommended.slice(0, 6).map((rec, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                <div className="flex-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-800">{rec.symbol}</span>
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      rec.recommendation.includes('BUY') ? 'bg-green-100 text-green-800' :
                      rec.recommendation.includes('SELL') ? 'bg-red-100 text-red-800' :
                      'bg-yellow-100 text-yellow-800'
                    }`}>
                      {rec.recommendation}
                    </span>
                  </div>
                  <div className="text-sm text-gray-500 mt-1">{rec.reason}</div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-blue-600">{rec.ai_score}</div>
                  <div className="text-xs text-gray-500">AI Score</div>
                </div>
              </div>
            ))}
            {recommended.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No recommendations available
              </div>
            )}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Popular US ETFs</h2>
          <div className="space-y-3">
            {etfs.slice(0, 8).map((etf) => (
              <div key={etf.symbol} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                <div className="flex-1">
                  <div className="font-semibold text-gray-800">{etf.symbol}</div>
                  <div className="text-sm text-gray-500">{etf.name}</div>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-gray-800">${etf.current_price.toFixed(2)}</div>
                  <div className={`text-sm ${etf.daily_change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {etf.daily_change_percent >= 0 ? '+' : ''}{etf.daily_change_percent.toFixed(2)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {portfolio && portfolio.positions.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-800">Your Positions</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-3 px-4 font-semibold text-gray-700">Symbol</th>
                  <th className="text-right py-3 px-4 font-semibold text-gray-700">Shares</th>
                  <th className="text-right py-3 px-4 font-semibold text-gray-700">Avg Cost</th>
                  <th className="text-right py-3 px-4 font-semibold text-gray-700">Current</th>
                  <th className="text-right py-3 px-4 font-semibold text-gray-700">Market Value</th>
                  <th className="text-right py-3 px-4 font-semibold text-gray-700">P&L</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.positions.map((pos) => (
                  <tr key={pos.symbol} className="border-b hover:bg-gray-50">
                    <td className="py-3 px-4 font-medium text-gray-800">{pos.symbol}</td>
                    <td className="py-3 px-4 text-right text-gray-600">{pos.quantity}</td>
                    <td className="py-3 px-4 text-right text-gray-600">${pos.avg_cost.toFixed(2)}</td>
                    <td className="py-3 px-4 text-right text-gray-600">${pos.current_price.toFixed(2)}</td>
                    <td className="py-3 px-4 text-right text-gray-600">${pos.market_value.toFixed(2)}</td>
                    <td className={`py-3 px-4 text-right font-medium ${
                      pos.unrealized_pnl >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {pos.unrealized_pnl >= 0 ? '+' : ''}${pos.unrealized_pnl.toFixed(2)}
                      <span className="block text-xs">
                        ({pos.unrealized_pnl_percent >= 0 ? '+' : ''}{pos.unrealized_pnl_percent.toFixed(2)}%)
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}
    </div>
  );
};

interface StatCardProps {
  title: string;
  value: string;
  subValue?: string;
  icon: React.ReactNode;
  color: 'blue' | 'green' | 'red' | 'purple' | 'orange';
}

const StatCard: React.FC<StatCardProps> = ({ title, value, subValue, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    purple: 'bg-purple-100 text-purple-600',
    orange: 'bg-orange-100 text-orange-600',
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
          {subValue && <p className="text-sm text-gray-500 mt-1">{subValue}</p>}
        </div>
        <div className={`p-3 rounded-full ${colorClasses[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
