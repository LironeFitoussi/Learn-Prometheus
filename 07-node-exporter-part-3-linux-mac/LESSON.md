# **Part 3 — Configure Prometheus Scraping for Node Exporter**

In Part 2, we:

✅ Created AWS infrastructure
✅ Installed Prometheus
✅ Installed Node Exporter

At this point:

* Prometheus is running on port `9090`
* Node Exporter is running on port `9100`

But Prometheus still does NOT know that Node Exporter exists.

In this part, we will configure Prometheus to:

* Discover the application server
* Scrape Node Exporter metrics
* Monitor the target
* Verify successful scraping

---

# **Architecture After Part 3**

```text id="g7m1b4"
Application Server
    ↓
Node Exporter :9100
    ↓
Prometheus Server
    ↓
Prometheus UI :9090
```

---

# **PART 3.1 — Connect to Prometheus Server**

# **1. SSH into Prometheus Server**

From your local machine:

```bash id="0j7t9m"
ssh -i prometheus-key.pem ubuntu@PROMETHEUS_PUBLIC_IP
```

---

# **2. Navigate to Prometheus Config Directory**

The Prometheus configuration file is located at:

```text id="9i5b8t"
/etc/prometheus/prometheus.yml
```

This YAML file controls:

* Scrape jobs
* Exporters
* Targets
* Intervals
* Monitoring behavior

---

# **PART 3.2 — Understand scrape_configs**

# **3. Open the Configuration File**

```bash id="0z4j3x"
sudo nano /etc/prometheus/prometheus.yml
```

---

# **4. Locate scrape_configs**

Inside the file you will see something similar to:

```yaml id="z6d5w2"
scrape_configs:
  - job_name: "prometheus"

    static_configs:
      - targets: ["localhost:9090"]
```

---

# **What Does This Mean?**

This is Prometheus scraping itself.

Prometheus includes an internal exporter automatically.

So:

```text id="x9m6s1"
Prometheus → Scrapes → Prometheus
```

This allows Prometheus to monitor its own health and performance.

---

# **5. Understanding YAML Indentation**

YAML formatting is extremely sensitive.

Even ONE extra space can break the configuration.

Important rules:

* Use spaces consistently
* Maintain indentation levels
* Do not mix tabs and spaces

---

# **Example of Correct YAML Structure**

```yaml id="9z5g2m"
scrape_configs:
  - job_name: "example"

    static_configs:
      - targets: ["1.2.3.4:9100"]
```

---

# **Common YAML Mistakes**

❌ Wrong indentation

```yaml id="7r3x5n"
scrape_configs:
-job_name: "bad"
```

❌ Mixed tabs/spaces

❌ Missing dashes

---

# **PART 3.3 — Add Node Exporter Target**

# **6. Copy Existing Job**

The easiest and safest method:

* Copy the existing Prometheus job
* Paste it below
* Modify it

This reduces indentation mistakes.

---

# **7. Add a New Scrape Job**

Under `scrape_configs`, add:

```yaml id="n7p6v2"
  - job_name: "application-server"

    static_configs:
      - targets: ["APPLICATION_PRIVATE_IP:9100"]
```

---

# **8. Replace APPLICATION_PRIVATE_IP**

Example:

```yaml id="v2m8r4"
  - job_name: "application-server"

    static_configs:
      - targets: ["172.31.15.20:9100"]
```

---

# **9. Why Use Private IPs?**

If both EC2 instances are inside the same AWS VPC:

Use:

```text id="v7x2m5"
Private IP
```

NOT public IP.

Benefits:

* Faster
* More secure
* Lower latency
* Internal AWS traffic only

---

# **Why Then to Use Public IPs**

Only use public IPs if:

* Servers are on different networks
* No private connectivity exists
* Scraping occurs over the internet

---

#**PART 3.4 — Save the Configuration**

# **10. Save the File in Nano**

Press:

```text id="d5f8r2"
CTRL + O
```

Then press:

```text id="v8m4q1"
ENTER
```

To exit:

```text id="g4x9t2"
CTRL + X
```

---

# **PART 3.5 — Restart Prometheus**

# **11. Restart the Service**

Option 1:

```bash id="f7m3v9"
sudo systemctl restart prometheus
```

---

## Alternative Stop/Start Method

Some administrators prefer:

```bash id="k8x5p2"
sudo systemctl stop prometheus
```

```bash id="s3m7w4"
sudo systemctl start prometheus
```

---

# **12. Verify Prometheus Started Correctly**

```bash id="w6p2m8"
sudo systemctl status prometheus
```

Expected:

```text id="q4n9x7"
active (running)
```

---

# **What If Prometheus Fails to Start?**

Most common reason:

# **Invalid YAML formatting**

Usually caused by:

* Incorrect indentation
* Extra spaces
* Missing dashes
* Syntax errors

---

# **13. Validate YAML Configuration**

You can validate the config using:

```bash id="t2v6r1"
promtool check config /etc/prometheus/prometheus.yml
```

Expected:

```text id="c7m3x9"
SUCCESS
```

---

# **PART 3.6 — Verify Scraping in Prometheus UI**

# **14. Open Prometheus Web UI**

In browser:

```text id="n6p4m2"
http://PROMETHEUS_PUBLIC_IP:9090
```

---

# **15. Open Targets Page**

Navigate to:

```text id="m7x3q8"
Status → Targets
```

---

# **16. Understand Targets**

Each entry under Targets represents one scrape job.

You should now see:

| Job                | Purpose                      |
| ------------------ | ---------------------------- |
| prometheus         | Prometheus monitoring itself |
| application-server | Node Exporter target         |

---

# **17. Verify Target State**

Look at the:

```text id="v4q8n1"
State
```

column.

Expected:

```text id="d2m7x9"
UP
```

Green color means:

✅ Prometheus can reach Node Exporter
✅ Metrics are being scraped successfully

---

# **PART 3.7 — Troubleshooting DOWN Targets**

# **18. If Target Shows DOWN**

Usually caused by:

| Problem               | Explanation                   |
| --------------------- | ----------------------------- |
| Wrong IP              | Incorrect target address      |
| Port blocked          | Security group/firewall issue |
| Node Exporter stopped | Service not running           |
| Wrong YAML            | Bad config                    |
| Wrong port            | Not using 9100                |

---

# **19. Verify Node Exporter Is Running**

SSH into application server:

```bash id="b6m9q4"
sudo systemctl status node_exporter
```

---

# **20. Test Connectivity from Prometheus Server**

From Prometheus server:

```bash id="x8m2p5"
curl http://APPLICATION_PRIVATE_IP:9100/metrics
```

If metrics appear:

✅ Networking works
✅ Security groups work
✅ Node Exporter works

---

# **21. Verify Security Groups**

Ensure:

| Server             | Port | Allowed From  |
| ------------------ | ---- | ------------- |
| Application Server | 9100 | prometheus-sg |

NOT:

```text id="f5v7m2"
0.0.0.0/0
```

unless temporarily testing.

---

# **PART 3.8 — Verify Metrics Collection**

# **22. Open Query Interface**

Go to:

```text id="x9p4m7"
http://PROMETHEUS_PUBLIC_IP:9090
```

---

# **23. Test Example Metrics**

## CPU Metrics

```text id="j7m3v2"
node_cpu_seconds_total
```

---

## Memory Metrics

```text id="r4x8m1"
node_memory_MemAvailable_bytes
```

---

## Disk Metrics

```text id="m2q7p5"
node_filesystem_avail_bytes
```

---

## Network Metrics

```text id="w8m5x3"
node_network_receive_bytes_total
```

Click:

```text id="k2v9m4"
Execute
```

You should now see live metric data.

---

# **24. Understanding What Happened**

The complete flow is now:

```text id="z6x3m7"
Node Exporter
    ↓ exposes metrics
:9100/metrics
    ↓
Prometheus scrapes metrics
    ↓
Prometheus stores metrics
    ↓
Prometheus UI queries metrics
```

---

# **Final State After Part 3**

You now have:

✅ AWS infrastructure configured
✅ Prometheus installed
✅ Node Exporter installed
✅ Security groups configured
✅ Scraping configured
✅ Targets UP
✅ Metrics being collected successfully

---

# **What Comes Next**

Typical next steps include:

* Installing Grafana
* Creating dashboards
* Configuring alerts
* Installing Alertmanager
* Monitoring multiple servers
* Using service discovery
* Monitoring Kubernetes clusters
