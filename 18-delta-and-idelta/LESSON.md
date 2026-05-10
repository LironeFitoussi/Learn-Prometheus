# **Prometheus Functions – `day_of_month`, `day_of_week`, `delta`, and `idelta`**

In this lesson, we will learn four important Prometheus functions related to:

* Date and time handling
* Measuring metric changes over time

The functions are:

* **`day_of_month()`**
* **`day_of_week()`**
* **`delta()`**
* **`idelta()`**

These functions are very useful for:

* time-based analysis
* monitoring trends
* dashboards in [Grafana](https://grafana.com?utm_source=chatgpt.com)
* alerting based on metric changes

---

# **1. The `day_of_month()` Function**

The **`day_of_month()`** function accepts an **instant vector** whose values represent timestamps in UTC format.

It returns the day of the month for each timestamp value.

---

## **Syntax**

```promql
day_of_month(vector)
```

---

## **Returned Value**

The function returns a number between:

```text
1 → 31
```

Depending on the day of the month represented by the timestamp.

---

## **Example**

```promql
day_of_month(time())
```

### Possible Result

```text
10
```

If the current UTC date is the 10th day of the month.

---

# **2. The `day_of_week()` Function**

The **`day_of_week()`** function works similarly, but returns the day of the week.

---

## **Syntax**

```promql
day_of_week(vector)
```

---

## **Returned Value**

Prometheus returns a value between:

| Value | Day       |
| ----- | --------- |
| `1`   | Monday    |
| `2`   | Tuesday   |
| `3`   | Wednesday |
| `4`   | Thursday  |
| `5`   | Friday    |
| `6`   | Saturday  |
| `7`   | Sunday    |

---

## **Example**

```promql
day_of_week(time())
```

### Possible Result

```text
7
```

If the current UTC day is Sunday.

---

# **3. The `delta()` Function**

The **`delta()`** function calculates how much a metric has changed over a period of time.

---

## **Important**

`delta()` should only be used with:

* **gauges**

It should not be used with:

* **counters**

Because counters continuously increase and may reset.

---

## **What `delta()` Does**

The function compares:

* the first value in the range
* with the last value in the range

And returns the difference between them.

---

## **Syntax**

```promql
delta(metric[range])
```

---

## **Example**

```promql
delta(node_cpu_temp_celsius[2h])
```

---

## **Interpretation**

This query answers the question:

> “How much did the CPU temperature change during the last 2 hours?”

---

## **Conceptual Example**

| Time  | Value |
| ----- | ----- |
| Start | `50`  |
| End   | `65`  |

Result:

```text
15
```

Because:

```text
65 - 50 = 15
```

---

# **4. The `idelta()` Function**

The **`idelta()`** function works very similarly to `delta()`.

The main difference is how the change is calculated.

---

## **Syntax**

```promql
idelta(metric[range])
```

---

## **Behavior**

While `delta()` uses:

* the first value
* and the last value in the range

`idelta()` uses:

* only the last two data points

This makes `idelta()` more focused on the most recent change.

---

## **Example**

```promql
idelta(node_cpu_temp_celsius[2h])
```

This shows the latest temperature change between the two most recent samples within the last two hours.

---

# **Difference Between `delta()` and `idelta()`**

| Function   | Calculation                |
| ---------- | -------------------------- |
| `delta()`  | First sample → Last sample |
| `idelta()` | Last two samples only      |

---

# **When to Use Them**

## **Use `delta()` When**

* You want the total change over a time range
* You are analyzing trends
* You need overall variation

---

## **Use `idelta()` When**

* You want the latest short-term change
* You need more reactive monitoring
* You are analyzing recent fluctuations

---

# **Important Notes**

## **Works Best with Gauges**

These functions are designed for:

* temperatures
* memory usage
* CPU load
* queue sizes
* active sessions

Not for counters like:

* HTTP requests total
* bytes sent total
* packets received total

---

# **Key Takeaways**

## **`day_of_month()`**

* Returns day of the month
* Values range from `1` to `31`

---

## **`day_of_week()`**

* Returns day of the week
* Values range from `1` (Monday) to `7` (Sunday)

---

## **`delta()`**

* Calculates total change across a range
* Uses first and last samples

---

## **`idelta()`**

* Calculates the most recent change
* Uses only the last two samples

---

These functions are commonly used in:

* monitoring dashboards
* time analysis
* anomaly detection
* operational visibility
* Prometheus alerting rules
