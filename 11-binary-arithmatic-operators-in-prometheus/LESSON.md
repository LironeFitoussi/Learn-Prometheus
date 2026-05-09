# **Arithmetic Operators in PromQL**

Prometheus provides several arithmetic operators that can be used inside **PromQL** queries to manipulate metric values. These operators work with:

* Scalars
* Instant vectors
* Vector-to-vector operations

Understanding how operators behave with different data types is very important when writing PromQL queries. 

---

# **1. PromQL Arithmetic Operators**

Prometheus supports the following arithmetic operators:

| Operator | Purpose            |
| -------- | ------------------ |
| `+`      | Addition           |
| `-`      | Subtraction        |
| `*`      | Multiplication     |
| `/`      | Division           |
| `%`      | Modulo (Remainder) |
| `^`      | Power              |

---

# **2. Scalar Operations**

When arithmetic operators are applied to two scalar values:

```text id="94i5vn"
2 + 2
```

Result:

```text id="4hn16u"
4
```

The result is another scalar value.

---

# **3. Scalars in Prometheus**

In Prometheus:

* Integers are treated as floats
* Numeric operations return scalar values

Examples:

```text id="jjlwmu"
10 - 3 = 7
5 * 2 = 10
20 / 4 = 5
2 ^ 3 = 8
```

---

# **4. Scalar + Instant Vector**

When an arithmetic operator is used between:

```text id="jlwm6m"
Scalar + Instant Vector
```

The scalar is applied to:

# **Every Item in the Vector**

---

# **5. Example Instant Vector**

Suppose an instant vector contains:

```text id="1yyqg8"
5
6
```

If we add `5`:

```text id="o2d6o7"
vector + 5
```

Result:

```text id="z34sln"
10
11
```

---

# **6. Prometheus UI Example**

Example metric query:

```text id="ysn3lm"
some_metric
```

Suppose the returned value is:

```text id="ul8xcu"
1
```

Now applying:

```text id="xxotrl"
some_metric + 6
```

Result:

```text id="ahsz06"
7
```

The scalar value is added to the vector item.

---

# **7. Example with Multiple Vector Items**

Suppose the vector contains:

```text id="mmdx5i"
550
333
```

Query:

```text id="kqrmja"
metric_name + 5
```

Result:

```text id="4e4vk0"
555
338
```

---

# **8. Subtraction Example**

Original values:

```text id="ap3u10"
550
333
```

Query:

```text id="ozxxhm"
metric_name - 10
```

Result:

```text id="m7rwsk"
540
323
```

---

# **9. Important Concept**

When applying arithmetic operations:

> The original vector is NOT modified.

Prometheus always returns:

# **A New Resulting Vector**

---

# **10. Vector-to-Vector Operations**

Prometheus can also apply operators between:

```text id="vzjlwm"
Instant Vector A + Instant Vector B
```

---

# **11. How Vector Matching Works**

Prometheus matches vector items based on:

* Metric name
* Labels

Only matching time series participate in the operation.

---

# **12. Example Vector A**

Suppose vector A contains:

```text id="t8gcy1"
m1{label="a"} = 5
m1{label="b"} = 8
m1{label="c"} = 10
m1{label="d"} = 12
```

---

# **13. Example Vector B**

```text id="6ozvny"
m1{label="a"} = 37
m1{label="b"} = 6
```

---

# **14. Vector Addition Example**

Query:

```text id="7qcxjs"
A + B
```

Matching occurs only for:

```text id="7bjlwm"
label="a"
label="b"
```

---

# **15. Resulting Vector**

```text id="mjlwmu"
m1{label="a"} = 42
m1{label="b"} = 14
```

Explanation:

| Matching Series | Calculation   |
| --------------- | ------------- |
| `a`             | `5 + 37 = 42` |
| `b`             | `8 + 6 = 14`  |

---

# **16. Non-Matching Metrics Disappear**

Metrics existing only in Vector A:

```text id="ukr4k6"
c
d
```

do NOT appear in the result because no matching series exists in Vector B.

---

# **17. Why Matching Matters**

Prometheus vector operations are label-aware.

Two series match only when:

* Metric names match
* Labels match

Otherwise:

```text id="tjlwmq"
No Output
```

---

# **18. Common Use Cases**

Arithmetic operators are often used for:

| Use Case          | Example                 |
| ----------------- | ----------------------- |
| CPU calculations  | Usage percentages       |
| Error rates       | Failed / total requests |
| Ratios            | Memory usage            |
| Scaling values    | Unit conversion         |
| Combining metrics | Aggregation logic       |

---

# **19. Example Real Query**

CPU usage percentage:

```text id="yjlwmx"
(node_cpu_seconds_total / 100) * 100
```

---

# **20. Important PromQL Behavior**

| Operation       | Behavior                           |
| --------------- | ---------------------------------- |
| Scalar + Scalar | Returns scalar                     |
| Scalar + Vector | Scalar applied to all vector items |
| Vector + Vector | Matching series combined           |

---

# **21. Key Concepts**

## Scalar

Single numeric value.

---

## Instant Vector

One sample per time series.

---

## Vector Matching

Prometheus aligns metrics using labels and metric names.

---

# **22. Summary**

Prometheus arithmetic operators can work with:

* Scalars
* Instant vectors
* Vector combinations

Operations on vectors always produce:

# **New Resulting Vectors**

without modifying the original metrics.

---

# **Key Takeaways**

* PromQL supports standard arithmetic operators
* Scalars affect every member of a vector
* Vector operations require matching labels
* Non-matching series disappear from results
* Prometheus creates new vectors for every operation
* Understanding vector matching is critical for advanced PromQL queries

