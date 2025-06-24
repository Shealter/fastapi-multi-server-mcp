import pytest
from unittest.mock import AsyncMock, patch
from servers.currency import get_exchange_rates, convert_currency


@pytest.mark.asyncio
async def test_get_exchange_rates():
    mock_response = {
        "result": "success",
        "base_code": "USD",
        "time_last_update_utc": "2024-01-01T00:00:00Z",
        "time_next_update_utc": "2024-01-02T00:00:00Z",
        "conversion_rates": {"EUR": 0.85, "GBP": 0.75, "JPY": 110.0},
    }

    with patch(
        "servers.currency.currency_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_exchange_rates("USD")

        assert result["base_currency"] == "USD"
        assert "EUR" in result["exchange_rates"]
        assert result["exchange_rates"]["EUR"] == 0.85


@pytest.mark.asyncio
async def test_convert_currency():
    mock_response = {
        "result": "success",
        "base_code": "USD",
        "target_code": "EUR",
        "conversion_rate": 0.85,
        "conversion_result": 85.0,
        "time_last_update_utc": "2024-01-01T00:00:00Z",
    }

    with patch(
        "servers.currency.currency_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await convert_currency("USD", "EUR", 100)

        assert result["from_currency"] == "USD"
        assert result["to_currency"] == "EUR"
        assert result["original_amount"] == 100
        assert result["converted_amount"] == 85.0
