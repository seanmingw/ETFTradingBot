"""Technical indicators calculation utilities."""
import numpy as np
from typing import List, Tuple

def calculate_sma(prices: List[float], period: int) -> List[float]:
    """Calculate Simple Moving Average."""
    if len(prices) < period:
        return []
    sma = []
    for i in range(period - 1, len(prices)):
        sma.append(sum(prices[i - period + 1:i + 1]) / period)
    return sma

def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Calculate Exponential Moving Average."""
    if len(prices) < period:
        return []

    ema = [sum(prices[:period]) / period]
    multiplier = 2 / (period + 1)

    for price in prices[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])

    return ema

def calculate_rsi(prices: List[float], period: int = 14) -> List[float]:
    """Calculate Relative Strength Index."""
    if len(prices) < period + 1:
        return []

    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    rsi_values = []
    if avg_loss == 0:
        rsi_values.append(100)
    else:
        rs = avg_gain / avg_loss
        rsi_values.append(100 - (100 / (1 + rs)))

    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period

        if avg_loss == 0:
            rsi_values.append(100)
        else:
            rs = avg_gain / avg_loss
            rsi_values.append(100 - (100 / (1 + rs)))

    return rsi_values

def calculate_macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[List[float], List[float], List[float]]:
    """Calculate MACD (Moving Average Convergence Divergence)."""
    if len(prices) < slow:
        return [], [], []

    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)

    macd_line = [fast_ema - slow_ema for fast_ema, slow_ema in zip(ema_fast[-len(ema_slow):], ema_slow)]

    signal_line = calculate_ema(macd_line, signal)

    histogram = []
    if len(signal_line) > 0 and len(macd_line) >= len(signal_line):
        start_idx = len(macd_line) - len(signal_line)
        histogram = [macd_line[start_idx + i] - signal_line[i] for i in range(len(signal_line))]

    return macd_line, signal_line, histogram

def calculate_bollinger_bands(prices: List[float], period: int = 20, num_std: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
    """Calculate Bollinger Bands."""
    if len(prices) < period:
        return [], [], []

    sma = calculate_sma(prices, period)
    upper = []
    lower = []

    for i in range(period - 1, len(prices)):
        window = prices[i - period + 1:i + 1]
        std = np.std(window)
        sma_idx = i - period + 1
        if sma_idx < len(sma):
            upper.append(sma[sma_idx] + num_std * std)
            lower.append(sma[sma_idx] - num_std * std)

    return upper, sma, lower

def calculate_vwap(high: List[float], low: List[float], close: List[float], volume: List[int]) -> List[float]:
    """Calculate Volume Weighted Average Price."""
    if len(high) != len(low) != len(close) != len(volume):
        return []

    typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    cumulative_tp_vol = []
    cumulative_vol = []

    running_tp_vol = 0
    running_vol = 0

    for tp, vol in zip(typical_price, volume):
        running_tp_vol += tp * vol
        running_vol += vol
        cumulative_tp_vol.append(running_tp_vol)
        cumulative_vol.append(running_vol)

    vwap = [tp_vol / vol if vol > 0 else 0 for tp_vol, vol in zip(cumulative_tp_vol, cumulative_vol)]
    return vwap

def calculate_atr(high: List[float], low: List[float], close: List[float], period: int = 14) -> List[float]:
    """Calculate Average True Range."""
    if len(high) < 2 or len(low) < 2 or len(close) < 2:
        return []

    true_range = []
    for i in range(1, len(high)):
        tr1 = high[i] - low[i]
        tr2 = abs(high[i] - close[i - 1])
        tr3 = abs(low[i] - close[i - 1])
        true_range.append(max(tr1, tr2, tr3))

    if len(true_range) < period:
        return []

    atr = [sum(true_range[:period]) / period]
    for i in range(period, len(true_range)):
        atr.append((atr[-1] * (period - 1) + true_range[i]) / period)

    return atr

def calculate_stochastic(high: List[float], low: List[float], close: List[float], period: int = 14) -> Tuple[List[float], List[float]]:
    """Calculate Stochastic Oscillator (%K and %D)."""
    if len(high) < period or len(low) < period or len(close) < period:
        return [], []

    k_values = []
    for i in range(period - 1, len(close)):
        window_high = max(high[i - period + 1:i + 1])
        window_low = min(low[i - period + 1:i + 1])
        if window_high != window_low:
            k = ((close[i] - window_low) / (window_high - window_low)) * 100
        else:
            k = 50
        k_values.append(k)

    d_values = calculate_sma(k_values, 3)

    return k_values, d_values
