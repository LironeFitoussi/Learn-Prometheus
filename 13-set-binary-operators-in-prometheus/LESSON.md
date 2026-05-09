# **Prometheus Set Binary Operators**

Prometheus also provides another category of operators called **set binary operators**.

There are **three set operators**:

* `and`
* `or`
* `unless`

These operators are:

* **Case sensitive**
* Must be written exactly in lowercase
* Applicable **only to instant vectors**

---

# **Example Instant Vectors**

Assume we have two instant vectors.

## **First Instant Vector**

| Metric | Label | Value |
| ------ | ----- | ----- |
| m      | a     | 10    |
| m      | b     | 4     |

## **Second Instant Vector**

| Metric | Label | Value |
| ------ | ----- | ----- |
| m      | a     | 10    |
| m      | c     | 4     |

---

# **1. The `and` Operator**

The `and` operator returns only the elements that exist in **both** instant vectors.

Example:

```promql id="f1c9k2"
vector1 and vector2
```

Result:

| Metric | Label | Value |
| ------ | ----- | ----- |
| m      | a     | 10    |

Why?

Because:

* `m{a}` exists in both vectors
* Metric name, labels, and values match

The other series are excluded because:

* `m{b}` exists only in the first vector
* `m{c}` exists only in the second vector

---

# **2. The `or` Operator**

The `or` operator returns the **union** of both instant vectors.

Example:

```promql id="e6v0pw"
vector1 or vector2
```

Result:

| Metric | Label | Value |
| ------ | ----- | ----- |
| m      | a     | 10    |
| m      | b     | 4     |
| m      | c     | 4     |

This combines all unique series from both vectors.

---

# **3. The `unless` Operator**

The `unless` operator returns elements from the **left-side vector** that do **not** exist in the right-side vector.

Example:

```promql id="2xq3mn"
vector1 unless vector2
```

Result:

| Metric | Label | Value |
| ------ | ----- | ----- |
| m      | b     | 4     |

Why?

* `m{a}` exists in both vectors → removed
* `m{b}` exists only in the left vector → kept

---

# **Important Notes**

## **Set operators work only on instant vectors**

You cannot apply:

* `and`
* `or`
* `unless`

to scalar values.

---

## **Matching is based on series identity**

Prometheus compares:

* Metric name
* Labels
* Sample identity

to determine whether two series match.

---

# **Summary Table**

| Operator | Description                                            |
| -------- | ------------------------------------------------------ |
| `and`    | Returns common series between both vectors             |
| `or`     | Returns all unique series from both vectors            |
| `unless` | Returns left-side series not present on the right side |

---

# **Key Takeaways**

* Set binary operators work only with instant vectors
* Operators are lowercase and case sensitive
* `and` → intersection
* `or` → union
* `unless` → difference between vectors

These operators are very useful when building advanced PromQL filtering and matching queries.
