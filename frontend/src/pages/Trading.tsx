import React, { useState, useEffect } from 'react';
import { ArrowUpRight, ArrowDownRight, Search, RefreshCw } from 'lucide-react';
import { etfApi, tradeApi } from '../services/api';
import type { ETF, TradeRequest, Position } from '../types';

const Trading: React.FC = () => {
  const [selectedEtf, setSelectedEtf] = useState<ETF | null>(null);
  const [etfs, setEtfs] = useState<ETF[]>([]);
  const [positions, setPositions] = useState<Position[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [tradeAction, setTradeAction] = useState<'buy' | 'sell'>('buy');
  const [quantity, setQuantity] = useState<number>(100);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [etfRes, posRes] = await Promise.all([
        etfApi.getAll('US').catch(() => ({ data: [] })),
        tradeApi.getPositions().catch(() => ({ data: [] })),
      ]);
      setEtfs(etfRes.data || []);
      setPositions(posRes.data || []);
    } catch (err) {
      setMessage({ type: 'error', text: 'Failed to load data' });
    } finally {
      setLoading(false);
    }
  };

  const handleTrade = async () => {
    if (!selectedEtf) {
      setMessage({ type: 'error', text: 'Please select an ETF first' });
      return;
    }

    if (quantity <= 0) {
      setMessage({ type: 'error', text: 'Quantity must be greater than 0' });
      return;
    }

    if (tradeAction === 'sell') {
      const position = positions.find(p => p.symbol === selectedEtf.symbol);
      if (!position || position.quantity < quantity) {
        setMessage({ type: 'error', text: 'Insufficient shares to sell' });
        return;
      }
    }

    try {
      const tradeRequest: TradeRequest = {
        symbol: selectedEtf.symbol,
        action: tradeAction,
        quantity,
        order_type: 'market',
        strategy: 'manual',
      };

      await tradeApi.execute(tradeRequest);
      setMessage({ type: 'success', text: `${tradeAction.toUpperCase()} order executed successfully` });
      loadData();
      setTimeout(() => setMessage(null), 3000);
    } catch (err: any) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Trade execution failed' });
    }
  };

  const filteredEtfs = etfs.filter(etf =>
    etf.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
    etf.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-800">ETF List</h2>
            <button
              onClick={loadData}
              className="p-2 hover:bg-gray-100 rounded-full transition"
              disabled={loading}
            >
              <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>

          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search ETFs by symbol or name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="space-y-2 max-h-96 overflow-y-auto">
            {filteredEtfs.map((etf) => (
              <div
                key={etf.symbol}
                onClick={() => setSelectedEtf(etf)}
                className={`p-4 rounded-lg cursor-pointer transition ${
                  selectedEtf?.symbol === etf.symbol
                    ? 'bg-blue-50 border-2 border-blue-500'
                    : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-lg text-gray-800">{etf.symbol}</span>
                      {etf.daily_change_percent > 0 ? (
                        <ArrowUpRight className="w-4 h-4 text-green-500" />
                      ) : (
                        <ArrowDownRight className="w-4 h-4 text-red-500" />
                      )}
                    </div>
                    <div className="text-sm text-gray-500">{etf.name}</div>
                    <div className="text-xs text-gray-400 mt-1">
                      Vol: {etf.volume.toLocaleString()} | PE: {etf.pe_ratio?.toFixed(2) || 'N/A'}
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-bold text-gray-800">${etf.current_price.toFixed(2)}</div>
                    <div className={`text-sm ${etf.daily_change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {etf.daily_change_percent >= 0 ? '+' : ''}{etf.daily_change_percent.toFixed(2)}%
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Trade Panel</h2>

            {selectedEtf ? (
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 rounded-lg">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-800">{selectedEtf.symbol}</div>
                    <div className="text-3xl font-bold text-blue-600 mt-2">${selectedEtf.current_price.toFixed(2)}</div>
                    <div className={`text-sm mt-1 ${selectedEtf.daily_change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                      {selectedEtf.daily_change_percent >= 0 ? '+' : ''}{selectedEtf.daily_change.toFixed(2)} ({selectedEtf.daily_change_percent.toFixed(2)}%)
                    </div>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Action</label>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => setTradeAction('buy')}
                      className={`py-3 px-4 rounded-lg font-semibold transition ${
                        tradeAction === 'buy'
                          ? 'bg-green-500 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      BUY
                    </button>
                    <button
                      onClick={() => setTradeAction('sell')}
                      className={`py-3 px-4 rounded-lg font-semibold transition ${
                        tradeAction === 'sell'
                          ? 'bg-red-500 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      SELL
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Quantity (Shares)</label>
                  <input
                    type="number"
                    min="1"
                    value={quantity}
                    onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 0))}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                <div className="p-4 bg-gray-50 rounded-lg space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Estimated Cost:</span>
                    <span className="font-semibold text-gray-800">
                      ${(selectedEtf.current_price * quantity).toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Commission:</span>
                    <span className="font-semibold text-gray-800">$1.00</span>
                  </div>
                  <div className="flex justify-between text-sm border-t pt-2">
                    <span className="text-gray-800 font-semibold">Total:</span>
                    <span className="font-bold text-lg text-blue-600">
                      ${(selectedEtf.current_price * quantity + 1).toFixed(2)}
                    </span>
                  </div>
                </div>

                <button
                  onClick={handleTrade}
                  disabled={loading}
                  className={`w-full py-3 rounded-lg font-semibold text-white transition ${
                    tradeAction === 'buy'
                      ? 'bg-green-500 hover:bg-green-600'
                      : 'bg-red-500 hover:bg-red-600'
                  } disabled:opacity-50`}
                >
                  {loading ? 'Executing...' : `${tradeAction.toUpperCase()} ${quantity} Shares`}
                </button>

                {message && (
                  <div className={`p-3 rounded-lg text-sm ${
                    message.type === 'success' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {message.text}
                  </div>
                )}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                Select an ETF to trade
              </div>
            )}
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-gray-800">Your Positions</h2>
            {positions.length > 0 ? (
              <div className="space-y-2">
                {positions.map((pos) => (
                  <div key={pos.symbol} className="p-3 bg-gray-50 rounded-lg">
                    <div className="flex justify-between items-center">
                      <div>
                        <div className="font-semibold text-gray-800">{pos.symbol}</div>
                        <div className="text-sm text-gray-500">{pos.quantity} shares @ ${pos.avg_cost.toFixed(2)}</div>
                      </div>
                      <div className="text-right">
                        <div className={`font-semibold ${pos.unrealized_pnl >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                          {pos.unrealized_pnl >= 0 ? '+' : ''}${pos.unrealized_pnl.toFixed(2)}
                        </div>
                        <div className={`text-xs ${pos.unrealized_pnl_percent >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                          {pos.unrealized_pnl_percent >= 0 ? '+' : ''}{pos.unrealized_pnl_percent.toFixed(2)}%
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-gray-500">
                No open positions
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Trading;
