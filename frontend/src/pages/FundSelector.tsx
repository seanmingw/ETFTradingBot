import React, { useState, useEffect } from 'react';
import { Search, Filter, TrendingUp, TrendingDown, BarChart3 } from 'lucide-react';

interface Fund {
  symbol: string;
  name: string;
  fund_type: 'exchange' | 'offline';
  current_price: number;
  daily_change: number;
  daily_change_percent: number;
  volume: number;
  region?: string;
  category?: string;
  fund_company?: string;
  expense_ratio?: number;
}

const FundSelector: React.FC = () => {
  const [funds, setFunds] = useState<Fund[]>([]);
  const [filteredFunds, setFilteredFunds] = useState<Fund[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [fundType, setFundType] = useState<string>('all');
  const [region, setRegion] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadFunds();
  }, [fundType, region]);

  useEffect(() => {
    filterFunds();
  }, [searchQuery, funds]);

  const loadFunds = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();

      if (fundType !== 'all') {
        params.append('fund_type', fundType);
      }
      if (region !== 'all') {
        params.append('region', region);
      }

      const response = await fetch(`http://localhost:8001/api/funds/list?${params.toString()}`);
      const data = await response.json();
      setFunds(data);
    } catch (error) {
      console.error('Failed to load funds:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterFunds = () => {
    if (!searchQuery.trim()) {
      setFilteredFunds(funds);
      return;
    }

    const query = searchQuery.toLowerCase();
    const filtered = funds.filter(fund =>
      fund.symbol.toLowerCase().includes(query) ||
      fund.name.toLowerCase().includes(query)
    );
    setFilteredFunds(filtered);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">基金选择</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Filter className="w-4 h-4 inline mr-1" />
              基金类型
            </label>
            <select
              value={fundType}
              onChange={(e) => setFundType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">全部</option>
              <option value="exchange">场内基金 (ETF)</option>
              <option value="offline">场外基金</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <BarChart3 className="w-4 h-4 inline mr-1" />
              地区/市场
            </label>
            <select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">全部</option>
              <option value="China">中国市场</option>
              <option value="US">美国市场</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              <Search className="w-4 h-4 inline mr-1" />
              搜索基金
            </label>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="输入代码或名称..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div className="mb-4 flex gap-4">
          <div className="px-4 py-2 bg-blue-100 rounded-lg">
            <span className="text-blue-800 font-semibold">场内基金 (ETF)</span>
            <span className="text-blue-600 ml-2">
              {funds.filter(f => f.fund_type === 'exchange').length} 只
            </span>
          </div>
          <div className="px-4 py-2 bg-green-100 rounded-lg">
            <span className="text-green-800 font-semibold">场外基金</span>
            <span className="text-green-600 ml-2">
              {funds.filter(f => f.fund_type === 'offline').length} 只
            </span>
          </div>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredFunds.map((fund) => (
              <div
                key={fund.symbol}
                className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition cursor-pointer border-l-4"
                style={{
                  borderLeftColor: fund.fund_type === 'exchange' ? 'blue' : 'green'
                }}
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <div className="font-bold text-lg text-gray-800">{fund.symbol}</div>
                    <div className="text-sm text-gray-600">{fund.name}</div>
                  </div>
                  <span
                    className={`px-2 py-1 rounded text-xs font-medium ${
                      fund.fund_type === 'exchange'
                        ? 'bg-blue-100 text-blue-800'
                        : 'bg-green-100 text-green-800'
                    }`}
                  >
                    {fund.fund_type === 'exchange' ? '场内' : '场外'}
                  </span>
                </div>

                <div className="flex justify-between items-end mt-3">
                  <div>
                    <div className="text-2xl font-bold text-gray-800">
                      {fund.fund_type === 'offline' ? '' : '¥'}{fund.current_price.toFixed(3)}
                    </div>
                    <div className={`flex items-center text-sm ${
                      fund.daily_change >= 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {fund.daily_change >= 0 ? (
                        <TrendingUp className="w-4 h-4 mr-1" />
                      ) : (
                        <TrendingDown className="w-4 h-4 mr-1" />
                      )}
                      {fund.daily_change >= 0 ? '+' : ''}{fund.daily_change.toFixed(4)}
                      ({fund.daily_change_percent.toFixed(2)}%)
                    </div>
                  </div>

                  <div className="text-right text-xs text-gray-500">
                    {fund.region && <div>{fund.region === 'China' ? '🇨🇳' : '🇺🇸'} {fund.region}</div>}
                    {fund.category && <div>{fund.category}</div>}
                    {fund.fund_company && <div>{fund.fund_company}</div>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {!loading && filteredFunds.length === 0 && (
          <div className="text-center py-12 text-gray-500">
            未找到符合条件的基金
          </div>
        )}
      </div>
    </div>
  );
};

export default FundSelector;
