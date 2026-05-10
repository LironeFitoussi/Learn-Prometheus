# **Prometheus Aggregation Over Time Functions**

In this lesson, we will learn about a very important group of Prometheus functions called:

# **Aggregation Over Time Functions**

These functions are essentially the same as Prometheus aggregation operators, but designed specifically for **range vectors** instead of instant vectors.

For example:

| Instant Vector Function | Range Vector Equivalent |
| ----------------------- | ----------------------- |
| `avg()`                 | `avg_over_time()`       |
| `sum()`                 | `sum_over_time()`       |
| `min()`                 | `min_over_time()`       |
| `max()`                 | `max_over_time()`       |
| `count()`               | `count_over_time()`     |

These functions are extremely useful for:

* historical analysis
* trend monitoring
* dashboard visualization
* smoothing metrics over time
* statistical calculations

They are heavily used in:

* [Prometheus](https://prometheus.io?utm_source=chatgpt.com)
* [Grafana](https://grafana.com?utm_source=chatgpt.com) dashboards

---

# **Understanding the Difference**

## **Aggregation Operators**

Functions like:

```promql id="v1q8ap"
avg()
sum()
min()
max()
```

work on:

```text id="zlh1fu"
Instant vectors
```

---

## **Aggregation Over Time Functions**

Functions like:

```promql id="l7n71k"
avg_over_time()
sum_over_time()
min_over_time()
```

work on:

```text id="52dwcq"
Range vectors
```

---

# **1. `avg_over_time()`**

The **`avg_over_time()`** function calculates the average value of all samples within a time range.

---

## **Syntax**

```promql id="yj4d3t"
avg_over_time(metric[range])
```

---

## **Example**

```promql id="0q9o0r"
avg_over_time(node_cpu_seconds_total[2h])
```

---

## **What It Does**

This query:

* looks at the last 2 hours
* calculates the average value
* for each unique time series

---

# **Why `avg()` Fails with Range Vectors**

Suppose you run:

```promql id="cw11h3"
avg(node_cpu_seconds_total[2h])
```

This produces an error because:

```text id="3q4gvu"
avg() only accepts instant vectors
```

The `[2h]` converts the metric into a:

```text id="6kq99n"
Range vector
```

So you must use:

```promql id="6c3l1l"
avg_over_time()
```

instead.

---

# **2. `sum_over_time()`**

The **`sum_over_time()`** function calculates the sum of all samples within a time range.

---

## **Syntax**

```promql id="y3wq2v"
sum_over_time(metric[range])
```

---

## **Example**

```promql id="b84tw9"
sum_over_time(node_network_receive_bytes_total[1h])
```

This calculates the total accumulated values during the last hour.

---

# **3. `min_over_time()`**

The **`min_over_time()`** function returns the minimum value found within the specified time range.

---

## **Syntax**

```promql id="r8bg0z"
min_over_time(metric[range])
```

---

## **Example**

```promql id="f5q1xj"
min_over_time(node_memory_usage_bytes[24h])
```

This returns the lowest memory usage value during the last 24 hours.

---

# **4. `max_over_time()`**

The **`max_over_time()`** function returns the maximum value within the selected range.

---

## **Syntax**

```promql id="x7h21t"
max_over_time(metric[range])
```

---

## **Example**

```promql id="9ruw7g"
max_over_time(node_cpu_temp_celsius[6h])
```

This returns the highest CPU temperature recorded during the last 6 hours.

---

# **5. `count_over_time()`**

The **`count_over_time()`** function counts the number of samples inside a range vector.

---

## **Syntax**

```promql id="2eqe4v"
count_over_time(metric[range])
```

---

## **Example**

```promql id="6cz7z6"
count_over_time(node_cpu_seconds_total[1h])
```

This returns how many samples were collected during the last hour.

---

# **Statistical Over Time Functions**

Prometheus also provides statistical aggregation functions over time.

---

# **`stddev_over_time()`**

Calculates the:

```text id="6wx6e7"
Standard deviation
```

within a time range.

---

## **Example**

```promql id="9c8vhm"
stddev_over_time(metric[1h])
```

Useful for:

* anomaly detection
* measuring variability
* identifying unstable metrics

---

# **`stdvar_over_time()`**

Calculates the:

```text id="6mpz7k"
Statistical variance
```

within a time range.

---

## **Example**

```promql id="pxm4bp"
stdvar_over_time(metric[1h])
```

---

# **Filtering Before Aggregation**

You can filter metrics before applying aggregation-over-time functions.

---

## **Example**

```promql id="5zq7sn"
avg_over_time(node_cpu_seconds_total{cpu="0"}[2h])
```

---

## **What Happens Here**

This query:

1. Selects only metrics where:

```text id="y6gwrx"
cpu="0"
```

2. Looks at the last 2 hours

3. Calculates the average value for each matching series

---

# **Practical Use Cases**

## **`avg_over_time()`**

Useful for:

* smoothing noisy metrics
* average CPU utilization
* long-term trends

---

## **`sum_over_time()`**

Useful for:

* total traffic analysis
* accumulated metrics
* throughput monitoring

---

## **`min_over_time()` / `max_over_time()`**

Useful for:

* detecting spikes
* identifying peaks
* finding lowest values

---

## **`count_over_time()`**

Useful for:

* checking scrape frequency
* identifying missing samples
* monitoring collection intervals

---

# **Key Takeaways**

## **Aggregation Functions**

Work on:

```text id="nff30m"
Instant vectors
```

---

## **Aggregation Over Time Functions**

Work on:

```text id="sg16jr"
Range vectors
```

---

# **Most Common Functions**

| Function             | Purpose            |
| -------------------- | ------------------ |
| `avg_over_time()`    | Average value      |
| `sum_over_time()`    | Total sum          |
| `min_over_time()`    | Minimum value      |
| `max_over_time()`    | Maximum value      |
| `count_over_time()`  | Number of samples  |
| `stddev_over_time()` | Standard deviation |
| `stdvar_over_time()` | Variance           |

---

These functions are fundamental for:

* observability
* monitoring systems
* historical analysis
* Grafana dashboards
* Prometheus alerting rules
