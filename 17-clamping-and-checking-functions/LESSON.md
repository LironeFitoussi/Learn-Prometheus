# **Prometheus Functions – `absent`, `absent_over_time`, and Mathematical Functions**

Now that we’ve covered **Prometheus operators**, the next important topic is **Prometheus functions**. These functions are extremely useful when building queries for dashboards, alerts, and visualizations in tools like [Grafana](https://grafana.com?utm_source=chatgpt.com).

In this lesson, we focus on:

* **`absent()`**
* **`absent_over_time()`**
* Mathematical functions like:

  * **`abs()`**
  * **`ceil()`**
  * **`floor()`**
  * **`clamp()`**
  * **`clamp_min()`**
  * **`clamp_max()`**

---

# **1. The `absent()` Function**

The **`absent()`** function checks whether an **instant vector** contains any elements.

## **Behavior of `absent()`**

This function behaves opposite to what many people initially expect:

| Input Vector         | Result                                       |
| -------------------- | -------------------------------------------- |
| Vector contains data | Returns **empty result**                     |
| Vector is empty      | Returns an **instant vector** with value `1` |

---

## **Example – Metric Exists**

Suppose we query:

```promql
node_cpu_seconds_total
```

This metric contains many values from Node Exporter.

Now wrap it inside `absent()`:

```promql
absent(node_cpu_seconds_total)
```

### Result

Since the metric exists and contains data:

```text
Empty result
```

---

## **Example – Metric Does Not Exist**

```promql
absent(node_cpu_seconds_total{cpu="random"})
```

### Result

Since this filter returns no data, Prometheus returns:

```text
{...} => 1
```

Important points:

* The return type is an **instant vector**
* It contains:

  * exactly **one element**
  * value = **1**
* The generated label name is not guaranteed

---

# **2. The `absent_over_time()` Function**

`absent_over_time()` works similarly to `absent()`, but it accepts a **range vector** instead of an instant vector.

---

## **Range Vector Example**

This will produce an error:

```promql
absent(node_cpu_seconds_total[1h])
```

Because:

* `absent()` does **not** accept range vectors

Instead, use:

```promql
absent_over_time(node_cpu_seconds_total[1h])
```

---

## **When No Data Exists**

```promql
absent_over_time(node_cpu_seconds_total{cpu="random"}[1h])
```

### Result

Returns:

```text
{...} => 1
```

---

## **Important Note**

Although `absent_over_time()` accepts a **range vector**, it still returns:

* an **instant vector**
* not a range vector

---

# **3. Mathematical Functions**

Prometheus also includes several mathematical helper functions.

---

# **`abs()` – Absolute Value**

Converts all values to their absolute value.

## Example

```promql
abs(metric_name)
```

### Behavior

| Input | Output |
| ----- | ------ |
| `-5`  | `5`    |
| `10`  | `10`   |

---

# **`ceil()` – Round Up**

Rounds values up to the nearest integer.

## Example

```promql
ceil(metric_name)
```

### Behavior

| Input | Output |
| ----- | ------ |
| `1.2` | `2`    |
| `1.6` | `2`    |

---

# **`floor()` – Round Down**

Rounds values down to the nearest integer.

## Example

```promql
floor(metric_name)
```

### Behavior

| Input | Output |
| ----- | ------ |
| `1.6` | `1`    |
| `1.9` | `1`    |

---

# **4. Clamp Functions**

The **clamp functions** are extremely important when working with dashboards and graphs.

They allow you to **limit values within a range**.

These functions are especially useful in [Grafana](https://grafana.com?utm_source=chatgpt.com) visualizations to remove extreme spikes and make graphs cleaner.

---

# **`clamp_min()`**

Sets a minimum allowed value.

Any value smaller than the minimum becomes the minimum value.

---

## Example

```promql
clamp_min(node_cpu_seconds_total, 300)
```

### Result

* Any value below `300` becomes `300`
* No output value will be smaller than `300`

---

# **`clamp_max()`**

Sets a maximum allowed value.

Any value larger than the maximum becomes the maximum value.

---

## Example

```promql
clamp_max(node_cpu_seconds_total, 150000)
```

### Result

* Any value above `150000` becomes `150000`
* No output value will exceed `150000`

---

# **`clamp()`**

Applies both minimum and maximum limits together.

---

## Example

```promql
clamp(node_cpu_seconds_total, 300, 150000)
```

### Result

| Condition     | Final Value |
| ------------- | ----------- |
| `< 300`       | `300`       |
| `> 150000`    | `150000`    |
| Between range | unchanged   |

---

# **Why Clamp Functions Matter**

Clamp functions are very useful when visualizing metrics because they:

* Remove extreme spikes
* Normalize graphs
* Improve dashboard readability
* Help focus on useful data ranges

This is particularly valuable in monitoring dashboards built with:

* [Prometheus](https://prometheus.io?utm_source=chatgpt.com)
* [Grafana](https://grafana.com?utm_source=chatgpt.com)

---

# **Key Takeaways**

## **`absent()`**

* Works with **instant vectors**
* Returns empty result if data exists
* Returns `{...} => 1` if data does not exist

---

## **`absent_over_time()`**

* Works with **range vectors**
* Returns an **instant vector**
* Useful for checking missing metrics over time

---

## **Mathematical Functions**

* `abs()` → absolute value
* `ceil()` → round up
* `floor()` → round down

---

## **Clamp Functions**

* `clamp_min()` → enforce minimum
* `clamp_max()` → enforce maximum
* `clamp()` → enforce both limits

These functions are widely used for:

* dashboard design
* metric cleanup
* visualization improvements
* alert tuning
