# **Prometheus Functions – `log2`, `log10`, `ln`, `sort`, `sort_desc`, `time`, and `timestamp`**

In this lesson, we will learn several useful Prometheus functions related to:

* logarithmic calculations
* sorting vectors
* working with timestamps and time data

The functions covered are:

* **`log2()`**
* **`log10()`**
* **`ln()`**
* **`sort()`**
* **`sort_desc()`**
* **`time()`**
* **`timestamp()`**

These functions are frequently used in:

* metric analysis
* dashboard visualization
* data normalization
* debugging
* time-based monitoring

---

# **1. The `log2()` Function**

The **`log2()`** function calculates the **binary logarithm** of every scalar value in an instant vector.

---

## **Syntax**

```promql id="9hyjtw"
log2(vector)
```

---

## **Behavior**

The function transforms each value using:

```text id="xjtvqj"
log₂(value)
```

---

## **Example**

```promql id="2zk5nm"
log2(metric_name)
```

If one item has value:

```text id="0h9mql"
2
```

The result becomes:

```text id="x9k3ka"
1
```

Because:

```text id="g2q6xj"
log₂(2) = 1
```

---

# **2. The `log10()` Function**

The **`log10()`** function calculates the **base-10 logarithm** of every scalar value in an instant vector.

---

## **Syntax**

```promql id="u6p8vq"
log10(vector)
```

---

## **Behavior**

The function transforms each value using:

```text id="5b75z0"
log₁₀(value)
```

---

## **Example**

```promql id="c6g07t"
log10(metric_name)
```

If one item has value:

```text id="v8zjlwm"
10
```

The result becomes:

```text id="lq7dnf"
1
```

Because:

```text id="mpx0mp"
log₁₀(10) = 1
```

---

# **3. The `ln()` Function**

The **`ln()`** function calculates the **natural logarithm** of each scalar value in an instant vector.

> Important:
> It is written as lowercase `ln`, not uppercase `LN`.

---

## **Syntax**

```promql id="s8oclh"
ln(vector)
```

---

## **Behavior**

The function applies:

```text id="2od3bi"
natural logarithm (base e)
```

to every value in the vector.

---

## **Example**

```promql id="t0ff0n"
ln(metric_name)
```

If a value equals:

```text id="m9g4tt"
2.718
```

The result will be approximately:

```text id="7yjlwm"
1
```

Because:

```text id="4kcfm6"
ln(e) = 1
```

---

# **4. The `sort()` Function**

The **`sort()`** function sorts all elements in an instant vector in **ascending order** based on their values.

---

## **Syntax**

```promql id="gx0mbx"
sort(vector)
```

---

## **Example**

```promql id="yv7mzn"
sort(clamp(node_cpu_seconds_total, 300, 150000))
```

### Result

The values start from the smallest:

```text id="g7fy6r"
300 → ... → 150000
```

---

# **5. The `sort_desc()` Function**

The **`sort_desc()`** function sorts vector elements in **descending order**.

---

## **Syntax**

```promql id="lbhkw0"
sort_desc(vector)
```

---

## **Example**

```promql id="a4w3wt"
sort_desc(clamp(node_cpu_seconds_total, 300, 150000))
```

### Result

The values start from the largest:

```text id="z2dw29"
150000 → ... → 300
```

---

# **6. The `time()` Function**

The **`time()`** function returns the current Unix timestamp.

---

## **Syntax**

```promql id="8t3cvz"
time()
```

---

## **Important Note**

The returned value is:

* close to the current time
* but not guaranteed to be the exact current timestamp

This is because Prometheus evaluates queries at specific execution times.

---

## **Example Result**

```text id="s9p7mz"
1715342400
```

This represents a Unix timestamp.

---

# **7. The `timestamp()` Function**

The **`timestamp()`** function returns the timestamp associated with every sample in an instant vector.

---

## **Syntax**

```promql id="8tx9yw"
timestamp(vector)
```

---

## **Behavior**

For every metric sample, Prometheus returns:

* the time when the sample was collected

instead of the sample value itself.

---

## **Example**

```promql id="df8mrq"
timestamp(node_cpu_seconds_total)
```

The returned values are timestamps representing when each metric sample was captured.

---

# **Using `offset` with `timestamp()`**

You can combine `offset` with metrics to inspect older samples.

---

## **Example**

```promql id="0xg9cn"
timestamp(node_cpu_seconds_total offset 1h)
```

---

## **Result**

The timestamps returned will correspond to:

```text id="r3jkqg"
one hour before the current query time
```

This is useful when:

* comparing historical data
* debugging delayed metrics
* analyzing past samples

---

# **Practical Use Cases**

## **Logarithmic Functions**

Useful for:

* data normalization
* exponential growth analysis
* visualization scaling

---

## **Sorting Functions**

Useful for:

* ranking metrics
* identifying highest or lowest values
* dashboard tables

---

## **Time Functions**

Useful for:

* debugging sample collection
* historical comparisons
* time-aware monitoring

---

# **Key Takeaways**

## **`log2()`**

* Binary logarithm
* Base 2

---

## **`log10()`**

* Decimal logarithm
* Base 10

---

## **`ln()`**

* Natural logarithm
* Base e

---

## **`sort()`**

* Ascending order

---

## **`sort_desc()`**

* Descending order

---

## **`time()`**

* Returns current Unix timestamp

---

## **`timestamp()`**

* Returns sample collection timestamps

---

These functions are commonly used in:

* [Prometheus](https://prometheus.io?utm_source=chatgpt.com) queries
* [Grafana](https://grafana.com?utm_source=chatgpt.com) dashboards
* monitoring systems
* observability workflows
* metric debugging
