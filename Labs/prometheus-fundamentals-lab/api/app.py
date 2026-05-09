"""
FastAPI service instrumented with Prometheus metrics.

Endpoints:
    GET /          -> normal response
    GET /slow      -> sleeps a random amount before responding
    GET /error     -> randomly returns HTTP 500
    GET /healthz   -> liveness probe (no metrics side-effects)
    GET /metrics   -> Prometheus exposition format

Metrics exposed:
    http_requests_total          (Counter)   labels: method, endpoint, status
    http_request_duration_seconds(Histogram) labels: method, endpoint
    active_requests              (Gauge)     labels: endpoint
"""

import os
import random
import time
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, PlainTextResponse
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

# --- Metrics ----------------------------------------------------------------
# Counter: monotonically increasing. Wrap with rate() in PromQL to get qps.
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests processed.",
    labelnames=("method", "endpoint", "status"),
)

# Histogram: bucketed observations. Used to compute latency percentiles via
# histogram_quantile() in PromQL. Buckets chosen for a web service profile.
HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds.",
    labelnames=("method", "endpoint"),
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)

# Gauge: instantaneous value, can go up and down. Tracks in-flight requests.
ACTIVE_REQUESTS = Gauge(
    "active_requests",
    "Number of in-flight HTTP requests.",
    labelnames=("endpoint",),
)

# --- Redis (supporting dep) -------------------------------------------------
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
_redis: redis.Redis | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    global _redis
    _redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    try:
        _redis.ping()
    except redis.RedisError:
        pass
    yield
    if _redis is not None:
        _redis.close()


app = FastAPI(title="orders-api", lifespan=lifespan)


# --- Metrics middleware -----------------------------------------------------
# Wraps every request to record duration, status, and active count.
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    endpoint = request.url.path
    method = request.method

    if endpoint == "/metrics":
        return await call_next(request)

    ACTIVE_REQUESTS.labels(endpoint=endpoint).inc()
    start = time.perf_counter()
    try:
        response = await call_next(request)
        status = response.status_code
    except Exception:
        status = 500
        raise
    finally:
        elapsed = time.perf_counter() - start
        HTTP_REQUEST_DURATION_SECONDS.labels(
            method=method, endpoint=endpoint
        ).observe(elapsed)
        HTTP_REQUESTS_TOTAL.labels(
            method=method, endpoint=endpoint, status=str(status)
        ).inc()
        ACTIVE_REQUESTS.labels(endpoint=endpoint).dec()

    return response


# --- Routes -----------------------------------------------------------------
@app.get("/")
def root():
    if _redis is not None:
        try:
            _redis.incr("orders:hits")
        except redis.RedisError:
            pass
    return {"service": "orders-api", "status": "ok"}


@app.get("/slow")
def slow():
    # Mostly fast, sometimes very slow — gives histograms something to chew on.
    delay = random.choices(
        population=[0.05, 0.2, 0.8, 2.0, 4.0],
        weights=[60, 20, 12, 6, 2],
        k=1,
    )[0]
    time.sleep(delay)
    return {"slept_seconds": delay}


@app.get("/error")
def error():
    # ~40% chance of 500, otherwise 200. Realistic noisy-endpoint behavior.
    if random.random() < 0.4:
        return JSONResponse(status_code=500, content={"error": "boom"})
    return {"status": "ok"}


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
