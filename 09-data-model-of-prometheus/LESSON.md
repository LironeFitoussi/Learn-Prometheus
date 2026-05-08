# **Understanding the Prometheus Data Model**

Before querying metrics in Prometheus, it is important to understand how Prometheus stores data internally. 

Prometheus stores information as:

# **Time Series Data**

---

# **1. What Is a Time Series?**

A time series is:

```text id="zmy19g"
Metric + Timestamp + Value
```

This means every metric collected by Prometheus is stored together with:

* A metric name
* A value
* A timestamp

---

# **2. Prometheus Stores Metrics Over Time**

For example:

| Timestamp | CPU Usage |
| --------- | --------- |
| 10:00     | 45%       |
| 10:15     | 50%       |
| 10:30     | 40%       |

Prometheus continuously records metric values over time.

---

# **3. Every Time Series Has Two Main Parts**

In Prometheus, a time series is identified by:

1. **Metric Name**
2. **Labels**

---

# **4. Metric Name**

The metric name identifies:

* What is being measured

Examples:

```text id="igv9d5"
node_cpu_seconds_total
http_requests_total
node_memory_MemAvailable_bytes
```

---

# **5. Labels**

Labels are:

# **Key-Value Pairs**

They add additional metadata to metrics.

Format:

```text id="6e6kkg"
key="value"
```

---

# **6. General Prometheus Metric Format**

The structure looks like this:

```text id="jk1p7w"
metric_name{label="value", label="value"}
```

---

# **7. Example Structure**

```text id="t7hh3s"
http_requests_total{method="GET", status="200"}
```

Explanation:

| Part                  | Meaning     |
| --------------------- | ----------- |
| `http_requests_total` | Metric name |
| `method="GET"`        | Label       |
| `status="200"`        | Label       |

---

# **8. Labels Are Optional**

A metric can exist:

* With labels
* Without labels

---

## Without Labels

```text id="78tp8f"
up
```

---

## With Labels

```text id="c2m8f4"
up{instance="server1", job="node_exporter"}
```

---

# **9. Example from the Lesson**

Example metric:

```text id="8mfx8j"
auth_api_hit{count="1", time_taken="800"}
```

---

## Breakdown

| Component          | Meaning     |
| ------------------ | ----------- |
| `auth_api_hit`     | Metric name |
| `count="1"`        | Label       |
| `time_taken="800"` | Label       |

---

# **10. Real-World API Example**

Imagine an authentication API.

Every time:

```text id="n9zsdm"
User Login Request → API Called
```

You may track:

* Number of requests
* Response time
* HTTP status
* Region
* Service name

---

# **11. Example with More Labels**

```text id="6rk87m"
auth_api_hit{
  method="POST",
  region="eu-west",
  status="200"
}
```

Labels make metrics highly searchable and filterable.

---

# **12. Why Labels Are Powerful**

Labels allow Prometheus to:

* Filter metrics
* Aggregate metrics
* Group metrics
* Query specific dimensions

---

# **13. Labels Create Unique Time Series**

Each unique label combination becomes a separate time series.

Example:

```text id="q1jdz4"
http_requests_total{status="200"}
http_requests_total{status="500"}
```

These are treated as:

# **Two Separate Time Series**

---

# **14. Prometheus Uses Linux Timestamps**

Prometheus internally stores timestamps as:

# **Unix/Linux Timestamps**

This allows efficient storage and querying of historical data.

---

# **15. Example of a Complete Time Series**

```text id="dfjjlwm"
Metric Name: node_cpu_seconds_total
Labels: {cpu="0", mode="idle"}
Timestamp: 1715151000
Value: 1250.45
```

---

# **16. Visual Representation**

```text id="lmd1wv"
Metric Name
      ↓
node_cpu_seconds_total
      ↓
Labels
      ↓
{cpu="0", mode="idle"}
      ↓
Timestamp + Value
```

---

# **17. Important Concepts**

## Metric Name

Defines what is being measured.

---

## Label

Metadata in key-value format.

---

## Time Series

A metric with labels over time.

---

# **18. Why the Data Model Matters**

Understanding the Prometheus data model is critical because:

* Queries depend on metric names
* Filtering depends on labels
* Aggregation uses labels
* Dashboards rely on labels

Without understanding labels, PromQL becomes difficult.

---

# **19. Preview: Prometheus Data Types**

The next step after understanding the data model is learning:

# **Prometheus Metric Types**

Such as:

* Counter
* Gauge
* Histogram
* Summary

These determine how metrics behave and how they should be queried.

---

# **20. Summary**

Prometheus stores metrics as:

# **Time Series**

Each time series contains:

* A metric name
* Optional labels
* Timestamped values

---

# **Key Takeaways**

* Prometheus uses a time-series data model
* Metrics are identified by names and labels
* Labels are key-value pairs
* Each label combination creates a unique time series
* Labels make filtering and aggregation possible
* Understanding the data model is essential before learning PromQL
