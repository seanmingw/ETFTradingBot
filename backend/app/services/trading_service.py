"""Trading service for executing and managing trades."""
from typing import List, Optional, Dict
from datetime import datetime
import logging
from ..models.trade import (
    TradeRequest, TradeResponse, Position, PortfolioSummary,
    TradingSignal, StrategyConfig
)
from ..utils.market_data import MarketDataProvider

logger = logging.getLogger(__name__)

class TradingService:
    """Service for managing trades and positions."""

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.market_data = MarketDataProvider()
        self.positions: Dict[str, Position] = {}
        self.trades: List[TradeResponse] = []
        self.cash = 100000.0
        self.strategy_config = StrategyConfig(name="default")

    def execute_trade(self, trade_request: TradeRequest) -> TradeResponse:
        """Execute a trade order."""
        try:
            symbol = trade_request.symbol.upper()
            quantity = trade_request.quantity
            action = trade_request.action

            current_price_data = self.market_data.get_realtime_price(symbol)
            if not current_price_data:
                raise ValueError(f"Unable to fetch price for {symbol}")

            current_price = current_price_data['price']

            if trade_request.order_type == 'limit' and trade_request.limit_price:
                if action == 'buy' and current_price > trade_request.limit_price:
                    raise ValueError(f"Current price {current_price} above limit price {trade_request.limit_price}")
                if action == 'sell' and current_price < trade_request.limit_price:
                    raise ValueError(f"Current price {current_price} below limit price {trade_request.limit_price}")
                current_price = trade_request.limit_price

            total_cost = current_price * quantity
            commission = max(0.0, 1.0)

            if action == 'buy':
                if total_cost + commission > self.cash:
                    raise ValueError(f"Insufficient funds. Required: ${total_cost + commission:.2f}, Available: ${self.cash:.2f}")

                position = self.positions.get(symbol)
                if position:
                    new_quantity = position.quantity + quantity
                    new_avg_cost = (position.avg_cost * position.quantity + current_price * quantity) / new_quantity
                    self.positions[symbol] = Position(
                        id=position.id,
                        symbol=symbol,
                        quantity=new_quantity,
                        avg_cost=new_avg_cost,
                        current_price=current_price,
                        market_value=current_price * new_quantity,
                        unrealized_pnl=(current_price - new_avg_cost) * new_quantity,
                        unrealized_pnl_percent=((current_price - new_avg_cost) / new_avg_cost * 100),
                        updated_at=datetime.now()
                    )
                else:
                    self.positions[symbol] = Position(
                        id=len(self.positions) + 1,
                        symbol=symbol,
                        quantity=quantity,
                        avg_cost=current_price,
                        current_price=current_price,
                        market_value=current_price * quantity,
                        unrealized_pnl=0.0,
                        unrealized_pnl_percent=0.0,
                        updated_at=datetime.now()
                    )

                self.cash -= (total_cost + commission)
            else:
                if symbol not in self.positions:
                    raise ValueError(f"No position found for {symbol}")

                position = self.positions[symbol]
                if position.quantity < quantity:
                    raise ValueError(f"Insufficient shares. Available: {position.quantity}, Requested: {quantity}")

                pnl = (current_price - position.avg_cost) * quantity
                self.cash += (total_cost - commission)

                if position.quantity == quantity:
                    del self.positions[symbol]
                else:
                    self.positions[symbol] = Position(
                        id=position.id,
                        symbol=symbol,
                        quantity=position.quantity - quantity,
                        avg_cost=position.avg_cost,
                        current_price=current_price,
                        market_value=current_price * (position.quantity - quantity),
                        unrealized_pnl=(current_price - position.avg_cost) * (position.quantity - quantity),
                        unrealized_pnl_percent=((current_price - position.avg_cost) / position.avg_cost * 100),
                        updated_at=datetime.now()
                    )

            trade = TradeResponse(
                id=len(self.trades) + 1,
                symbol=symbol,
                action=action,
                quantity=quantity,
                price=current_price,
                commission=commission,
                total_amount=total_cost,
                strategy=trade_request.strategy,
                status='FILLED',
                created_at=datetime.now()
            )
            self.trades.append(trade)

            return trade

        except Exception as e:
            logger.error(f"Error executing trade: {e}")
            raise

    def get_positions(self) -> List[Position]:
        """Get all current positions."""
        for symbol, position in self.positions.items():
            current_price_data = self.market_data.get_realtime_price(symbol)
            if current_price_data:
                current_price = current_price_data['price']
                position.current_price = current_price
                position.market_value = current_price * position.quantity
                position.unrealized_pnl = (current_price - position.avg_cost) * position.quantity
                position.unrealized_pnl_percent = ((current_price - position.avg_cost) / position.avg_cost * 100)
                position.updated_at = datetime.now()

        return list(self.positions.values())

    def get_portfolio_summary(self) -> PortfolioSummary:
        """Get portfolio summary with all positions."""
        positions = self.get_positions()

        total_value = sum(p.market_value for p in positions)
        total_cost = sum(p.avg_cost * p.quantity for p in positions)
        total_pnl = total_value - total_cost
        total_pnl_percent = (total_pnl / total_cost * 100) if total_cost > 0 else 0

        return PortfolioSummary(
            total_value=total_value + self.cash,
            total_cost=total_cost,
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_percent,
            day_pnl=0.0,
            day_pnl_percent=0.0,
            positions=positions,
            cash=self.cash,
            buying_power=self.cash * 2
        )

    def get_trades(self, limit: int = 50) -> List[TradeResponse]:
        """Get trade history."""
        return self.trades[-limit:]

    def generate_signals(self, symbols: List[str]) -> List[TradingSignal]:
        """Generate trading signals for given symbols."""
        signals = []

        for symbol in symbols:
            try:
                price_data = self.market_data.get_price_history(symbol, period='1mo')
                if not price_data or len(price_data['prices']) < 50:
                    continue

                closes = [p['close'] for p in price_data['prices']]

                ma_20 = sum(closes[-20:]) / 20
                ma_50 = sum(closes[-50:]) / 50 if len(closes) >= 50 else ma_20
                current_price = closes[-1]

                signal = self._determine_signal(symbol, current_price, ma_20, ma_50, closes)
                if signal:
                    signals.append(signal)

            except Exception as e:
                logger.error(f"Error generating signal for {symbol}: {e}")
                continue

        return signals

    def _determine_signal(self, symbol: str, current_price: float, ma_20: float, ma_50: float, closes: List[float]) -> Optional[TradingSignal]:
        """Determine trading signal based on technical analysis."""
        import numpy as np

        returns = np.diff(closes) / closes[:-1]
        volatility = np.std(returns[-20:]) * np.sqrt(252)

        if current_price > ma_20 > ma_50:
            confidence = min(95, 60 + (current_price / ma_20 - 1) * 1000)
            return TradingSignal(
                symbol=symbol,
                action='BUY',
                confidence=round(confidence, 2),
                strategy='TREND_FOLLOWING',
                reason='Bullish trend confirmed by price above moving averages',
                entry_price=current_price,
                stop_loss=round(current_price * (1 - 2 * volatility), 2),
                take_profit=round(current_price * (1 + 4 * volatility), 2),
                timestamp=datetime.now()
            )
        elif current_price < ma_20 < ma_50:
            confidence = min(95, 60 + (1 - current_price / ma_20) * 1000)
            return TradingSignal(
                symbol=symbol,
                action='SELL',
                confidence=round(confidence, 2),
                strategy='TREND_REVERSAL',
                reason='Bearish trend confirmed by price below moving averages',
                entry_price=current_price,
                stop_loss=round(current_price * (1 + 2 * volatility), 2),
                take_profit=round(current_price * (1 - 4 * volatility), 2),
                timestamp=datetime.now()
            )

        return None

    def cancel_trade(self, trade_id: int) -> bool:
        """Cancel a pending trade (if supported by broker)."""
        for i, trade in enumerate(self.trades):
            if trade.id == trade_id and trade.status == 'PENDING':
                self.trades[i].status = 'CANCELLED'
                return True
        return False
