import pytest
from unittest.mock import AsyncMock, patch
from servers.news import get_top_headlines, search_news


@pytest.mark.asyncio
async def test_get_top_headlines():
    mock_response = {
        "totalResults": 1,
        "articles": [
            {
                "title": "Test News",
                "description": "Test Description",
                "url": "https://example.com",
                "source": {"name": "Test Source"},
                "author": "Test Author",
                "publishedAt": "2024-01-01T12:00:00Z",
                "urlToImage": "https://example.com/image.jpg",
            }
        ],
    }

    with patch(
        "servers.news.news_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_top_headlines("us")

        assert result["total_results"] == 1
        assert len(result["articles"]) == 1
        assert result["articles"][0]["title"] == "Test News"


@pytest.mark.asyncio
async def test_search_news():
    mock_response = {
        "totalResults": 1,
        "articles": [
            {
                "title": "Search Result",
                "description": "Search Description",
                "url": "https://example.com",
                "source": {"name": "Search Source"},
                "author": "Search Author",
                "publishedAt": "2024-01-01T12:00:00Z",
                "urlToImage": "https://example.com/image.jpg",
            }
        ],
    }

    with patch(
        "servers.news.news_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await search_news("test query")

        assert result["total_results"] == 1
        assert result["query"] == "test query"
        assert len(result["articles"]) == 1
