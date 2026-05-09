"""
Traffic generator. Hits the API on a loop so Prometheus has something
interesting to scrape. Probabilities and interval are env-configurable
so learners can change traffic shape from docker-compose.yml.
"""

import logging
import os
import random
import signal
import sys
import time

import httpx

API_URL = os.getenv("API_URL", "http://api:8000")
INTERVAL_MS = int(os.getenv("REQUEST_INTERVAL_MS", "500"))
SLOW_PROB = float(os.getenv("SLOW_PROBABILITY", "0.2"))
ERROR_PROB = float(os.getenv("ERROR_PROBABILITY", "0.15"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("worker")

_running = True


def _stop(*_):
    global _running
    _running = False


signal.signal(signal.SIGINT, _stop)
signal.signal(signal.SIGTERM, _stop)


def pick_endpoint() -> str:
    r = random.random()
    if r < ERROR_PROB:
        return "/error"
    if r < ERROR_PROB + SLOW_PROB:
        return "/slow"
    return "/"


def main() -> None:
    log.info(
        "worker starting api=%s interval=%dms slow=%.2f error=%.2f",
        API_URL, INTERVAL_MS, SLOW_PROB, ERROR_PROB,
    )
    interval = INTERVAL_MS / 1000.0
    with httpx.Client(timeout=10.0) as client:
        while _running:
            endpoint = pick_endpoint()
            url = f"{API_URL}{endpoint}"
            try:
                resp = client.get(url)
                log.info("GET %s -> %d", endpoint, resp.status_code)
            except httpx.HTTPError as exc:
                log.warning("GET %s failed: %s", endpoint, exc)
            time.sleep(interval)
    log.info("worker stopped")


if __name__ == "__main__":
    sys.exit(main())
