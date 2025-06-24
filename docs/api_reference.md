## Weather Server (`/weather`)

### Tools

#### `get_current_weather`
Get current weather for a specific city.

**Parameters:**
- `city` (string): Name of the city
- `country_code` (string, optional): ISO 3166 country code
- `units` (string, optional): Temperature units ('metric', 'imperial', 'kelvin')

**Returns:**
```json
{
  "city": "London",
  "country": "GB",
  "temperature": 15.5,
  "feels_like": 14.2,
  "humidity": 78,
  "pressure": 1013,
  "description": "overcast clouds",
  "wind_speed": 3.2,
  "visibility": 10000,
  "units": "metric"
}
```

#### `get_weather_forecast`
Get weather forecast for a specific city.

**Parameters:**
- `city` (string): Name of the city
- `days` (int, optional): Number of days for forecast (1-5)
- `country_code` (string, optional): ISO 3166 country code
- `units` (string, optional): Temperature units

**Returns:**
```json
{
  "city": "London",
  "country": "GB",
  "forecasts": [
    {
      "datetime": "2024-01-01 12:00:00",
      "temperature": 15.5,
      "description": "clear sky",
      "humidity": 78,
      "wind_speed": 3.2
    }
  ],
  "units": "metric"
}
```

## News Server (`/news`)

### Tools

#### `get_top_headlines`
Get top news headlines.

**Parameters:**
- `country` (string, optional): Country code (default: 'us')
- `category` (string, optional): News category
- `page_size` (int, optional): Number of articles (max 100)

**Returns:**
```json
{
  "total_results": 100,
  "articles": [
    {
      "title": "Breaking News",
      "description": "Important news story",
      "url": "https://example.com/article",
      "source": "News Source",
      "author": "Reporter Name",
      "published_at": "2024-01-01T12:00:00Z",
      "url_to_image": "https://example.com/image.jpg"
    }
  ],
  "country": "us",
  "category": null
}
```

## GitHub Server (`/github`)

### Tools

#### `get_user_info`
Get GitHub user information.

**Parameters:**
- `username` (string): GitHub username

**Returns:**
```json
{
  "username": "testuser",
  "name": "Test User",
  "bio": "Software developer",
  "location": "San Francisco",
  "company": "GitHub",
  "public_repos": 50,
  "followers": 1000,
  "following": 100,
  "created_at": "2020-01-01T00:00:00Z",
  "avatar_url": "https://github.com/avatar.jpg",
  "html_url": "https://github.com/testuser"
}
```

## Currency Server (`/currency`)

### Tools

#### `convert_currency`
Convert amount from one currency to another.

**Parameters:**
- `from_currency` (string): Source currency code
- `to_currency` (string): Target currency code  
- `amount` (float): Amount to convert

**Returns:**
```json
{
  "from_currency": "USD",
  "to_currency": "EUR",
  "exchange_rate": 0.85,
  "original_amount": 100,
  "converted_amount": 85.0,
  "last_updated": "2024-01-01T00:00:00Z"
}
```

## Quote Server (`/quotes`)

### Tools

#### `get_random_quote`
Get a random inspirational quote.

**Parameters:**
- `min_length` (int, optional): Minimum quote length
- `max_length` (int, optional): Maximum quote length
- `tags` (string, optional): Comma-separated tags

**Returns:**
```json
{
  "quote": "The only way to do great work is to love what you do.",
  "author": "Steve Jobs",
  "length": 52,
  "tags": ["motivational", "work"]
}
```