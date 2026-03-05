# Weather MCP Server

A Model Context Protocol (MCP) server that provides weather information using the Open-Meteo API (free, no API key required).

## Features

- **get_current_weather**: Get current weather for any city (temperature, humidity, wind speed, weather condition)
- **get_weather_forecast**: Get weather forecast for up to 7 days
- **Dual transport support**: STDIO (local) and HTTP/SSE (remote)
- **API key authentication**: Optional Bearer token authentication for HTTP mode
- **Rate limiting**: 100 requests per minute per client
- **Input validation**: Robust city and days parameter validation
- **Error handling**: Graceful handling of timeouts, HTTP errors, and invalid inputs

## Requirements

- Python 3.12+
- conda environment `cs146s` or the following packages:
  - `mcp`
  - `httpx`
  - `uvicorn`
  - `starlette`

## Installation

1. Activate the conda environment:
```bash
conda activate cs146s
```

2. Or install dependencies directly:
```bash
pip install mcp httpx uvicorn starlette
```

## Running the Server

### STDIO Mode (Local)

Run the server in stdio mode for Claude Desktop or other local clients:

```bash
python -m server.main
```

Or explicitly:
```bash
python -m server.main --mode stdio
```

### HTTP Mode (Remote)

Run the server in HTTP mode for remote clients:

```bash
python -m server.main --mode http --port 8000
```

The server will start on `http://localhost:8000`.

## Configuration (Claude Desktop)

Add the following to your Claude Desktop config file:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["-m", "server.main"],
      "env": {}
    }
  }
}
```

Or use the absolute path:

```json
{
  "mcpServers": {
    "weather": {
      "command": "/home/username/miniconda3/envs/cs146s/bin/python",
      "args": ["-m", "server.main"]
    }
  }
}
```

## Authentication (HTTP Mode)

### Setting Up API Key

Set the `WEATHER_API_KEY` environment variable:

```bash
export WEATHER_API_KEY=your-secret-api-key
python -m server.main --mode http
```

### Client Request Format

Include the API key in the Authorization header:

```bash
curl -H "Authorization: Bearer your-secret-api-key" http://localhost:8000/health
```

## Rate Limiting

The server enforces rate limits:
- 100 requests per minute per client IP
- Returns 429 status when limit exceeded

## Tool Reference

### get_current_weather

Get current weather for a city.

**Parameters:**
- `city` (string, required): City name (e.g., "San Francisco", "London", "Tokyo")

**Example:**
```json
{
  "city": "San Francisco"
}
```

**Output:**
```json
{
  "city": "San Francisco",
  "temperature": 18.5,
  "unit": "°C",
  "humidity": 65,
  "wind_speed": 12.3,
  "wind_unit": "km/h",
  "weather_code": 3,
  "timezone": "America/Los_Angeles"
}
```

### get_weather_forecast

Get weather forecast for a city.

**Parameters:**
- `city` (string, required): City name
- `days` (integer, optional): Number of days (1-7), default: 7

**Example:**
```json
{
  "city": "London",
  "days": 5
}
```

**Output:**
```json
{
  "city": "London",
  "timezone": "Europe/London",
  "forecast": [
    {"date": "2026-03-03", "temp_max": 12.5, "temp_min": 5.2, "weather_code": 61},
    {"date": "2026-03-04", "temp_max": 13.1, "temp_min": 6.0, "weather_code": 63},
    ...
  ]
}
```

## Weather Codes

The weather codes follow the WMO Weather interpretation codes:
- 0: Clear sky
- 1, 2, 3: Mainly clear, partly cloudy, overcast
- 45, 48: Fog
- 51, 53, 55: Drizzle
- 61, 63, 65: Rain
- 71, 73, 75: Snow
- 80, 81, 82: Rain showers
- 95: Thunderstorm

## Error Handling

The server handles the following errors gracefully:
- Network timeouts (10 second timeout)
- HTTP errors (4xx, 5xx)
- Invalid city names
- Rate limiting
- Invalid input parameters

## Architecture

```
.
├── server/
│   ├── __init__.py
│   └── main.py          # Main server entry point
├── README.md
└── requirements.txt
```

## API Endpoints (HTTP Mode)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/sse` | GET | SSE connection for MCP |
| `/messages` | GET | Message endpoint |

## License

MIT
