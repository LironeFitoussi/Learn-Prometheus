# Prometheus Fundamentals — SRE Investigation Lab

> You are the new on-call engineer for the **orders-api** service. Your team uses Prometheus. Your job in this lab is not to memorize PromQL — it is to **think like an SRE**: form hypotheses, ask the right questions, and let the metrics answer them.

---

## 1. Introduction

### What Prometheus is

Prometheus is an open-source **time-series database** plus a **scrape engine** plus a **query language**. It periodically pulls metrics from your services (the **pull model**), stores each observation as a numeric sample with a timestamp, and lets you query the history with **PromQL**.

### Why pull, not push

Push systems (StatsD, etc.) make services responsible for delivering metrics. Pull systems make the monitor responsible for collecting them. Pull means:

- Prometheus knows whether a target is reachable. (If a scrape fails, it records `up == 0` automatically.)
- Service code stays simple — just expose `/metrics`.
- Adding new monitoring is a config change, not a code change.

### Metrics, labels, time series

A **metric** is a named measurement, e.g. `http_requests_total`. **Labels** are key/value dimensions attached to it, e.g. `method="GET"`, `endpoint="/slow"`, `status="200"`. The combination

```
http_requests_total{method="GET", endpoint="/slow", status="200"}
```

is one **time series** — a stream of `(timestamp, value)` samples. Change any label value and you get a new, separate series.

### Why observability matters

Logs tell you *what happened* once. Metrics tell you *how often* and *how fast* over time. When a service degrades at 3 a.m. you don't read logs first — you look at the latency graph and the error rate graph. That is the muscle this lab builds.

---

## 2. Architecture

```
                ┌──────────────┐
                │   worker     │  generates traffic
                │ (no metrics) │  every 500ms
                └──────┬───────┘
                       │  HTTP GET /, /slow, /error
                       ▼
                ┌──────────────┐    ┌──────────┐
                │   api        │───▶│  redis   │  (supporting dep,
                │  FastAPI     │    │          │   no metrics)
                │  /metrics    │    └──────────┘
                └──────┬───────┘
                       │  Prometheus scrapes /metrics every 5s
                       ▼
                ┌──────────────┐
                │  prometheus  │   :9090 — query UI + TSDB
                └──────────────┘
```

| Container   | Role                                                                |
| ----------- | ------------------------------------------------------------------- |
| api         | FastAPI service. Exposes `/`, `/slow`, `/error`, `/metrics`.        |
| worker      | Loop that hits the API. Creates realistic, noisy traffic.           |
| redis       | Backing store the API touches. Supporting dep, not instrumented.    |
| prometheus  | Scrapes `api:8000/metrics` and `localhost:9090/metrics` every 5s.   |

### Why `/metrics` exists

The API does not push anything anywhere. It just serves a plain-text page on `/metrics` listing every metric and its current value. Prometheus is the only thing that calls that endpoint. This separation is the entire point of the pull model.

---

## 3. Startup

```bash
cd Labs/prometheus-fundamentals-lab
docker compose up --build -d
```

Verify all four containers are running:

```bash
docker compose ps
```

Open these in your browser:

| URL                                   | What you should see                              |
| ------------------------------------- | ------------------------------------------------ |
| http://localhost:9090                 | Prometheus query UI                              |
| http://localhost:9090/targets         | Two scrape jobs, both UP                         |
| http://localhost:8000/                | `{"service":"orders-api","status":"ok"}`         |
| http://localhost:8000/metrics         | Raw metrics text — scroll through it             |

Watch the worker doing its job:

```bash
docker compose logs -f worker
```

---

## 4. Core Concepts

Each concept is illustrated with a metric **from this lab**. Open Prometheus at http://localhost:9090, paste the query into the expression bar, hit **Execute**, switch between **Table** and **Graph**.

### Counter

A monotonically increasing number. Resets only when the process restarts.

> Try: `http_requests_total`

You will see many series — one per `(method, endpoint, status)` combination. The raw value is rarely useful by itself; it grows forever. You almost always wrap a counter in `rate()` or `increase()`.

### Gauge

A value that goes up *and* down.

> Try: `active_requests`

Mostly 0 or 1 in this lab. When `/slow` is sleeping, the gauge for `endpoint="/slow"` will sit at 1 for that duration.

### Histogram

A counter, but split into **buckets**. Each bucket counts how many observations fell at or below a latency threshold. Histograms are how you compute percentiles.

> Try: `http_request_duration_seconds_bucket`
> Then: `http_request_duration_seconds_count`
> Then: `http_request_duration_seconds_sum`

Three series families come from one histogram metric:
- `_bucket{le="0.1"}` — count of requests with duration ≤ 0.1s
- `_count` — total observations (same as the request counter)
- `_sum` — sum of all observed durations (lets you compute average)

You'll use this in Exercise B.

### Labels

Labels are how you slice. Try:

> `http_requests_total{endpoint="/error"}`
> `http_requests_total{status="500"}`
> `http_requests_total{endpoint="/error", status="500"}`

### Time series

A series = metric name + label set. Each line in the **Table** view of `http_requests_total` is **one** time series. `count(http_requests_total)` will tell you how many distinct series exist for that metric — that number is your **cardinality**.

---

## 5. Investigation-Based Exercises

Rules of engagement:

1. Read the **Scenario** and **Symptoms**.
2. Try to answer the **Questions to ask** before looking at hints.
3. Use hints **one at a time**. Stop as soon as you can move forward.
4. Run the **Validation** step before peeking at the solution.
5. Solutions live at the bottom — earn them.

> Need traffic to stop or speed up between exercises?
> ```bash
> docker compose stop worker     # silence
> docker compose start worker    # resume
> ```

---

### Exercise A — Is The Service Healthy?

**Scenario.** A teammate writes in Slack: *"users are reporting failures on orders-api, can you check?"*

**Symptoms.**
- You have access to Prometheus only.
- You don't know which endpoint is failing or how often.

**Questions to ask yourself.**
- What does "failure" mean as a metric? An HTTP status? A scrape failure? Both?
- Which metric in this lab records HTTP responses? Which label distinguishes good from bad?
- Are failures concentrated on one endpoint, or spread out?
- "Reporting failures" — is the rate elevated, or has it always been like this?

**Investigation goals.**
- Find the metric that exposes per-status request counts.
- Quantify the failure rate (failures per second).
- Identify which endpoint is the worst offender.

**Hints (use in order, only as needed).**

> Hint 1 — Which of `http_requests_total`, `http_request_duration_seconds`, `active_requests` carries a status label?

> Hint 2 — A counter's raw value isn't useful. What function turns a counter into "events per second"?

> Hint 3 — Try filtering. `{status="500"}` narrows to errors. `{status=~"5.."}` matches any 5xx via regex.

> Hint 4 — To compare per-endpoint, sum away the status and group by endpoint: `sum by (endpoint) (...)`.

**Validation.**
- You can produce a graph of error rate per endpoint.
- You can state, in one sentence, which endpoint is contributing most failures and at roughly what rate.

---

### Exercise B — Something Is Slow

**Scenario.** A second message: *"the API feels sluggish."* "Feels" is not a metric.

**Symptoms.**
- No specific endpoint named.
- No specific latency threshold cited.

**Questions to ask yourself.**
- "Slow" compared to what? Average? p95? p99?
- Why would looking at the average duration mislead you?
- Which metric family has buckets, and what is a bucket *for*?
- If 99% of requests finish in 100ms but 1% take 5 seconds, what tells the real story?

**Investigation goals.**
- Compute a p95 latency per endpoint.
- Identify which endpoint has tail latency that would justify the "sluggish" complaint.
- Be able to explain *why* `histogram_quantile` needs `_bucket` plus `rate()`.

**Hints.**

> Hint 1 — Look at `http_request_duration_seconds_sum` and `http_request_duration_seconds_count`. Their ratio gives you something — what?

> Hint 2 — That ratio is the **average**. Averages hide spikes. You want a percentile.

> Hint 3 — Percentiles come from the `_bucket` series. There is a function literally named `histogram_quantile`.

> Hint 4 — `histogram_quantile` needs a *rate* of bucket counts as input, not the raw counter. The `le` label is the bucket boundary; you must keep it.

> Hint 5 — Skeleton: `histogram_quantile(0.95, sum by (le, endpoint) (rate(<bucket_metric>[5m])))`.

**Validation.**
- Your graph shows distinct latency lines for `/`, `/slow`, `/error`.
- `/slow` has a clearly higher p95 than the others. Make sure you can articulate why that matches the worker's behavior.

---

### Exercise C — Traffic Spike

**Scenario.** A capacity-planning question: *"how many requests per second is this service actually handling, broken down by endpoint?"*

**Symptoms.** None — this is a baseline question, not an incident. But how you answer it is the same skill you'd use during a real spike.

**Questions to ask yourself.**
- Why can't I just read `http_requests_total` and divide by uptime?
- What's the difference between `rate()` and `increase()`?
- What window length makes sense for a 5s scrape interval?

**Investigation goals.**
- Produce a per-endpoint requests-per-second graph.
- Now simulate a spike. Edit the worker's interval and observe the graph react.

**To create a spike.**

```bash
# Drop interval from 500ms to 50ms = ~10x traffic
docker compose stop worker
# edit docker-compose.yml: REQUEST_INTERVAL_MS: "50"
docker compose up -d worker
```

**Hints.**

> Hint 1 — `rate(metric[window])` gives **per-second average** over `window`.

> Hint 2 — Window must be at least 4× the scrape interval to be reliable. With 5s scrapes, `[1m]` is a safe minimum, `[5m]` smoother.

> Hint 3 — To see one line per endpoint instead of dozens (one per status combo), aggregate: `sum by (endpoint) (rate(... [1m]))`.

**Validation.**
- Before / after spike, your `sum by (endpoint) (rate(...))` graph clearly shows the jump.
- You can articulate why a shorter window reacts faster but is noisier.
- Reset the worker interval back to 500ms when done.

---

### Exercise D — API Down

**Scenario.** A real outage drill.

**Inflict the outage.**
```bash
docker compose stop api
```

**Symptoms.**
- No requests succeed.
- Worker logs flood with connection errors.

**Questions to ask yourself.**
- What metric does Prometheus generate **on its own**, regardless of what the target exposes?
- Where in the Prometheus UI can you see scrape health directly?
- If the API is down, which of these will *also* go to zero, and which will simply stop updating?
   - `http_requests_total`
   - `up`
   - `rate(http_requests_total[1m])`

**Investigation goals.**
- Confirm the outage from Prometheus (not from `docker ps`).
- Be able to explain the difference between "metric is missing" and "metric is zero".

**Hints.**

> Hint 1 — Visit http://localhost:9090/targets. What changed?

> Hint 2 — There is a single built-in metric every job has, and its value is 0 or 1. What is it?

> Hint 3 — Counters that aren't being scraped don't reset to zero — they freeze at last value. But `rate()` over a window with no new samples will eventually evaluate to 0. Why?

**Recovery.**
```bash
docker compose start api
```
Watch `up{job="api"}` flip back to 1.

**Validation.**
- You produced a graph of `up` showing the gap.
- You can explain to a colleague the difference between a missing series and a zero-valued series.

---

### Exercise E — Label Exploration

**Scenario.** You've been asked to add a new label `customer_tier` (e.g. `free`, `pro`, `enterprise`) to `http_requests_total`. Before you ship the change, your tech lead asks: *"how many new series will that create?"*

**Questions to ask yourself.**
- How is the count of distinct series for a metric determined?
- What is **cardinality** and why does Prometheus care?
- Roughly how many series exist *today* for `http_requests_total`?
- If you add one label with 3 possible values, what happens to the series count? What if it had 10,000 values (e.g. user IDs)?

**Investigation goals.**
- Compute current cardinality of `http_requests_total`.
- Reason about the multiplicative effect of adding a label.
- Articulate the rule: **never label by anything unbounded** (user ID, request ID, full URL with query string).

**Hints.**

> Hint 1 — `count()` counts series, not samples.

> Hint 2 — Try `count(http_requests_total)`. Now `count by (endpoint) (http_requests_total)`.

> Hint 3 — Adding a label multiplies cardinality by that label's distinct value count. Adding `customer_tier` with 3 values → ~3× series. Adding `user_id` with 1M users → 1M× series. The TSDB will not love you.

**Validation.**
- You can name the current cardinality of `http_requests_total`.
- You can predict the cardinality after adding a 3-valued label.
- You can list two label ideas that would be **bad** (unbounded) and one that would be safe (small fixed set).

---

### Exercise F — Counter Behavior

**Scenario.** A junior teammate graphs `http_requests_total` directly and says: *"why does this just keep going up forever? It's useless."*

**Questions to ask yourself.**
- Why is a counter designed to only increase?
- What happens to a counter when the API process restarts? Try it:
  ```bash
  docker compose restart api
  ```
- Now graph `http_requests_total{endpoint="/"}` raw — what shape do you see at the restart moment?
- Now graph `rate(http_requests_total{endpoint="/"}[1m])` over the same period. Why does this one *not* show a giant negative spike or weird behavior?

**Investigation goals.**
- See a counter reset with your own eyes.
- Understand that `rate()` is **counter-reset aware** — that is the entire reason the function exists.
- Be able to explain why exposing a "requests in the last minute" gauge directly from the app would be a worse design than exposing a counter.

**Hints.**

> Hint 1 — Restart the API and graph the raw counter and the `rate()` side by side, in the Prometheus **Graph** tab.

> Hint 2 — Read the Prometheus docs definition of `rate()` aloud: "calculates the per-second average rate of increase, **automatically adjusts for resets**".

> Hint 3 — If the app exposed "requests in last minute" as a gauge, what happens between scrapes? What if the scrape misses one cycle? Counters + `rate()` are **derivable** server-side from any window — gauges are not.

**Validation.**
- You can describe what `rate()` does on a reset, in plain English.
- You can defend the "always counter, never gauge for events" rule.

---

## Solutions

> Read these only after you've worked the exercise.

<details>
<summary>Exercise A solution</summary>

```promql
# Per-endpoint 5xx error rate (errors per second)
sum by (endpoint) (rate(http_requests_total{status=~"5.."}[1m]))

# Errors as a fraction of total requests
sum by (endpoint) (rate(http_requests_total{status=~"5.."}[1m]))
  /
sum by (endpoint) (rate(http_requests_total[1m]))
```
`/error` should dominate (~40% error rate by design).
</details>

<details>
<summary>Exercise B solution</summary>

```promql
# p95 latency per endpoint
histogram_quantile(
  0.95,
  sum by (le, endpoint) (rate(http_request_duration_seconds_bucket[5m]))
)

# average (for comparison — note how it lies)
sum by (endpoint) (rate(http_request_duration_seconds_sum[5m]))
  /
sum by (endpoint) (rate(http_request_duration_seconds_count[5m]))
```
`/slow` p95 will be in the multi-second range; the average is much lower because most calls return fast.
</details>

<details>
<summary>Exercise C solution</summary>

```promql
sum by (endpoint) (rate(http_requests_total[1m]))
```
After dropping `REQUEST_INTERVAL_MS` to 50, all lines should rise ~10×.
</details>

<details>
<summary>Exercise D solution</summary>

```promql
up{job="api"}
```
Reads 1 normally, drops to 0 while the API is stopped, returns to 1 on recovery. `http_requests_total` series go *stale* (no new samples) but their last-known value persists for ~5 minutes; `rate(...[1m])` falls to 0 because there is no increase in the window.
</details>

<details>
<summary>Exercise E solution</summary>

```promql
count(http_requests_total)
count by (endpoint) (http_requests_total)
```
With three endpoints (`/`, `/slow`, `/error`), one method (`GET`), and a small set of statuses (mostly `200`, plus `500` from `/error`), expect ~4–6 distinct series. Adding a 3-valued label triples that. Adding a per-user label is the classic outage cause.
</details>

<details>
<summary>Exercise F solution</summary>

```promql
http_requests_total{endpoint="/"}                 # raw — drops to 0 on restart
rate(http_requests_total{endpoint="/"}[1m])       # smooth across the reset
```
`rate()` detects that the counter went down and treats the new lower value as a fresh start, instead of reporting a huge negative rate.
</details>

---

## Where To Go Next

- Add a second instance of the API (`docker compose up --scale api=2`). Watch series multiply by `instance`. Re-run Exercise B aggregating across instances.
- Replace the worker with `hey` or `wrk` for controlled load testing.
- Move on to the sibling lab `prometheus-lab/` (this repo) for a Grafana + Node Exporter + cAdvisor host-monitoring view.
- Read the Prometheus docs on **recording rules** and **alerting rules**, then add an alert for `sum by (endpoint) (rate(http_requests_total{status=~"5.."}[1m])) > 0.5`.
