import random
from typing import List, Optional
from mcp.server.fastmcp import FastMCP
from utils.api_clients import APIClient, retry_on_failure

# Initialize quote API clients
quote_client = APIClient(
    base_url="https://api.quotable.io",
    default_headers={"Content-Type": "application/json"},
)

fact_client = APIClient(
    base_url="https://uselessfacts.jsph.pl",
    default_headers={"Content-Type": "application/json"},
)

# Create MCP server
mcp = FastMCP(name="quote-server", stateless_http=True)


@mcp.tool()
async def get_random_quote(
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    tags: Optional[str] = None,
) -> dict:
    """
    Get a random inspirational quote.

    Args:
        min_length: Minimum quote length
        max_length: Maximum quote length
        tags: Comma-separated tags to filter quotes (e.g., 'motivational,success')
    """
    params = {}

    if min_length:
        params["minLength"] = min_length
    if max_length:
        params["maxLength"] = max_length
    if tags:
        params["tags"] = tags

    try:
        data = await quote_client.get("/random", params=params)

        return {
            "quote": data["content"],
            "author": data["author"],
            "length": data["length"],
            "tags": data["tags"],
        }
    except Exception as e:
        raise Exception(f"Failed to get random quote: {str(e)}")


@mcp.tool()
async def get_quote_by_category(category: str, limit: int = 10) -> dict:
    """
    Get quotes by specific category/tag.

    Args:
        category: Category/tag name (e.g., 'motivational', 'wisdom', 'success')
        limit: Number of quotes to return (max 50)
    """
    params = {"tags": category, "limit": min(limit, 50)}

    try:
        data = await quote_client.get("/quotes", params=params)

        quotes = []
        for quote in data["results"]:
            quotes.append(
                {
                    "quote": quote["content"],
                    "author": quote["author"],
                    "length": quote["length"],
                    "tags": quote["tags"],
                }
            )

        return {
            "category": category,
            "total_quotes": data["totalCount"],
            "quotes": quotes,
        }
    except Exception as e:
        raise Exception(f"Failed to get quotes by category: {str(e)}")


@mcp.tool()
async def get_quote_by_author(author: str, limit: int = 10) -> dict:
    """
    Get quotes by a specific author.

    Args:
        author: Author name
        limit: Number of quotes to return (max 50)
    """
    params = {"author": author, "limit": min(limit, 50)}

    try:
        data = await quote_client.get("/quotes", params=params)

        quotes = []
        for quote in data["results"]:
            quotes.append(
                {
                    "quote": quote["content"],
                    "author": quote["author"],
                    "length": quote["length"],
                    "tags": quote["tags"],
                }
            )

        return {"author": author, "total_quotes": data["totalCount"], "quotes": quotes}
    except Exception as e:
        raise Exception(f"Failed to get quotes by author: {str(e)}")


@mcp.tool()
async def get_random_fact() -> dict:
    """
    Get a random interesting fact.
    """
    try:
        data = await fact_client.get("/api/v2/facts/random")

        return {
            "fact": data["text"],
            "source": data.get("source", "Unknown"),
            "language": "en",
        }
    except Exception as e:
        raise Exception(f"Failed to get random fact: {str(e)}")


@mcp.tool()
async def get_quote_categories() -> dict:
    """
    Get available quote categories/tags.
    """
    try:
        data = await quote_client.get("/tags")

        categories = []
        for tag in data:
            categories.append({"name": tag["name"], "quote_count": tag["quoteCount"]})

        return {
            "total_categories": len(categories),
            "categories": sorted(
                categories, key=lambda x: x["quote_count"], reverse=True
            ),
        }
    except Exception as e:
        raise Exception(f"Failed to get quote categories: {str(e)}")


@mcp.tool()
async def search_quotes(query: str, limit: int = 10) -> dict:
    """
    Search for quotes containing specific keywords.

    Args:
        query: Search query/keywords
        limit: Number of quotes to return (max 50)
    """
    params = {"query": query, "limit": min(limit, 50)}

    try:
        data = await quote_client.get("/search/quotes", params=params)

        quotes = []
        for quote in data["results"]:
            quotes.append(
                {
                    "quote": quote["content"],
                    "author": quote["author"],
                    "length": quote["length"],
                    "tags": quote["tags"],
                }
            )

        return {"query": query, "total_results": data["totalCount"], "quotes": quotes}
    except Exception as e:
        raise Exception(f"Failed to search quotes: {str(e)}")
