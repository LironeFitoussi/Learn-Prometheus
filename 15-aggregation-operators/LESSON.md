# **Prometheus Aggregation Operators**

Prometheus provides a set of **aggregation operators** that are used to aggregate the elements of a single instant vector.

The result of an aggregation operation is:

* A **new instant vector**
* Usually with **fewer items**
* And aggregated values

Aggregation operators are essential for summarizing, grouping, and analyzing metrics in PromQL.

---

# **Common Aggregation Operators**

## **1. `sum`**

Calculates the total sum of values in an instant vector.

Example:

```promql id="s4k8nm"
sum(node_cpu_seconds_total)
```

This adds together all values from the metric.

---

## **2. `min`**

Finds the smallest value in the instant vector.

Example:

```promql id="x7v2qd"
min(node_cpu_seconds_total)
```

---

## **3. `max`**

Finds the largest value in the instant vector.

Example:

```promql id="m3r6tp"
max(node_cpu_seconds_total)
```

---

## **4. `avg`**

Calculates the average of all values in the vector.

Example:

```promql id="p9z5fw"
avg(node_cpu_seconds_total)
```

---

## **5. `count`**

Counts the number of elements in the vector.

Example:

```promql id="u2n8ky"
count(node_cpu_seconds_total)
```

---

## **6. `group`**

Groups elements together.

Important:

* It does not perform calculations on the values
* The resulting value is always `1`

Example:

```promql id="d6w1xr"
group(node_cpu_seconds_total)
```

Result:

```text id="q5v9ls"
value = 1
```

---

## **7. `count_values`**

Counts how many elements have the same value.

Example:

```promql id="f8t3mb"
count_values("value", node_cpu_seconds_total)
```

---

# **Top and Bottom Operators**

## **8. `topk`**

Returns the largest `K` elements from a vector.

Example:

```promql id="k1p7vz"
topk(2, node_cpu_seconds_total)
```

Returns the two largest values.

---

## **9. `bottomk`**

Returns the smallest `K` elements.

Example:

```promql id="r4m2xn"
bottomk(2, node_cpu_seconds_total)
```

Returns the two smallest values.

---

# **Statistical Aggregation Operators**

## **10. `stddev`**

Calculates the population standard deviation.

Example:

```promql id="t7q4cd"
stddev(node_cpu_seconds_total)
```

---

## **11. `stdvar`**

Calculates the population standard variance.

Example:

```promql id="h3w8pf"
stdvar(node_cpu_seconds_total)
```

---

# **Aggregation Syntax**

Aggregation operators are used like functions.

General syntax:

```promql id="c5n9rk"
operator(metric_name)
```

Example:

```promql id="b1x6qs"
sum(node_cpu_seconds_total)
```

This calculates the sum of all values returned by the metric.

---

# **Using `by` for Grouping**

We can group aggregation results by specific labels using the `by` keyword.

Syntax:

```promql id="z2m4tv"
operator by(label)(metric)
```

Example:

```promql id="n8k3wy"
sum by(mode)(node_cpu_seconds_total)
```

This means:

* Group results by the `mode` label
* Sum values within each group

Result:

| mode   | value |
| ------ | ----- |
| idle   | ...   |
| system | ...   |
| user   | ...   |

---

# **Using `without` to Exclude Labels**

We can also exclude labels during aggregation using `without`.

Syntax:

```promql id="q7t1mp"
operator without(label)(metric)
```

Example:

```promql id="v4d8zk"
sum without(mode)(node_cpu_seconds_total)
```

This means:

* Ignore the `mode` label
* Group by all remaining labels

---

# **Practical Examples**

## **Summing All CPU Metrics**

```promql id="m7r2xf"
sum(node_cpu_seconds_total)
```

Returns a single aggregated value.

---

## **Grouping CPU Metrics by Mode**

```promql id="j5w9nc"
sum by(mode)(node_cpu_seconds_total)
```

Groups results based on CPU mode.

---

## **Finding Top 3 Largest Values**

```promql id="x1q6tv"
topk(3, node_cpu_seconds_total)
```

Returns the three largest values.

---

## **Finding Bottom 3 Smallest Values**

```promql id="l8p2wr"
bottomk(3, node_cpu_seconds_total)
```

Returns the three smallest values.

---

# **Understanding `group`**

Example:

```promql id="f6z3mq"
group(node_cpu_seconds_total)
```

Result:

| value |
| ----- |
| 1     |

Because all elements are grouped into a single group.

---

## **Grouping by Label with `group`**

Example:

```promql id="r2v7nk"
group by(mode)(node_cpu_seconds_total)
```

If there are four different values for `mode`, the result contains four rows.

Important:

* The value is always `1`
* Only grouping changes

---

# **Combining Aggregation Operators**

Aggregation operators can be combined.

Example:

```promql id="w3x8tb"
topk(2, avg by(mode)(node_cpu_seconds_total))
```

This query:

1. Calculates averages grouped by `mode`
2. Returns the two largest averages

---

# **Summary Table**

| Operator       | Description            |
| -------------- | ---------------------- |
| `sum`          | Sum of values          |
| `min`          | Smallest value         |
| `max`          | Largest value          |
| `avg`          | Average value          |
| `count`        | Number of elements     |
| `group`        | Groups elements        |
| `count_values` | Counts matching values |
| `topk`         | Largest K values       |
| `bottomk`      | Smallest K values      |
| `stddev`       | Standard deviation     |
| `stdvar`       | Standard variance      |

---

# **Key Takeaways**

* Aggregation operators work on instant vectors
* They reduce and summarize data
* `by` groups results using specific labels
* `without` excludes labels from grouping
* `topk` and `bottomk` help identify extreme values
* Aggregations can be nested and combined for advanced PromQL queries
