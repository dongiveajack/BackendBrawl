import contextlib
from fastapi import FastAPI
from redis.asyncio import Redis, ConnectionPool

import os

# Global variables for Redis connection
pool: ConnectionPool = None
client: Redis = None

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Setup Redis connection pool
    global pool, client
    redis_host = os.getenv("REDIS_HOST", "localhost")
    # minimal logging or no logging
    pool = ConnectionPool.from_url(f"redis://{redis_host}:6379", max_connections=2500)
    client = Redis(connection_pool=pool)
    yield
    # Shutdown: Close connection pool
    await client.aclose()
    await pool.disconnect()

from prometheus_fastapi_instrumentator import Instrumentator

# Disable unnecessary logging (uvicorn handles this via config mostly, but we can reduce internal logs)
app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)

@app.get("/cache")
async def get_cache():
    # Single responsibility: HTTP -> Redis GET -> Response
    value = await client.get("test_key")
    
    # Minimal JSON serialization overhead
    # Return dictionary directly, FastAPI handles JSON encoding
    # redis-py returns bytes, need to decode
    if value:
        return {"value": value.decode("utf-8")}
    return {"value": None}
