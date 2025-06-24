import httpx
from typing import Dict, Any, Optional
import asyncio


class APIClient:
    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        self.base_url = base_url
        self.default_headers = default_headers or {}

    async def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make GET request to API endpoint"""
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=request_headers)
            response.raise_for_status()
            return response.json()

    async def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make POST request to API endpoint"""
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data, headers=request_headers)
            response.raise_for_status()
            return response.json()


# Retry decorator for API calls
def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    await asyncio.sleep(delay * (2**attempt))
            return None

        return wrapper

    return decorator
