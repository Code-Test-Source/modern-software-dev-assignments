import argparse
import logging
import os
import time
from typing import Any, Optional

import httpx
import uvicorn
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("weather_mcp_server")

API_BASE_URL = "https://api.open-meteo.com/v1"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1"

API_KEY: Optional[str] = os.environ.get("WEATHER_API_KEY")
RATE_LIMIT_REQUESTS = 100
RATE_LIMIT_WINDOW = 60

_rate_limit_store: dict[str, list[float]] = {}

app = Server(
    name="weather-mcp-server",
    version="1.0.0",
)


def _check_rate_limit(client_id: str) -> bool:
    """Check if client has exceeded rate limit."""
    now = time.time()
    if client_id not in _rate_limit_store:
        _rate_limit_store[client_id] = []

    _rate_limit_store[client_id] = [
        ts for ts in _rate_limit_store[client_id] if now - ts < RATE_LIMIT_WINDOW
    ]

    if len(_rate_limit_store[client_id]) >= RATE_LIMIT_REQUESTS:
        return False

    _rate_limit_store[client_id].append(now)
    return True


def _validate_api_key(request: Request) -> bool:
    """Validate API key from request headers."""
    if API_KEY is None:
        return True

    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False

    token = auth_header[7:]
    return token == API_KEY


def _get_coordinates(city: str) -> dict[str, float]:
    """Get latitude and longitude for a city using geocoding API."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            f"{GEOCODING_URL}/search",
            params={"name": city, "count": 1, "language": "en", "format": "json"},
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("results"):
            raise ValueError(f"City '{city}' not found")

        result = data["results"][0]
        return {"latitude": result["latitude"], "longitude": result["longitude"]}


def _get_weather(lat: float, lon: float) -> dict[str, Any]:
    """Get current weather data."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            f"{API_BASE_URL}/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m",
                "timezone": "auto",
            },
        )
        response.raise_for_status()
        return response.json()


def _get_forecast(lat: float, lon: float, days: int = 7) -> dict[str, Any]:
    """Get weather forecast."""
    with httpx.Client(timeout=10.0) as client:
        response = client.get(
            f"{API_BASE_URL}/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                "timezone": "auto",
                "forecast_days": days,
            },
        )
        response.raise_for_status()
        return response.json()


def _validate_city(city: str) -> str:
    """Validate city name input."""
    if not city or not isinstance(city, str):
        raise ValueError("City name is required")
    city = city.strip()
    if len(city) < 2:
        raise ValueError("City name must be at least 2 characters")
    if len(city) > 100:
        raise ValueError("City name must be less than 100 characters")
    return city


def _validate_days(days: Any) -> int:
    """Validate days parameter."""
    if days is None:
        return 7
    try:
        days = int(days)
    except (ValueError, TypeError) as e:
        raise ValueError("Days must be an integer") from e
    if days < 1:
        raise ValueError("Days must be at least 1")
    if days > 7:
        raise ValueError("Days must be at most 7")
    return days


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware for HTTP mode."""

    async def dispatch(self, request: Request, call_next):
        client_id = request.client.host if request.client else "unknown"

        if not _check_rate_limit(client_id):
            logger.warning(f"Rate limit exceeded for client: {client_id}")
            return JSONResponse(
                status_code=429, content={"error": "Rate limit exceeded. Try again later."}
            )

        response = await call_next(request)
        return response


class AuthMiddleware(BaseHTTPMiddleware):
    """Authentication middleware for HTTP mode."""

    async def dispatch(self, request: Request, call_next):
        if API_KEY is None:
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            logger.warning(f"Missing or invalid Authorization header from {request.client.host}")
            return JSONResponse(
                status_code=401,
                content={"error": "Authorization header required. Use 'Bearer <api_key>'"},
            )

        token = auth_header[7:]
        if token != API_KEY:
            logger.warning(f"Invalid API key from {request.client.host}")
            return JSONResponse(status_code=401, content={"error": "Invalid API key"})

        return await call_next(request)


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather for a city. Returns temperature, humidity, wind speed, and weather condition.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'San Francisco', 'London', 'Tokyo')",
                    }
                },
                "required": ["city"],
            },
        ),
        Tool(
            name="get_weather_forecast",
            description="Get weather forecast for a city for up to 7 days.",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name (e.g., 'San Francisco', 'London', 'Tokyo')",
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days (1-7)",
                        "minimum": 1,
                        "maximum": 7,
                        "default": 7,
                    },
                },
                "required": ["city"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    try:
        if name == "get_current_weather":
            city = _validate_city(arguments.get("city"))
            logger.info(f"Getting current weather for: {city}")

            coords = _get_coordinates(city)
            weather = _get_weather(coords["latitude"], coords["longitude"])

            current = weather["current"]
            result = {
                "city": city,
                "temperature": current["temperature_2m"],
                "unit": "°C",
                "humidity": current["relative_humidity_2m"],
                "wind_speed": current["wind_speed_10m"],
                "wind_unit": "km/h",
                "weather_code": current["weather_code"],
                "timezone": weather["timezone"],
            }

            return [TextContent(type="text", text=str(result))]

        elif name == "get_weather_forecast":
            city = _validate_city(arguments.get("city"))
            days = _validate_days(arguments.get("days", 7))
            logger.info(f"Getting {days}-day forecast for: {city}")

            coords = _get_coordinates(city)
            forecast = _get_forecast(coords["latitude"], coords["longitude"], days)

            daily = forecast["daily"]
            result = {
                "city": city,
                "timezone": forecast["timezone"],
                "forecast": [
                    {
                        "date": daily["time"][i],
                        "temp_max": daily["temperature_2m_max"][i],
                        "temp_min": daily["temperature_2m_min"][i],
                        "weather_code": daily["weather_code"][i],
                    }
                    for i in range(len(daily["time"]))
                ],
            }

            return [TextContent(type="text", text=str(result))]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except httpx.TimeoutException:
        logger.error("Request timed out")
        return [TextContent(type="text", text="Error: Request timed out. Please try again.")]
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e}")
        return [TextContent(type="text", text=f"Error: HTTP error {e.response.status_code}")]
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return [TextContent(type="text", text=f"Error: {str(e)}")]
    except Exception as e:
        logger.exception("Unexpected error")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def stdio_main() -> None:
    """STDIO server main entry point."""
    logger.info("Starting Weather MCP Server (STDIO mode)")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


def create_sse_app() -> Starlette:
    """Create SSE-based HTTP server for remote MCP."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(request.scope, request.receive, request._send) as (
            read_stream,
            write_stream,
        ):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    async def health_check(request: Request) -> JSONResponse:
        return JSONResponse({"status": "healthy", "server": "weather-mcp-server"})

    app_starlette = Starlette(
        routes=[
            Route("/health", health_check),
            Route("/sse", endpoint=handle_sse),
            Route("/messages", endpoint=handle_sse),
        ]
    )

    app_starlette.add_middleware(RateLimitMiddleware)
    if API_KEY:
        app_starlette.add_middleware(AuthMiddleware)

    return app_starlette


async def http_main(host: str = "0.0.0.0", port: int = 8000) -> None:
    """HTTP server main entry point."""
    auth_enabled = API_KEY is not None
    logger.info(f"Starting Weather MCP Server (HTTP mode) on {host}:{port}")
    logger.info(f"Authentication: {'enabled' if auth_enabled else 'disabled'}")

    config = uvicorn.Config(
        create_sse_app(),
        host=host,
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    import asyncio

    parser = argparse.ArgumentParser(description="Weather MCP Server")
    parser.add_argument(
        "--mode",
        choices=["stdio", "http"],
        default="stdio",
        help="Server mode: stdio (local) or http (remote)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="HTTP host")
    parser.add_argument("--port", type=int, default=8000, help="HTTP port")
    args = parser.parse_args()

    if args.mode == "http":
        asyncio.run(http_main(args.host, args.port))
    else:
        asyncio.run(stdio_main())
