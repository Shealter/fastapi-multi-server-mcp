# Deployment Guide

## Local Development

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd multi-server-mcp
   uv venv && source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run Application**
   ```bash
   python main.py
   ```

## Docker Deployment

1. **Build Image**
   ```bash
   docker build -t mcp-server .
   ```

2. **Run Container**
   ```bash
   docker run -d -p 10000:10000 --env-file .env mcp-server
   ```

3. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

## Production Deployment

### Using Gunicorn

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:10000
```

### Environment Variables

```env
# Production settings
PORT=10000
HOST=0.0.0.0
LOG_LEVEL=info
WORKERS=4

# API Keys (required)
OPENWEATHER_API_KEY=your_key
NEWS_API_KEY=your_key
GITHUB_TOKEN=your_token
EXCHANGE_RATES_API_KEY=your_key
```

### Health Checks

The application provides a health check endpoint at `/health`:

```bash
curl http://localhost:10000/health
```

Response:
```json
{
  "status": "healthy",
  "servers": 5
}
```

## Monitoring

### Logging

The application uses structured logging. In production, consider:

- Centralized logging (ELK stack, Splunk)
- Log rotation and retention policies
- Error tracking (Sentry, Rollbar)

### Metrics

Consider adding:

- Prometheus metrics
- Application performance monitoring
- API response time tracking
- Rate limiting monitoring

## Security Considerations

1. **API Keys**: Store securely using environment variables or secret management
2. **Rate Limiting**: Implement rate limiting for public endpoints
3. **HTTPS**: Always use HTTPS in production
4. **CORS**: Configure CORS appropriately for your use case
5. **Authentication**: Consider adding authentication for sensitive endpoints
