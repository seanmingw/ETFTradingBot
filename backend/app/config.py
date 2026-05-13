"""Configuration settings for the ETF trading bot."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

    DATABASE_URL = os.getenv('DATABASE_URL', f'sqlite:///{BASE_DIR}/etf_trading.db')

    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    ALPACA_API_KEY = os.getenv('ALPACA_API_KEY', '')
    ALPACA_API_SECRET = os.getenv('ALPACA_API_SECRET', '')
    ALPACA_BASE_URL = os.getenv('ALPACA_BASE_URL', 'https://paper-api.alpaca.markets')

    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')

    AI_MODEL_PATH = os.getenv('AI_MODEL_PATH', f'{BASE_DIR}/models/ai')

    CACHE_TTL = 300
    PRICE_UPDATE_INTERVAL = 60
    NEWS_UPDATE_INTERVAL = 900

    MAX_POSITION_SIZE = 0.2
    MAX_DAILY_TRADES = 10
    MAX_PORTFOLIO_EXPOSURE = 0.8

    STOP_LOSS_PERCENT = 0.03
    TAKE_PROFIT_PERCENT = 0.08
    MAX_DAILY_LOSS = 0.05
    MAX_PORTFOLIO_DRAWDOWN = 0.15

    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = BASE_DIR / 'logs' / 'app.log'

    class Config:
        SCHEDULER_API_ENABLED = True
