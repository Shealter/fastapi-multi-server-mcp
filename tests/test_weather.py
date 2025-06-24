import pytest
from unittest.mock import AsyncMock, patch
from servers.weather import (
    get_current_weather,
    get_weather_forecast,
    get_weather_by_coordinates
)


@pytest.mark.asyncio
async def test_get_current_weather():
    mock_response = {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 15.5, "feels_like": 14.2, "humidity": 78, "pressure": 1013},
        "weather": [{"description": "overcast clouds"}],
        "wind": {"speed": 3.2},
        "visibility": 10000,
    }

    with patch(
        "servers.weather.weather_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_current_weather("London", "GB")

        assert result["city"] == "London"
        assert result["country"] == "GB"
        assert result["temperature"] == 15.5
        assert result["description"] == "overcast clouds"


@pytest.mark.asyncio
async def test_get_weather_forecast():
    mock_response = {
        "city": {"name": "London", "country": "GB"},
        "list": [
            {
                "dt_txt": "2024-01-01 12:00:00",
                "main": {"temp": 15.5, "humidity": 78},
                "weather": [{"description": "clear sky"}],
                "wind": {"speed": 3.2},
            }
        ],
    }

    with patch(
        "servers.weather.weather_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_weather_forecast("London", 1)

        assert result["city"] == "London"
        assert len(result["forecasts"]) == 1
        assert result["forecasts"][0]["temperature"] == 15.5

@pytest.mark.asyncio
async def test_get_weather_by_coordinates():
    mock_response = {
        "name": "London",
        "sys": {"country": "GB"},
        "main": {"temp": 15.5, "feels_like": 14.2, "humidity": 78, "pressure": 1013},
        "weather": [{"description": "overcast clouds"}],
        "wind": {"speed": 3.2},
        "visibility": 10000,
    }

    with patch(
        "servers.weather.weather_client.get", new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = mock_response

        result = await get_weather_by_coordinates(51.5074, -0.1278)

        assert result["city"] == "London"
        assert result["country"] == "GB"
        assert result["temperature"] == 15.5
        assert result["description"] == "overcast clouds"