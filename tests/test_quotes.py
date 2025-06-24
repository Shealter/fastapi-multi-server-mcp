import pytest
from unittest.mock import AsyncMock, patch
from servers.quote import get_random_quote, get_random_fact


@pytest.mark.asyncio
async def test_get_random_quote():
    mock_response = {
        "content": "The only way to do great work is to love what you do.",
        "author": "Steve Jobs",
        "length": 52,
        "tags": ["motivational", "work"],
    }

    with patch(
        "servers.quote.quote_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_random_quote()

        assert (
            result["quote"] == "The only way to do great work is to love what you do."
        )
        assert result["author"] == "Steve Jobs"
        assert result["length"] == 52


@pytest.mark.asyncio
async def test_get_random_fact():
    mock_response = {
        "text": "Bananas are berries, but strawberries are not.",
        "source": "Science Facts",
        "language": "en",
    }

    with patch(
        "servers.quote.fact_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_random_fact()

        assert "Bananas are berries" in result["fact"]
        assert result["language"] == "en"
