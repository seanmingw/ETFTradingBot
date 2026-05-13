"""FastAPI application main entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import etf, trades, analysis, news
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Global ETF Trading Bot",
    description="AI-powered ETF trading and analysis platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(etf.router)
app.include_router(trades.router)
app.include_router(analysis.router)
app.include_router(news.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Global ETF Trading Bot",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "etf": "/api/etf",
            "trades": "/api/trades",
            "analysis": "/api/analysis",
            "news": "/api/news"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

logger.info("ETF Trading Bot API started")
