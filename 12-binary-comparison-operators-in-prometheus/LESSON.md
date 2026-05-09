# **Prometheus Binary Comparison Operators**

In Prometheus, writing meaningful queries requires understanding the **six binary comparison operators**:

* `==` → Equal
* `!=` → Not equal
* `>` → Greater than
* `<` → Less than
* `>=` → Greater than or equal
* `<=` → Less than or equal

These operators behave differently depending on the data types on the left and right sides of the expression.

---

# **1. Comparing Scalar Values**

A **scalar** is a single numeric value.

Example:

```promql
10 == 10
```

Result:

```text
1
```

In Prometheus:

* `1` represents **true**
* `0` represents **false**

Another example:

```promql
10 == 5
```

Result:

```text
0
```

Because the values are different.

---

# **2. Comparing an Instant Vector with a Scalar**

Assume we have the following instant vector:

| Metric | Labels | Value |
| ------ | ------ | ----- |
| m      | a      | 10    |
| m      | b      | 4     |

Example query:

```promql
m == 10
```

Prometheus filters the vector and returns only the samples whose value matches the scalar.

Result:

| Metric | Labels | Value |
| ------ | ------ | ----- |
| m      | a      | 10    |

The sample with value `4` is removed because it does not satisfy the condition.

---

# **3. Comparing Two Instant Vectors**

When comparing two instant vectors:

* Prometheus matches series based on labels
* Only matching series are compared
* Returned results depend on the comparison outcome

Example:

Left vector:

| Labels | Value |
| ------ | ----- |
| a      | 10    |
| b      | 4     |

Right vector:

| Labels | Value |
| ------ | ----- |
| a      | 10    |
| b      | 8     |

Query:

```promql
left_vector == right_vector
```

Result:

| Labels | Value |
| ------ | ----- |
| a      | 10    |

Why?

* `a`: `10 == 10` → true
* `b`: `4 == 8` → false

Only matching series with true comparisons are returned.

---

# **4. Using Other Comparison Operators**

The same logic applies to the remaining operators.

Example:

```promql
left_vector > right_vector
```

Prometheus returns:

* Series that exist in both vectors
* Where the left-side value is greater than the right-side value

Using the previous example:

| Labels | Left | Right | Result |
| ------ | ---- | ----- | ------ |
| a      | 10   | 10    | false  |
| b      | 4    | 8     | false  |

No results would be returned.

If values were:

| Labels | Left | Right |
| ------ | ---- | ----- |
| a      | 15   | 10    |

Then:

```promql
15 > 10
```

would return the `a` series.

---

# **Key Takeaways**

* Prometheus comparison operators return:

  * `1` for true
  * `0` for false (with scalar comparisons)
* Vector-to-scalar comparisons filter matching samples
* Vector-to-vector comparisons:

  * Match series by labels
  * Return only successful comparisons
* The six comparison operators are:

  * `==`
  * `!=`
  * `>`
  * `<`
  * `>=`
  * `<=`

These operators are essential for building filtering logic, alerts, and advanced PromQL queries.
