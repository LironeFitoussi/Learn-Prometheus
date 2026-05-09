# Prometheus Fundamentals Lab

A small Docker Compose stack for **learning Prometheus by investigation**. An instrumented FastAPI service, a worker generating realistic traffic, Redis, and Prometheus — nothing else. No Grafana, no Alertmanager, no Kubernetes. The point is to build operational intuition: scraping, metrics, labels, time series, counters, histograms, and PromQL — applied to a service that is deliberately misbehaving.

> The real content of this lab is in [`lab-guide/LAB.md`](lab-guide/LAB.md). The README only gets you running.

---

## Quick Start

```bash
cd Labs/prometheus-fundamentals-lab
docker compose up --build -d
```

| URL                                  | What                                       |
| ------------------------------------ | ------------------------------------------ |
| http://localhost:9090                | Prometheus query UI                        |
| http://localhost:9090/targets        | Scrape target health                       |
| http://localhost:8000/               | API root                                   |
| http://localhost:8000/slow           | Slow endpoint                              |
| http://localhost:8000/error          | Random 500s                                |
| http://localhost:8000/metrics        | Raw Prometheus exposition                  |

Then open [`lab-guide/LAB.md`](lab-guide/LAB.md) and start with **Exercise A**.

---

## Architecture Overview

```
worker ──HTTP──▶ api ──▶ redis
                  │
                  │ /metrics
                  ▼
              prometheus  :9090
```

- **api** — FastAPI app, instrumented with `prometheus-client`. Exposes `http_requests_total` (counter), `http_request_duration_seconds` (histogram), `active_requests` (gauge).
- **worker** — Loops forever, hits `/`, `/slow`, `/error` with configurable probabilities.
- **redis** — Touched by the API. Supporting dependency, not instrumented.
- **prometheus** — Scrapes `api:8000` and itself every 5 seconds.

---

## Project Structure

```
prometheus-fundamentals-lab/
├── docker-compose.yml
├── prometheus/
│   └── prometheus.yml
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app.py
├── worker/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── worker.py
├── lab-guide/
│   └── LAB.md          ← the actual lesson
└── README.md
```

---

## Useful Commands

```bash
# Build + start everything
docker compose up --build -d

# Watch worker traffic
docker compose logs -f worker

# Watch API
docker compose logs -f api

# Restart only the API (used in Exercise F to demo counter resets)
docker compose restart api

# Stop the API to simulate an outage (Exercise D)
docker compose stop api
docker compose start api

# Change traffic shape — edit env vars in docker-compose.yml then:
docker compose up -d worker

# Hot-reload Prometheus config (after editing prometheus.yml)
curl -X POST http://localhost:9090/-/reload

# Stop everything (keep Prometheus TSDB volume)
docker compose down

# Stop everything and wipe stored metrics
docker compose down -v
```

---

## Tunables (worker)

Set in `docker-compose.yml` under `worker.environment`:

| Var                   | Default | Effect                                    |
| --------------------- | ------- | ----------------------------------------- |
| `REQUEST_INTERVAL_MS` | 500     | Time between requests. Lower = more load. |
| `SLOW_PROBABILITY`    | 0.2     | Fraction of requests that hit `/slow`.    |
| `ERROR_PROBABILITY`   | 0.15    | Fraction of requests that hit `/error`.   |

After changing these, restart the worker only:

```bash
docker compose up -d worker
```

---

## Troubleshooting

**`docker compose up --build` fails on Python install.**
Network issue or pip mirror. Retry; `pip` caches across builds.

**Prometheus targets show DOWN for `api`.**
Check the API came up: `docker compose ps`, `docker compose logs api`. From the prometheus container you can probe: `docker compose exec prometheus wget -qO- http://api:8000/metrics | head`.

**`/metrics` returns 404.**
The `/metrics` route is registered by `app.py`. If you edited the file, make sure you didn't accidentally delete the `metrics()` handler. Rebuild: `docker compose up --build -d api`.

**Worker logs say `connection refused`.**
The API is starting up. The worker's `depends_on` waits for the API healthcheck, but if the API crashes after starting you'll see this. `docker compose logs api` to see why.

**Port already in use (9090 or 8000).**
Something else is on it. Stop the other process or remap the host side in `docker-compose.yml` (e.g. `"19090:9090"`).

**No data in Prometheus graphs.**
Wait 30–60 seconds after `up`. Prometheus needs a few scrape cycles to have something to graph. Then refresh.

---

## Reset Instructions

```bash
# Just restart the stack (keeps stored metrics)
docker compose restart

# Wipe Prometheus TSDB and start fresh
docker compose down -v
docker compose up --build -d

# Nuclear: also remove built images so next build is from scratch
docker compose down -v --rmi local
docker compose up --build -d
```

---

## What's Next

Once you finish all six exercises in [`LAB.md`](lab-guide/LAB.md):

1. Add a recording rule that pre-computes `sum by (endpoint) (rate(http_requests_total[1m]))` so dashboards stay cheap.
2. Add an alerting rule that fires when 5xx rate exceeds 0.5/s for 2 minutes.
3. Move to the sibling [`../prometheus-lab/`](../prometheus-lab/) to bring Grafana, Node Exporter, and cAdvisor into the picture.
