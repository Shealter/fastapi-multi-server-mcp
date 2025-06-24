from typing import Optional
from mcp.server.fastmcp import FastMCP
from utils.api_clients import APIClient
from utils.config import settings

# Initialize weather API client
weather_client = APIClient(
    base_url="https://api.openweathermap.org/data/2.5",
    default_headers={"Content-Type": "application/json"},
)

# Create MCP server
mcp = FastMCP(name="weather-server", stateless_http=True)


@mcp.tool()
async def get_current_weather(
    city: str, country_code: Optional[str] = None, units: str = "metric"
) -> dict:
    """
    Get current weather for a specific city.

    Args:
        city: Name of the city
        country_code: Optional ISO 3166 country code (e.g., 'US', 'GB')
        units: Temperature units ('metric', 'imperial', 'kelvin')
    """
    api_key = settings.openweather_api_key
    if not api_key:
        raise ValueError("OpenWeatherMap API key not configured")

    location = f"{city},{country_code}" if country_code else city
    params = {"q": location, "appid": api_key, "units": units}

    try:
        data = await weather_client.get("/weather", params=params)
        return {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", "N/A"),
            "units": units,
        }
    except Exception as e:
        raise Exception(f"Failed to get weather data: {str(e)}")


@mcp.tool()
async def get_weather_forecast(
    city: str, days: int = 5, country_code: Optional[str] = None, units: str = "metric"
) -> dict:
    """
    Get weather forecast for a specific city.

    Args:
        city: Name of the city
        days: Number of days for forecast (1-5)
        country_code: Optional ISO 3166 country code
        units: Temperature units ('metric', 'imperial', 'kelvin')
    """
    api_key = settings.openweather_api_key
    if not api_key:
        raise ValueError("OpenWeatherMap API key not configured")

    location = f"{city},{country_code}" if country_code else city
    params = {
        "q": location,
        "appid": api_key,
        "units": units,
        "cnt": days * 8,  # 8 forecasts per day (3-hour intervals)
    }

    try:
        data = await weather_client.get("/forecast", params=params)
        forecasts = []

        for item in data["list"][: days * 8]:
            forecasts.append(
                {
                    "datetime": item["dt_txt"],
                    "temperature": item["main"]["temp"],
                    "description": item["weather"][0]["description"],
                    "humidity": item["main"]["humidity"],
                    "wind_speed": item["wind"]["speed"],
                }
            )

        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecasts": forecasts,
            "units": units,
        }
    except Exception as e:
        raise Exception(f"Failed to get weather forecast: {str(e)}")


@mcp.tool()
async def get_weather_by_coordinates(
    lat: float, lon: float, units: str = "metric"
) -> dict:
    """
    Get current weather by geographical coordinates.

    Args:
        lat: Latitude
        lon: Longitude
        units: Temperature units ('metric', 'imperial', 'kelvin')
    """
    api_key = settings.openweather_api_key
    if not api_key:
        raise ValueError("OpenWeatherMap API key not configured")

    params = {"lat": lat, "lon": lon, "appid": api_key, "units": units}

    try:
        data = await weather_client.get("/weather", params=params)
        return {
            "location": f"{data['name']}, {data['sys']['country']}",
            "coordinates": {"lat": lat, "lon": lon},
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
            "units": units,
        }
    except Exception as e:
        raise Exception(f"Failed to get weather by coordinates: {str(e)}")
