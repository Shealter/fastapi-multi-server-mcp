from typing import List, Optional, Dict
from mcp.server.fastmcp import FastMCP
from utils.api_clients import APIClient
from utils.config import settings

# Initialize currency API client
currency_client = APIClient(
    base_url="https://v6.exchangerate-api.com/v6",
    default_headers={"Content-Type": "application/json"},
)

# Create MCP server
mcp = FastMCP(name="currency-server", stateless_http=True)


@mcp.tool()
async def get_exchange_rates(base_currency: str = "USD") -> dict:
    """
    Get current exchange rates for a base currency.

    Args:
        base_currency: Base currency code (e.g., 'USD', 'EUR', 'GBP')
    """
    api_key = settings.exchange_rates_api_key
    if not api_key:
        raise ValueError("Exchange Rates API key not configured")

    try:
        data = await currency_client.get(f"/{api_key}/latest/{base_currency.upper()}")

        if data["result"] == "success":
            return {
                "base_currency": data["base_code"],
                "last_updated": data["time_last_update_utc"],
                "next_update": data["time_next_update_utc"],
                "exchange_rates": data["conversion_rates"],
            }
        else:
            raise Exception(f"API Error: {data.get('error-type', 'Unknown error')}")

    except Exception as e:
        raise Exception(f"Failed to get exchange rates: {str(e)}")


@mcp.tool()
async def convert_currency(from_currency: str, to_currency: str, amount: float) -> dict:
    """
    Convert amount from one currency to another.

    Args:
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
        amount: Amount to convert
    """
    api_key = settings.exchange_rates_api_key
    if not api_key:
        raise ValueError("Exchange Rates API key not configured")

    try:
        data = await currency_client.get(
            f"/{api_key}/pair/{from_currency.upper()}/{to_currency.upper()}/{amount}"
        )

        if data["result"] == "success":
            return {
                "from_currency": data["base_code"],
                "to_currency": data["target_code"],
                "exchange_rate": data["conversion_rate"],
                "original_amount": amount,
                "converted_amount": data["conversion_result"],
                "last_updated": data["time_last_update_utc"],
            }
        else:
            raise Exception(f"API Error: {data.get('error-type', 'Unknown error')}")

    except Exception as e:
        raise Exception(f"Failed to convert currency: {str(e)}")


@mcp.tool()
async def get_supported_currencies() -> dict:
    """
    Get list of all supported currencies.
    """
    api_key = settings.exchange_rates_api_key
    if not api_key:
        raise ValueError("Exchange Rates API key not configured")

    try:
        data = await currency_client.get(f"/{api_key}/codes")

        if data["result"] == "success":
            currencies = {}
            for code_pair in data["supported_codes"]:
                currencies[code_pair[0]] = code_pair[1]

            return {"total_currencies": len(currencies), "currencies": currencies}
        else:
            raise Exception(f"API Error: {data.get('error-type', 'Unknown error')}")

    except Exception as e:
        raise Exception(f"Failed to get supported currencies: {str(e)}")


@mcp.tool()
async def get_historical_rates(
    base_currency: str, target_currency: str, date: str
) -> dict:
    """
    Get historical exchange rates for a specific date.

    Args:
        base_currency: Base currency code (e.g., 'USD')
        target_currency: Target currency code (e.g., 'EUR')
        date: Date in YYYY-MM-DD format
    """
    api_key = settings.exchange_rates_api_key
    if not api_key:
        raise ValueError("Exchange Rates API key not configured")

    try:
        # Parse date to ensure correct format
        from datetime import datetime

        datetime.strptime(date, "%Y-%m-%d")

        data = await currency_client.get(
            f"/{api_key}/history/{base_currency.upper()}/{date}"
        )

        if data["result"] == "success":
            target_rate = data["conversion_rates"].get(target_currency.upper())

            return {
                "base_currency": data["base_code"],
                "target_currency": target_currency.upper(),
                "date": date,
                "exchange_rate": target_rate,
                "all_rates": data["conversion_rates"]
                if target_currency.upper() == "ALL"
                else None,
            }
        else:
            raise Exception(f"API Error: {data.get('error-type', 'Unknown error')}")

    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD format.")
    except Exception as e:
        raise Exception(f"Failed to get historical rates: {str(e)}")
