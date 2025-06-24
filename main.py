import contextlib
import os
from fastapi import FastAPI
from dotenv import load_dotenv

# Import all MCP servers
from servers.weather import mcp as weather_mcp
from servers.news import mcp as news_mcp
from servers.currency import mcp as currency_mcp
from servers.quotes import mcp as quote_mcp

# Load environment variables
load_dotenv()


# Create a combined lifespan to manage all session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        await stack.enter_async_context(weather_mcp.session_manager.run())
        await stack.enter_async_context(news_mcp.session_manager.run())
        await stack.enter_async_context(currency_mcp.session_manager.run())
        await stack.enter_async_context(quote_mcp.session_manager.run())
        yield


# Create FastAPI application
app = FastAPI(
    title="Multi-Server MCP Application",
    description="FastAPI application hosting multiple MCP servers for various public APIs",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount all MCP servers
app.mount("/weather", weather_mcp.streamable_http_app())
app.mount("/news", news_mcp.streamable_http_app())
app.mount("/currency", currency_mcp.streamable_http_app())
app.mount("/quotes", quote_mcp.streamable_http_app())


@app.get("/")
async def root():
    return {
        "message": "Multi-Server MCP Application",
        "servers": {
            "weather": "/weather - Weather data and forecasts",
            "news": "/news - Latest news and articles",
            "currency": "/currency - Exchange rates and conversion",
            "quotes": "/quotes - Inspirational quotes and facts",
        },
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "servers": 5}


# Configuration
PORT = int(os.environ.get("PORT", 10000))
HOST = os.environ.get("HOST", "0.0.0.0")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host=HOST, port=PORT, log_level=os.environ.get("LOG_LEVEL", "info")
    )
