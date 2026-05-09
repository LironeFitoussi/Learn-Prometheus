# **Prometheus Data Types and PromQL Basics**

Prometheus includes its own query language called:

# **PromQL (Prometheus Query Language)**

PromQL is used to retrieve and analyze metrics stored inside Prometheus. Before learning PromQL deeply, it is important to understand the core Prometheus data types. 

---

# **1. Prometheus Data Types**

The lesson introduces three important concepts:

1. Scalar
2. Instant Vector
3. Range Vector

---

# **2. Scalar Data Type**

A scalar represents:

* A single numeric value
* Or a string value

---

## Float Values

In Prometheus:

```text id="k0ozjo"
1
1.5
100
```

are all treated as:

# **Float Values**

Even integers are internally considered floats.

---

## String Values

Strings are enclosed in quotes:

```text id="o2yefc"
"200"
```

or

```text id="prag0m"
'200'
```

Both single and double quotes are valid.

---

# **3. Example Metric with Labels**

Example metric:

```text id="eh3tmh"
prometheus_http_requests_total{code="200", job="prometheus"}
```

---

## Breakdown

| Component                        | Meaning     |
| -------------------------------- | ----------- |
| `prometheus_http_requests_total` | Metric name |
| `code="200"`                     | Label       |
| `job="prometheus"`               | Label       |

---

# **4. String Matching in PromQL**

Suppose we run:

```text id="tibm1s"
prometheus_http_requests_total{job="prometheus", code=~"2.*"}
```

Explanation:

| Part     | Meaning       |
| -------- | ------------- |
| `code=~` | Regex match   |
| `"2.*"`  | Starts with 2 |

This matches:

* 200
* 201
* 204
* 299

---

# **5. Why String Labels Are Useful**

String labels allow:

* Pattern matching
* Flexible filtering
* Regex searches

Without strings, regex filtering would not work effectively.

---

# **6. Type Mismatch Example**

This query will NOT work correctly:

```text id="1q11uk"
prometheus_http_requests_total{code=200}
```

Why?

Because:

```text id="nhh3s7"
code="200"
```

was stored as a string, not a numeric value.

Prometheus label values are fundamentally strings.

---

# **7. Instant Vectors**

An instant vector returns:

# **One Sample Per Time Series**

At a single timestamp.

---

## Simple Instant Vector Query

```text id="g70v23"
auth_api_hit
```

This returns:

* Current/latest sampled value
* For all matching time series

---

# **8. Instant Vector Example**

Example result:

```text id="98n8es"
auth_api_hit = 5101
```

This is called an:

# **Instant Vector**

because only one value is returned per series.

---

# **9. Filtering Instant Vectors**

You can filter using labels:

```text id="mdt8cr"
auth_api_hit{count="1", time_taken="800"}
```

This returns only metrics matching:

* `count="1"`
* `time_taken="800"`

---

# **10. Range Vectors**

A range vector returns:

# **Multiple Samples Over Time**

Instead of one value, you get a collection of values.

---

# **11. Range Syntax**

Range vectors use square brackets:

```text id="z0djlwm"
metric_name[time]
```

Example:

```text id="tm88e7"
auth_api_hit[5m]
```

Meaning:

```text id="58goq1"
Last 5 minutes
```

---

# **12. Important Time Units**

| Unit | Meaning      |
| ---- | ------------ |
| `ms` | Milliseconds |
| `s`  | Seconds      |
| `m`  | Minutes      |
| `h`  | Hours        |
| `d`  | Days         |
| `w`  | Weeks        |
| `y`  | Years        |

---

# **13. Important Notes About Time Ranges**

Prometheus always interprets ranges as:

# **Past Time**

Example:

```text id="xt4i5f"
[5m]
```

means:

```text id="mf8q4k"
5 minutes before now
```

There is no negative time syntax like:

```text id="l5om7f"
[-5m]
```

---

# **14. Example Using Real Metrics**

Example metric:

```text id="p1wnwz"
node_network_transmit_errs_total
```

---

## Instant Vector Query

```text id="uhlr0s"
node_network_transmit_errs_total
```

Returns:

* One latest value per device/interface

Example labels:

```text id="m5rxg5"
device="ap1"
device="dl0"
```

Each unique label combination creates a separate time series.

---

# **15. Range Vector Query**

Example:

```text id="rm2hn8"
node_network_transmit_errs_total[5m]
```

Now each series returns:

* Multiple timestamped values
* Covering the last 5 minutes

---

# **16. Why It Is Called a Vector**

A vector means:

# **A Collection of Values**

So:

| Type           | Returned Data   |
| -------------- | --------------- |
| Instant Vector | One value       |
| Range Vector   | Multiple values |

---

# **17. What Determines Number of Returned Samples?**

Two major factors:

---

## 1. Query Time Range

Example:

```text id="w2knsl"
[5m]
[1h]
[7d]
```

Longer range → More samples.

---

## 2. Scrape Interval**

Configured in:

```text id="39i5o8"
prometheus.yml
```

Default:

```text id="w5vcx7"
15 seconds
```

---

# **18. Example Calculation**

If:

* Scrape interval = 15 seconds
* Query range = 5 minutes

Then approximately:

```text id="rtb2s7"
300 / 15 = 20 samples
```

will be returned per time series.

---

# **19. Prometheus UI Behavior**

When querying metrics in the Prometheus UI:

* Instant vectors show one value per series
* Range vectors show many values per series

This is why graphs become possible.

---

# **20. Summary of Data Types**

| Data Type      | Description                |
| -------------- | -------------------------- |
| Scalar         | Single number/string       |
| Instant Vector | One sample per series      |
| Range Vector   | Multiple samples over time |

---

# **21. Key Takeaways**

* PromQL is Prometheus’s query language
* Labels are stored as strings
* Instant vectors return one value
* Range vectors return many timestamped values
* Time ranges use square brackets
* Sample count depends on scrape interval and range duration
* Understanding vectors is essential before writing advanced PromQL queries

