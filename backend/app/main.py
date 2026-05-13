"""FastAPI application main entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import etf, trades, analysis, news, auth, funds
from .auth import create_database
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Global Fund Trading Platform",
    description="AI-powered fund trading and analysis platform with exchange and offline funds",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(funds.router)
app.include_router(etf.router)
app.include_router(trades.router)
app.include_router(analysis.router)
app.include_router(news.router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    create_database()
    logger.info("Database initialized")

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Global Fund Trading Platform",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "auth": "/api/auth",
            "funds": "/api/funds",
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
