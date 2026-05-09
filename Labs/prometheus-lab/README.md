# Prometheus Learning Lab

A self-contained Docker Compose stack for learning **Prometheus**, **Grafana**, **Node Exporter**, and **cAdvisor**. Beginner friendly, but structured the way a small production setup would be: pinned image versions, healthchecks, restart policies, named volumes, auto-provisioned datasource, alert rules, and helper scripts.

> Target: Linux Docker host. Works on Docker Desktop (macOS/Windows) with caveats — see [Troubleshooting](#troubleshooting).

---

## Architecture

```
                   ┌──────────────┐
                   │   Grafana    │   :3000
                   │ (dashboards) │
                   └──────┬───────┘
                          │  PromQL over HTTP
                          ▼
                   ┌──────────────┐
                   │  Prometheus  │   :9090
                   │  TSDB + rules│
                   └──┬────────┬──┘
                pull  │        │  pull
              /metrics│        │/metrics
                      ▼        ▼
            ┌─────────────┐  ┌──────────┐
            │node-exporter│  │ cAdvisor │
            │  host stats │  │container │
            │   :9100     │  │  stats   │
            └─────────────┘  │  :8080   │
                             └──────────┘
```

**Data flow:** exporters expose `/metrics` in Prometheus text format → Prometheus scrapes them every 5s → samples land in the local TSDB → Grafana queries Prometheus via PromQL → alert rules fire when expressions stay true for `for:` duration.

---

## Components

| Service       | Image                                   | Port | What it does                                                              |
| ------------- | --------------------------------------- | ---- | ------------------------------------------------------------------------- |
| prometheus    | `prom/prometheus:v2.55.1`               | 9090 | Pulls metrics, stores time series, evaluates rules. Web UI + query API.   |
| grafana       | `grafana/grafana:11.3.0`                | 3000 | Visualizes metrics. Datasource auto-provisioned to point at Prometheus.   |
| node-exporter | `prom/node-exporter:v1.8.2`             | 9100 | Exposes Linux host metrics (CPU, memory, disk, network) read from /proc.  |
| cadvisor      | `gcr.io/cadvisor/cadvisor:v0.49.1`      | 8080 | Per-container stats from cgroups + Docker.                                |

**Exporter** = a small process that translates some system's stats into the Prometheus text exposition format and serves them on `/metrics`. There are exporters for nearly every database, message queue, and OS — Node Exporter and cAdvisor are two of the most common.

---

## How Prometheus Scraping Works

Prometheus uses a **pull** model: it has a list of targets and HTTP-GETs `/metrics` from each one every `scrape_interval`. The endpoint returns plain text:

```
# HELP node_cpu_seconds_total Seconds the cpus spent in each mode.
# TYPE node_cpu_seconds_total counter
node_cpu_seconds_total{cpu="0",mode="idle"} 12345.67
node_cpu_seconds_total{cpu="0",mode="user"}   234.12
```

Each line becomes one sample on one **time series**. A series is uniquely identified by the metric name plus its label set:

```
node_cpu_seconds_total{cpu="0", mode="idle", instance="node-exporter:9100", job="node-exporter", role="host"}
```

`job` comes from the `job_name` in `prometheus.yml`. `instance` comes from the target's address. `role` is added explicitly under `static_configs.labels`. `cpu` and `mode` come from the exporter itself.

**Key idea:** changing any label produces a new, separate time series. That is why label cardinality matters in production — millions of unique series eat memory.

---

## Time Series, Labels, and the Data Model

* **Counter** — only goes up (e.g. `http_requests_total`). Always wrap counters in `rate()` before graphing.
* **Gauge** — can go up or down (e.g. `node_memory_MemAvailable_bytes`). Graph the raw value.
* **Histogram** / **Summary** — quantile-friendly aggregates (e.g. `http_request_duration_seconds_bucket`).

`rate(metric[5m])` = per-second average increase of a counter over the last 5 minutes. It is the workhorse function for counters — it handles counter resets and gives a smooth rate even with bursty data.

---

## Why cAdvisor Needs Host Mounts

cAdvisor runs in a container but reports on **the host and every container on it**. Each mount has a specific purpose:

| Mount                          | Why it's needed                                                  |
| ------------------------------ | ---------------------------------------------------------------- |
| `/:/rootfs:ro`                 | Read host filesystem layout and mount info.                      |
| `/var/run:/var/run:ro`         | Access Docker socket dir to discover and label running containers.|
| `/sys:/sys:ro`                 | Read **cgroup** stats — where Linux exposes per-container CPU and memory accounting. This is the core data source.|
| `/var/lib/docker/:/var/lib/docker:ro` | Read Docker container metadata (image, labels).           |
| `/dev/disk/:/dev/disk:ro`      | Resolve block devices for per-container disk I/O metrics.        |

Without these, cAdvisor either crashes or reports only a fraction of metrics. `privileged: true` is set because cgroup v2 on some distros requires it.

---

## Quickstart

```bash
cd Labs/prometheus-lab
docker compose up -d
```

| URL                          | What                                            |
| ---------------------------- | ----------------------------------------------- |
| http://localhost:9090        | Prometheus UI (Graph, Targets, Alerts, Status)  |
| http://localhost:9090/targets| Live target list with health and last error     |
| http://localhost:9090/alerts | Alert state                                     |
| http://localhost:3000        | Grafana — login `admin` / `admin`               |
| http://localhost:9100/metrics| Raw node-exporter output                        |
| http://localhost:8080        | cAdvisor UI                                     |

---

## Verifying the Stack

```bash
# 1. Containers healthy
docker compose ps

# 2. Prometheus self-check
curl -s http://localhost:9090/-/healthy

# 3. Targets all UP
bash scripts/check-targets.sh

# 4. A simple query (should return 4 series, all value 1)
curl -s 'http://localhost:9090/api/v1/query?query=up' | jq
```

In Grafana: **Explore → Prometheus → run** `up` — you should see one series per target.

---

## Starter PromQL Queries

```promql
# 1. Health of every scrape target. 1 = up, 0 = down.
up

# 2. Host CPU usage (%). Idle ratio inverted across all CPUs.
100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))

# 3. Available memory as fraction of total.
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes

# 4. Per-container CPU usage rate (cores).
rate(container_cpu_usage_seconds_total{name!=""}[5m])

# 5. Per-container memory usage (bytes).
container_memory_usage_bytes{name!=""}
```

Notes:
* `rate(...[5m])` — average per-second increase over a 5-minute window. Required for counter metrics.
* `{label!=""}` — filters out the empty-name aggregate series cAdvisor emits for the root cgroup.
* `avg by (instance) (...)` — groups across CPUs so you get one number per host instead of one per core.

---

## Alert Rules

Defined in `prometheus/rules/alerts.yml`:

| Alert            | Expression                                                              | For   | Severity |
| ---------------- | ----------------------------------------------------------------------- | ----- | -------- |
| InstanceDown     | `up == 0`                                                               | 1m    | critical |
| HighCPUUsage     | host CPU > 80%                                                          | 5m    | warning  |
| HighMemoryUsage  | available memory < 15%                                                  | 5m    | warning  |

`for:` means the expression must stay true continuously for that duration before firing. Avoids flapping on transient spikes. View at http://localhost:9090/alerts.

> This lab does **not** include Alertmanager — alerts are visible in the Prometheus UI but no notifications are sent. Adding Alertmanager is a natural next step.

---

## Useful Commands

```bash
# Validate prometheus.yml + rules with promtool
bash scripts/validate-config.sh

# List every target with health + last scrape error
bash scripts/check-targets.sh

# Hot-reload Prometheus after editing config (no restart)
bash scripts/reload-prometheus.sh

# Tail logs
docker compose logs -f prometheus
docker compose logs -f cadvisor

# Exec into Prometheus container
docker compose exec prometheus /bin/sh

# Run promtool ad-hoc against a query
docker compose exec prometheus promtool query instant http://localhost:9090 'up'

# Stop a service to test InstanceDown alert
docker compose stop node-exporter

# Bring everything down (keep volumes)
docker compose down

# Bring everything down AND wipe TSDB + Grafana state
docker compose down -v
```

> **Windows users:** the `.sh` scripts assume Bash. Run them from Git Bash or WSL, or invoke the underlying `docker` / `curl` commands directly from PowerShell.

---

## Troubleshooting

**Target shows DOWN on /targets**
1. `docker compose ps` — is the target service running and healthy?
2. From the prometheus container, can you reach the target?
   `docker compose exec prometheus wget -qO- http://node-exporter:9100/metrics | head`
3. Check `lastError` in `bash scripts/check-targets.sh`.

**Grafana datasource fails with "connection refused"**
* Make sure you used `http://prometheus:9090` (Compose DNS), **not** `http://localhost:9090`. Inside Grafana's container, `localhost` is Grafana itself.

**cAdvisor crashes / no container metrics on Linux**
* SELinux or AppArmor may be blocking the host mounts. Try `:z` mount flag on SELinux systems, or add the container to AppArmor's unconfined profile.
* On cgroup v2 systems older cAdvisor versions misreport; v0.49.x supports both.

**cAdvisor on Docker Desktop (Mac/Windows)**
* The host mounts point at the **VM** Docker Desktop runs, not your real host. Container metrics work; host-level metrics from node-exporter will reflect the VM, not macOS/Windows. This is fine for learning.

**Edited prometheus.yml but Prometheus didn't pick it up**
* Run `bash scripts/reload-prometheus.sh`. If it returns an error, your YAML is invalid — `validate-config.sh` will tell you where.

**Port already in use**
* Something else is on 9090 / 3000 / 9100 / 8080. Either stop it or remap the left side of `ports:` in `docker-compose.yml` (e.g. `"19090:9090"`).

---

## Things to Experiment With

These are the point of the lab. Break things, watch the metrics react.

1. **Trigger InstanceDown.** `docker compose stop node-exporter`. Watch http://localhost:9090/targets show DOWN, wait 1 minute, see `InstanceDown` go FIRING on /alerts. Start it again with `docker compose start node-exporter`.

2. **Generate CPU load.** On Linux: `docker run --rm -it polinux/stress stress --cpu 4 --timeout 600s`. Watch `100 * (1 - avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))` in Prometheus, and after 5 minutes see `HighCPUUsage` fire.

3. **Inspect labels.** Add `team: platform` under `node-exporter`'s `static_configs.labels`. Run `bash scripts/reload-prometheus.sh`. Query `up{team="platform"}` — see the new dimension appear.

4. **Change scrape_interval.** Set it to `1s`. Reload. Watch `prometheus_tsdb_head_samples_appended_total` rate go up. Set it to `30s` — see graphs become coarser. Pick the right tradeoff for your prod workload.

5. **Break a config on purpose.** Indent something wrong in `prometheus.yml`. Run `bash scripts/validate-config.sh` — read the error. Fix it. Reload.

6. **Add a doomed scrape target.** Add `targets: ["does-not-exist:9999"]` to a job. Reload. Watch it appear on /targets as DOWN with a DNS error in `lastError`. Remove it.

7. **Query in Grafana Explore.** Build the CPU-usage panel from the PromQL above. Save as a dashboard JSON, drop it in `grafana/dashboards/` — it auto-provisions under the "Lab" folder.

8. **Watch a counter reset.** Restart node-exporter. Graph `node_cpu_seconds_total{mode="user"}` (raw, no `rate`) — see the line drop to zero. Now graph `rate(node_cpu_seconds_total{mode="user"}[1m])` — see that `rate()` handles the reset cleanly. This is why you always wrap counters in `rate()`.

---

## Stop / Cleanup

```bash
docker compose down       # stop containers, keep TSDB + Grafana volumes
docker compose down -v    # wipe everything including stored metrics + dashboards
```

---

## Next Steps

* Add **Alertmanager** for real notifications (Slack, email, PagerDuty).
* Add a second Prometheus and explore **federation**.
* Replace `static_configs` with **file_sd_configs** or **dns_sd_configs** for dynamic targets.
* Move to **Kubernetes** with the Prometheus Operator / kube-prometheus-stack — covered in the next labs in this repo.
