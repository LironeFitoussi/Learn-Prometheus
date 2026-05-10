# **Installing Node Exporter on macOS Using Homebrew**

In this lesson, we will learn how to install and configure **Node Exporter** on a macOS machine using [Homebrew](https://brew.sh?utm_source=chatgpt.com).

This setup allows you to:

* collect system metrics locally
* expose metrics to [Prometheus](https://prometheus.io?utm_source=chatgpt.com)
* practice Prometheus monitoring on your own Mac without needing another server

> Note:
> If you are not using macOS or do not want to install Node Exporter locally, you can safely skip this lesson.

---

# **What Is Node Exporter?**

**Node Exporter** is a Prometheus exporter that collects system-level metrics such as:

* CPU usage
* memory usage
* disk utilization
* filesystem statistics
* network metrics

It exposes these metrics through an HTTP endpoint that Prometheus can scrape.

---

# **Prerequisites**

Before continuing, you should already have:

* [Homebrew](https://brew.sh?utm_source=chatgpt.com) installed
* [Prometheus](https://prometheus.io?utm_source=chatgpt.com) installed via Homebrew

---

# **1. Install Node Exporter**

Open the terminal and run:

```bash id="j8s13p"
brew install node_exporter
```

This installs Node Exporter on your Mac.

---

# **2. Start Node Exporter as a Service**

One advantage of installing via Homebrew is that you can easily run Node Exporter as a background service.

Run:

```bash id="q2b5mv"
brew services start node_exporter
```

---

# **3. Verify Node Exporter Is Running**

Open your browser and visit:

```text id="d6yr6o"
http://localhost:9100
```

You should see the Node Exporter landing page.

---

## **View Metrics**

Click:

```text id="v9h2fx"
Metrics
```

Or open directly:

```text id="r9zmrp"
http://localhost:9100/metrics
```

You will see all metrics exposed by Node Exporter.

Examples include:

* CPU metrics
* memory statistics
* filesystem data
* network metrics

These metrics are now available for Prometheus to scrape.

---

# **4. Configure Prometheus to Scrape Node Exporter**

Now we must add Node Exporter as a scrape target inside the Prometheus configuration.

---

# **Locate the Prometheus Configuration File**

When Prometheus is installed with Homebrew, its configuration file is usually located at:

```text id="d31g08"
/usr/local/etc/prometheus.yml
```

---

# **How to Access the Folder**

## **Using Finder**

1. Open **Finder**
2. Navigate to:

```text id="yl6m0l"
/usr/local/etc
```

---

## **If the `/usr` Folder Is Hidden**

Press:

```text id="g2fxr0"
Command + Shift + G
```

Then type:

```text id="n9sq6w"
/usr
```

This opens the hidden system folder.

---

# **5. Edit `prometheus.yml`**

Open the file using:

* TextEdit
* Visual Studio Code
* any text editor

---

## **Existing Scrape Configuration**

Inside the file, you will already see a scrape job for Prometheus itself.

Duplicate that existing job and modify it for Node Exporter.

---

## **Example Configuration**

```yaml id="j5r9xg"
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node_exporter"
    static_configs:
      - targets: ["localhost:9100"]
```

---

# **6. Save the File**

After adding the Node Exporter scrape configuration:

1. Save the file
2. Close the editor

---

# **7. Restart Prometheus**

Return to the terminal and restart Prometheus.

The lecture recommends stopping and starting instead of using restart.

---

## **Stop Prometheus**

```bash id="p7gxtm"
brew services stop prometheus
```

---

## **Start Prometheus**

```bash id="u8r5jv"
brew services start prometheus
```

---

# **8. Verify Targets in Prometheus**

Open Prometheus in your browser:

```text id="2m4r4i"
http://localhost:9090
```

---

## **Check Targets**

Inside Prometheus:

1. Open the **Status** menu
2. Click **Targets**

You should now see:

| Target        | Status |
| ------------- | ------ |
| Prometheus    | UP     |
| Node Exporter | UP     |

Both targets should appear:

* green
* healthy
* active

---

# **Why This Setup Is Useful**

With this local setup, you can:

* practice Prometheus queries
* test Grafana dashboards
* learn PromQL
* monitor your own Mac
* experiment without needing cloud servers or virtual machines

This is an excellent environment for:

* learning observability
* testing dashboards
* experimenting with alerts

---

# **Useful Ports**

| Service       | Port   |
| ------------- | ------ |
| Prometheus    | `9090` |
| Node Exporter | `9100` |

---

# **Key Takeaways**

## **Install Node Exporter**

```bash id="5jrm9j"
brew install node_exporter
```

---

## **Start Node Exporter**

```bash id="6w6tgm"
brew services start node_exporter
```

---

## **Node Exporter Metrics URL**

```text id="a5b53t"
http://localhost:9100/metrics
```

---

## **Prometheus UI**

```text id="7czl7p"
http://localhost:9090
```

---

## **Prometheus Configuration File**

```text id="1c2qnh"
/usr/local/etc/prometheus.yml
```

---

This setup provides a complete local monitoring environment using:

* [Prometheus](https://prometheus.io?utm_source=chatgpt.com)
* [Node Exporter](https://github.com/prometheus/node_exporter?utm_source=chatgpt.com)
* [Homebrew](https://brew.sh?utm_source=chatgpt.com)
* [Grafana](https://grafana.com?utm_source=chatgpt.com)
