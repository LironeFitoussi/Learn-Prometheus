# **How Prometheus Collects Metrics**

After installing Prometheus, the next step is understanding **how metrics and data are collected and stored** inside Prometheus. 

Prometheus mainly works using a **pull-based architecture**, where it periodically connects to systems and retrieves metrics.

---

# **1. Direct Application Instrumentation**

One way to send metrics to Prometheus is through the application itself.

## How It Works

If you have access to the application's source code, you can:

* Add a Prometheus client library
* Collect metrics inside the application
* Expose those metrics for Prometheus

Prometheus supports libraries for many languages:

* Python
* Java
* Ruby
* .NET
* Go
* Node.js

---

## Example Architecture

```text id="2mdx4x"
Application → Prometheus Client Library → Prometheus
```

This approach works well when:

* You own the application
* You can modify the source code
* You can deploy updated code

---

# **2. The Problem with Third-Party Systems**

Many systems cannot be modified directly.

Examples include:

* MySQL databases
* HAProxy load balancers
* Amazon CloudWatch
* Linux servers
* Windows servers
* IoT devices

For these systems:

* You do not control the source code
* You cannot add Prometheus libraries

---

# **3. Why Manual Scripts Are Not Ideal**

One possible solution is writing scripts such as:

* Bash scripts
* PowerShell scripts

These scripts could:

1. Collect metrics
2. Run on schedules
3. Send data somewhere

Usually using:

* Cron jobs (Linux)
* Scheduled Tasks (Windows)

---

## Limitations of Script-Based Collection

This approach has major problems:

* Difficult to maintain
* Hard to scale
* Inefficient for large infrastructures
* Complicated with thousands or millions of devices

---

# **4. Prometheus Exporters**

Prometheus solves this problem using **Exporters**.

An exporter is a service that:

1. Collects metrics from a system
2. Converts them into Prometheus format
3. Exposes them through an HTTP endpoint

Prometheus then retrieves the metrics from the exporter.

---

# **5. Exporter Architecture**

```text id="e2x83z"
Target System → Exporter → Prometheus
```

Prometheus never talks directly to many systems.

Instead:

* The exporter acts as a translator
* Prometheus pulls metrics from exporters

---

# **6. Common Types of Exporters**

There are exporters for many technologies.

| Exporter Type       | Purpose                |
| ------------------- | ---------------------- |
| Node Exporter       | Linux server metrics   |
| Windows Exporter    | Windows metrics        |
| MySQL Exporter      | Database metrics       |
| HAProxy Exporter    | Load balancer metrics  |
| CloudWatch Exporter | AWS monitoring metrics |
| Blackbox Exporter   | Endpoint probing       |
| SNMP Exporter       | Network devices        |

---

# **7. IoT and Large-Scale Monitoring**

Prometheus exporters are especially useful for:

* Sensors
* Traffic systems
* Smart buildings
* Industrial monitoring
* Large IoT deployments

---

## Why Push Directly Is a Problem

Imagine:

* 1 million IoT devices
* Each pushing data constantly

This could overload Prometheus completely.

---

# **8. Prometheus Uses Pull, Not Push**

Prometheus is fundamentally a **pull-based** monitoring system.

This means:

* Prometheus initiates the connection
* Prometheus requests the metrics
* Systems do not send data directly to Prometheus

---

# **9. Scraping**

The process of Prometheus collecting metrics is called:

# **Scraping**

During scraping:

1. Prometheus connects to an exporter
2. Reads the metrics endpoint
3. Stores the metrics internally

---

# **10. Scrape Interval**

Scraping frequency is configured in the Prometheus configuration file.

Default scrape interval:

```text id="v83tpg"
15 seconds
```

So every 15 seconds:

```text id="q5wq4q"
Prometheus → Exporter → Metrics Collected
```

---

# **11. Push Gateway**

Sometimes applications cannot expose metrics for scraping.

In such cases, Prometheus uses a component called:

# **Pushgateway**

---

# **12. What Pushgateway Does**

Pushgateway acts as:

* Temporary storage for pushed metrics
* An intermediary between applications and Prometheus

Applications push metrics to Pushgateway.

Prometheus still pulls metrics from Pushgateway.

---

# **13. Pushgateway Architecture**

```text id="2h7hgf"
Application → Pushgateway → Prometheus
```

Important:

> Prometheus itself still remains a pull-based system.

---

# **14. Why Pushgateway Exists**

Pushgateway is useful for:

* Short-lived jobs
* Batch processes
* Scheduled tasks
* Temporary workloads

Examples:

* Backup jobs
* CI/CD pipelines
* One-time scripts

---

# **15. Key Difference: Push vs Pull**

| Pull Model                    | Push Model            |
| ----------------------------- | --------------------- |
| Prometheus requests metrics   | Systems send metrics  |
| Better scalability            | Harder to control     |
| Easier centralized monitoring | Risk of overload      |
| Native Prometheus model       | Not native Prometheus |

Prometheus always prefers:

# **Pull-Based Monitoring**

---

# **16. Complete Monitoring Flow**

## Using Exporters

```text id="jnh2ig"
Linux Server → Node Exporter → Prometheus
MySQL → MySQL Exporter → Prometheus
HAProxy → HAProxy Exporter → Prometheus
```

---

## Using Pushgateway

```text id="94iqrw"
Application → Pushgateway → Prometheus
```

---

# **17. Important Concepts**

## Exporter

A service that exposes metrics in Prometheus format.

---

## Scraping

Prometheus pulling metrics from targets.

---

## Pushgateway

A temporary bridge for push-based applications.

---

# **18. Summary**

Prometheus supports two major monitoring approaches:

## Pull via Exporters

Best for:

* Infrastructure
* Servers
* Databases
* Third-party systems

---

## Push via Pushgateway

Best for:

* Batch jobs
* Temporary applications
* Short-lived processes

---

# **Key Takeaways**

* Prometheus is primarily a **pull-based monitoring system**
* Exporters expose metrics for Prometheus scraping
* Scraping happens periodically (default: every 15 seconds)
* Pushgateway allows applications to push metrics indirectly
* Exporters make Prometheus highly scalable across complex infrastructures
