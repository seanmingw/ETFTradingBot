"""News service for fetching and analyzing financial news."""
from typing import List, Optional, Dict
import logging
from datetime import datetime, timedelta
import requests
import random

logger = logging.getLogger(__name__)

class NewsService:
    """Service for fetching and analyzing financial news."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def get_news_for_symbol(self, symbol: str, limit: int = 20) -> List[Dict]:
        """Get news articles for a specific ETF symbol."""
        try:
            mock_news = self._generate_mock_news(symbol, limit)
            return mock_news
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []

    def analyze_sentiment(self, news_items: List[Dict]) -> Dict:
        """Analyze sentiment of news articles."""
        if not news_items:
            return {
                'overall_sentiment': 'NEUTRAL',
                'sentiment_score': 0.0,
                'bullish_count': 0,
                'bearish_count': 0,
                'neutral_count': 0,
                'average_score': 0.0
            }

        sentiments = []
        for news in news_items:
            sentiment = self._analyze_single_article(news)
            sentiments.append(sentiment)

        bullish = sum(1 for s in sentiments if s['label'] == 'BULLISH')
        bearish = sum(1 for s in sentiments if s['label'] == 'BEARISH')
        neutral = sum(1 for s in sentiments if s['label'] == 'NEUTRAL')
        avg_score = sum(s['score'] for s in sentiments) / len(sentiments)

        overall = 'BULLISH' if avg_score > 0.2 else 'BEARISH' if avg_score < -0.2 else 'NEUTRAL'

        return {
            'overall_sentiment': overall,
            'sentiment_score': round(avg_score, 3),
            'bullish_count': bullish,
            'bearish_count': bearish,
            'neutral_count': neutral,
            'average_score': round(avg_score, 3)
        }

    def _analyze_single_article(self, article: Dict) -> Dict:
        """Analyze sentiment of a single article."""
        title = article.get('title', '').lower()
        content = article.get('content', '').lower()

        bullish_keywords = [
            'surge', 'rally', 'gain', 'rise', 'climb', 'soar', 'jump', 'boost',
            'strong', 'growth', 'profit', 'beat', 'exceed', 'optimistic', 'bullish',
            'upgrade', 'buy', 'outperform', 'positive', 'recovery'
        ]

        bearish_keywords = [
            'fall', 'drop', 'decline', 'plunge', 'tumble', 'sink', 'crash', 'loss',
            'weak', 'concern', 'risk', 'miss', 'warn', 'pessimistic', 'bearish',
            'downgrade', 'sell', 'underperform', 'negative', 'recession'
        ]

        bullish_count = sum(1 for kw in bullish_keywords if kw in title or kw in content)
        bearish_count = sum(1 for kw in bearish_keywords if kw in title or kw in content)

        score = (bullish_count - bearish_count) / max(bullish_count + bearish_count, 1)

        if score > 0.2:
            label = 'BULLISH'
        elif score < -0.2:
            label = 'BEARISH'
        else:
            label = 'NEUTRAL'

        return {
            'label': label,
            'score': score,
            'confidence': abs(score)
        }

    def _generate_mock_news(self, symbol: str, limit: int) -> List[Dict]:
        """Generate mock news data for demonstration."""
        news_templates = [
            {
                'title': f'{symbol} Shows Strong Performance Amid Market Rally',
                'content': f'{symbol} has demonstrated robust performance as markets continue their upward trajectory. Analysts point to favorable economic indicators.',
                'sentiment': 'BULLISH'
            },
            {
                'title': f'{symbol} Faces Headwinds as Sector Struggles',
                'content': f'{symbol} experiences pressure as its respective sector navigates challenging market conditions.',
                'sentiment': 'BEARISH'
            },
            {
                'title': f'{symbol} Trading Volume Spikes Amid Options Activity',
                'content': f'Unusual options activity detected in {symbol}, suggesting major institutional moves may be underway.',
                'sentiment': 'NEUTRAL'
            },
            {
                'title': f'Fed Policy Update: Impact on {symbol}',
                'content': f'The latest Federal Reserve policy announcements could influence {symbol} performance in the coming months.',
                'sentiment': 'NEUTRAL'
            },
            {
                'title': f'{symbol} ETF Sees Record Inflows as Investors Seek Safety',
                'content': f'Investors poured record amounts into {symbol} as market uncertainty drives demand for defensive positions.',
                'sentiment': 'BULLISH'
            },
            {
                'title': f'Q2 Earnings Preview: What to Expect from {symbol}',
                'content': f' analysts expect {symbol} to show resilient performance driven by underlying holdings strength.',
                'sentiment': 'BULLISH'
            },
            {
                'title': f'{symbol} Technical Analysis Shows Key Support Level',
                'content': f'Chart analysts identify critical support levels for {symbol} as momentum indicators suggest potential rebound.',
                'sentiment': 'NEUTRAL'
            },
            {
                'title': f'Global Market Rally Lifts {symbol} to New Highs',
                'content': f'{symbol} reaches new 52-week highs as global markets rally on positive economic data.',
                'sentiment': 'BULLISH'
            },
            {
                'title': f'{symbol} Announces Rebalancing: Key Changes Ahead',
                'content': f'{symbol} fund managers announce portfolio rebalancing that could impact sector allocations.',
                'sentiment': 'NEUTRAL'
            },
            {
                'title': f'Volatility Returns: {symbol} Navigates Market Uncertainty',
                'content': f'Increased market volatility creates trading opportunities in {symbol} for active investors.',
                'sentiment': 'NEUTRAL'
            }
        ]

        news = []
        for i in range(min(limit, len(news_templates))):
            template = news_templates[i % len(news_templates)]
            days_ago = random.randint(0, 7)
            hours_ago = random.randint(0, 23)

            news.append({
                'id': i + 1,
                'symbol': symbol,
                'title': template['title'],
                'content': template['content'],
                'source': random.choice(['Yahoo Finance', 'Reuters', 'Bloomberg', 'CNBC', 'MarketWatch']),
                'url': f'https://example.com/news/{symbol.lower()}-{i+1}',
                'sentiment': template['sentiment'],
                'published_at': (datetime.now() - timedelta(days=days_ago, hours=hours_ago)).isoformat()
            })

        return news

    def get_market_overview(self) -> Dict:
        """Get overall market news and sentiment."""
        return {
            'date': datetime.now().isoformat(),
            'major_indices': {
                'SPY': self._get_mock_index_data('SPY'),
                'QQQ': self._get_mock_index_data('QQQ'),
                'IWM': self._get_mock_index_data('IWM')
            },
            'market_sentiment': random.choice(['RISK_ON', 'RISK_OFF', 'NEUTRAL']),
            'fear_greed_index': random.randint(20, 80)
        }

    def _get_mock_index_data(self, symbol: str) -> Dict:
        """Generate mock index data."""
        change = random.uniform(-2, 2)
        return {
            'symbol': symbol,
            'change_percent': round(change, 2),
            'sentiment': 'POSITIVE' if change > 0.5 else 'NEGATIVE' if change < -0.5 else 'NEUTRAL'
        }

    def get_related_news(self, symbol: str, related_symbols: List[str]) -> Dict:
        """Get news for symbol and related symbols."""
        all_news = self.get_news_for_symbol(symbol, limit=10)

        for related in related_symbols[:3]:
            related_news = self.get_news_for_symbol(related, limit=5)
            all_news.extend(related_news)

        all_news.sort(key=lambda x: x.get('published_at', ''), reverse=True)

        return {
            'symbol': symbol,
            'related_symbols': related_symbols[:3],
            'news': all_news[:20],
            'sentiment_summary': self.analyze_sentiment(all_news)
        }
