from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from utils.api_clients import APIClient
from utils.config import settings

# Initialize news API client
news_client = APIClient(
    base_url="https://newsapi.org/v2",
    default_headers={"Content-Type": "application/json"},
)

# Create MCP server
mcp = FastMCP(name="news-server", stateless_http=True)


@mcp.tool()
async def get_top_headlines(
    country: str = "us", category: Optional[str] = None, page_size: int = 10
) -> dict:
    """
    Get top news headlines.

    Args:
        country: Country code (e.g., 'us', 'gb', 'ca')
        category: News category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
        page_size: Number of articles to return (max 100)
    """
    api_key = settings.news_api_key
    if not api_key:
        raise ValueError("News API key not configured")

    params = {"apiKey": api_key, "country": country, "pageSize": min(page_size, 100)}

    if category:
        params["category"] = category

    try:
        data = await news_client.get("/top-headlines", params=params)
        articles = []

        for article in data["articles"]:
            articles.append(
                {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "source": article["source"]["name"],
                    "author": article.get("author"),
                    "published_at": article["publishedAt"],
                    "url_to_image": article.get("urlToImage"),
                }
            )

        return {
            "total_results": data["totalResults"],
            "articles": articles,
            "country": country,
            "category": category,
        }
    except Exception as e:
        raise Exception(f"Failed to get top headlines: {str(e)}")


@mcp.tool()
async def search_news(
    query: str, sort_by: str = "publishedAt", language: str = "en", page_size: int = 10
) -> dict:
    """
    Search for news articles by keyword.

    Args:
        query: Search query/keywords
        sort_by: Sort articles by ('relevancy', 'popularity', 'publishedAt')
        language: Language code (e.g., 'en', 'es', 'fr')
        page_size: Number of articles to return (max 100)
    """
    api_key = settings.news_api_key
    if not api_key:
        raise ValueError("News API key not configured")

    params = {
        "apiKey": api_key,
        "q": query,
        "sortBy": sort_by,
        "language": language,
        "pageSize": min(page_size, 100),
    }

    try:
        data = await news_client.get("/everything", params=params)
        articles = []

        for article in data["articles"]:
            articles.append(
                {
                    "title": article["title"],
                    "description": article["description"],
                    "url": article["url"],
                    "source": article["source"]["name"],
                    "author": article.get("author"),
                    "published_at": article["publishedAt"],
                    "url_to_image": article.get("urlToImage"),
                }
            )

        return {
            "total_results": data["totalResults"],
            "articles": articles,
            "query": query,
            "sort_by": sort_by,
            "language": language,
        }
    except Exception as e:
        raise Exception(f"Failed to search news: {str(e)}")


@mcp.tool()
async def get_news_by_category(
    category: str, country: str = "us", page_size: int = 10
) -> dict:
    """
    Get news articles by specific category.

    Args:
        category: News category ('business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology')
        country: Country code (e.g., 'us', 'gb', 'ca')
        page_size: Number of articles to return (max 100)
    """
    valid_categories = [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
    ]
    if category not in valid_categories:
        raise ValueError(
            f"Invalid category. Must be one of: {', '.join(valid_categories)}"
        )

    return await get_top_headlines(
        country=country, category=category, page_size=page_size
    )
