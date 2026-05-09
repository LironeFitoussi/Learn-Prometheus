# **Writing Queries in Prometheus (PromQL)**

Finally, it is time to start writing queries in **Prometheus** using **PromQL**.

Previously, we learned that to view a metric in Prometheus, we can simply use the metric name. We also learned that we can apply filters using what is called:

* **Filter Matchers**
* **Label Selectors**

---

# **Basic Query Structure**

A Prometheus query usually contains:

* The **metric name**
* An optional set of **filters**

General structure:

```promql id="d9f4nx"
metric_name{label1="value1", label2="value2"}
```

The filters are composed of:

* **Labels**
* Each label is a `key="value"` pair

Example:

```promql id="x3v8qp"
prometheus_http_requests_total{code="200", job="prometheus"}
```

---

# **How Filters Work**

Inside the curly braces `{}`:

* Each filter is separated by a comma
* A comma represents a logical **AND**

So:

```promql id="u7m2ke"
{code="200", job="prometheus"}
```

means:

```text id="r6c1tb"
code = "200" AND job = "prometheus"
```

---

# **Complete Example**

Query:

```promql id="w1z5fd"
prometheus_http_requests_total{code="200", job="prometheus"}
```

Prometheus will return only the time series where:

* The metric name is:

```text id="n4x8sa"
prometheus_http_requests_total
```

And:

* `code = "200"`
* `job = "prometheus"`

---

# **Filter Operators (Matchers)**

Prometheus supports four main filter operators.

| Operator | Meaning                           |
| -------- | --------------------------------- |
| `=`      | Equal                             |
| `!=`     | Not equal                         |
| `=~`     | Matches regular expression        |
| `!~`     | Does not match regular expression |

---

# **1. Equal Operator (`=`)**

Checks if values are exactly equal.

Example:

```promql id="k8r3vm"
code="200"
```

Returns only metrics where:

```text id="m5q2yn"
code = 200
```

---

# **2. Not Equal Operator (`!=`)**

Returns metrics whose value is different.

Example:

```promql id="s2w7lc"
code!="200"
```

---

# **3. Regular Expression Match (`=~`)**

Allows matching strings using **regex**.

Example:

```promql id="f9d6pt"
code=~"2.*"
```

This means:

* The value must start with `2`
* Anything after that is allowed

So it matches:

* `200`
* `201`
* `204`

---

# **Important Regex Note**

When writing regular expressions in Prometheus:

✅ Use:

```text id="h4n1zk"
2.*
```

❌ Avoid:

```text id="p7v5mx"
2
```

Because:

* Regex expressions that can match empty strings may produce unexpected results
* `.*` means:

  * any character
  * any number of times

---

# **4. Negative Regex Match (`!~`)**

This is the opposite of `=~`.

Example:

```promql id="y6b3qw"
code!~"5.*"
```

Returns everything that does **not** start with `5`.

---

# **Testing Queries in Prometheus**

For testing, you can use any metric that returns multiple rows.

Example metric:

```promql id="c3r9vf"
prometheus_http_response_size_bytes_bucket
```

This metric comes from Prometheus’s internal exporter.

---

# **Filtering by Labels**

Example:

```promql id="e1k8mt"
prometheus_http_response_size_bytes_bucket{handler="/static/*filepath"}
```

This returns only metrics where:

```text id="q9u4ld"
handler = "/static/*filepath"
```

---

# **Using Regex in Labels**

If we want to ignore part of the text:

```promql id="b5x7ns"
prometheus_http_response_size_bytes_bucket{handler=~"/static/.*"}
```

Here:

```text id="v2p6rh"
.*
```

means:

* any character
* any number of times

So:

```text id="m8d1cy"
/static/anything
```

will match.

---

# **Combining Filters**

We can add more filters using commas.

Example:

```promql id="t4w9qp"
prometheus_http_response_size_bytes_bucket{handler=~"/static/.*", le="1000"}
```

This means:

* `handler` matches the regex
* AND `le = "1000"`

---

# **Important: Data Types**

In Prometheus, types must match exactly.

✅ Correct:

```promql id="z7n2fx"
le="1000"
```

❌ Incorrect:

```promql id="j3m6vk"
le=1000
```

Why?

Because:

* Labels are always strings
* `"1000"` is a string
* `1000` is a number

Prometheus does not automatically convert types.

---

# **Summary**

## **Query Structure**

```promql id="r5k8tb"
metric_name{label="value"}
```

---

## **Filter Operators**

| Operator | Usage                |
| -------- | -------------------- |
| `=`      | Equal                |
| `!=`     | Not equal            |
| `=~`     | Regex match          |
| `!~`     | Negative regex match |

---

## **Best Practices**

* Use regex properly with `.*`
* Labels must use quoted strings
* Commas represent logical AND
* Always test queries in the Prometheus UI

---

# **Final Example**

```promql id="g1v4md"
prometheus_http_response_size_bytes_bucket{
  handler=~"/static/.*",
  le="1000"
}
```

This query returns all time series:

* From the metric `prometheus_http_response_size_bytes_bucket`
* Where:

  * `handler` starts with `/static/`
  * and `le` equals `"1000"`
