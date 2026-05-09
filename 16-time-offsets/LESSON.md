# **Understanding Time Offset in Prometheus**

In this lecture, we learn about an important Prometheus concept called **time offset**.

Normally, when we query a metric in Prometheus, we receive the **latest scraped values** for that metric.

Example:

```promql id="m4x8tv"
prometheus_http_requests_total
```

This query returns the most recent time series values for the metric.

We can also add optional label filters:

```promql id="k7r2wp"
prometheus_http_requests_total{code="200"}
```

---

# **What Is Time Offset?**

Sometimes we do not want the latest metric values.

Instead, we may want:

* Values from 5 minutes ago
* Values from 1 hour ago
* Values from several days ago

Prometheus provides the `offset` keyword for this purpose.

---

# **Offset Syntax**

General syntax:

```promql id="t3n6qy"
metric_name offset time
```

Example:

```promql id="z1v9md"
prometheus_http_requests_total offset 10m
```

This returns the metric values from **10 minutes ago**.

---

# **Supported Time Units**

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

# **Examples**

## **10 Minutes Ago**

```promql id="c8p4rk"
prometheus_http_requests_total offset 10m
```

---

## **8 Hours Ago**

```promql id="j2x7nb"
prometheus_http_requests_total offset 8h
```

---

## **10 Days Ago**

```promql id="f5w1tz"
prometheus_http_requests_total offset 10d
```

If Prometheus does not have data that old, no results will be returned.

---

# **Comparing Current and Historical Values**

Example:

Without offset:

```promql id="v9k3mq"
prometheus_http_requests_total
```

Current value:

```text id="b4r6yn"
21
```

With offset:

```promql id="q7m2xp"
prometheus_http_requests_total offset 8m
```

Historical value:

```text id="g1t5wc"
20
```

This shows that:

* Current scrape value = `21`
* Value 8 minutes ago = `20`

---

# **Viewing Metrics as Graphs**

Prometheus can display instant vectors as graphs.

When you execute a query:

1. Results first appear as a table
2. You can switch to the **Graph** tab
3. Each time series can be visualized separately

Some graphs are:

* Flat (values do not change)
* Dynamic (values change over time)

---

# **Adding Multiple Panels**

Prometheus allows multiple graph panels.

You can:

* Click **Add Panel**
* Add new queries
* View multiple graphs simultaneously

---

# **Important: Graphs Work Only with Instant Vectors**

Prometheus graphs require **instant vectors**.

If you use a **range vector**, the graph will fail.

Example:

```promql id="x4d9qb"
prometheus_http_requests_total[5m]
```

This creates a range vector.

Prometheus returns an error because range vectors cannot be directly graphed in this view.

---

# **Using Aggregation with Graphs**

Suppose we use:

```promql id="p8v2kc"
group by(code)(prometheus_http_requests_total)
```

We receive multiple rows grouped by `code`.

However:

* `group()` always returns value `1`
* Every graph becomes a flat line at `1`

---

# **Using Useful Aggregations**

Instead of `group`, we usually use:

* `avg`
* `sum`
* `count`
* `max`
* `min`

Example:

```promql id="r6m1wd"
avg by(code)(prometheus_http_requests_total)
```

Now each graph displays meaningful values.

---

# **Combining Offset with Aggregation**

Suppose we want:

* The average value
* Grouped by `code`
* From 8 hours ago

Correct query:

```promql id="n5q7tz"
avg by(code)(
  prometheus_http_requests_total offset 8h
)
```

---

# **Important Rule About `offset`**

The `offset` keyword must always be applied:

✅ Directly after the metric name

Correct:

```promql id="h2x8pv"
metric_name offset 8h
```

---

# **Incorrect Usage**

❌ Wrong:

```promql id="d4w9mc"
avg(metric_name) offset 8h
```

❌ Wrong:

```promql id="s1r6yk"
avg by(code)(metric_name) offset 8h
```

These produce errors.

---

# **Why?**

Because:

* `offset` modifies the metric data itself
* Aggregation functions operate on the result returned by the metric

The order is:

1. Fetch metric data
2. Apply offset
3. Apply aggregation
4. Apply grouping

---

# **Correct Query Flow**

```text id="u7v3nd"
metric → offset → aggregation → grouping
```

---

# **Final Example**

```promql id="k9m4wx"
avg by(code)(
  prometheus_http_requests_total offset 8h
)
```

This query:

1. Retrieves `prometheus_http_requests_total`
2. Uses values from 8 hours ago
3. Calculates averages
4. Groups results by `code`

---

# **Key Takeaways**

* `offset` retrieves historical metric values
* It must be placed directly after the metric
* Prometheus graphs work only with instant vectors
* `group()` always returns value `1`
* Aggregation operators like `avg` and `sum` are more useful for graphing
* Aggregations can be combined with offsets for historical analysis
