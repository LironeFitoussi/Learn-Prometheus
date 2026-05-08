# Installing Prometheus on Windows


# **Installing Prometheus on Windows**

In this section, you will learn how to install **Prometheus** on a **Windows** operating system.
This setup is mainly intended for **local learning and testing**, not for production environments.

---

# **Important Before You Start**

Installing Prometheus on Windows:

* ✅ Is useful for learning and local practice.
* ❌ Is not recommended for production use.
* ⚠️ Every time the machine restarts, you will need to manually run `prometheus.exe` again.

---

# **Step 1 — Download Prometheus**

Open your browser and go to:

[Prometheus Downloads](https://prometheus.io/download/?utm_source=chatgpt.com)

On the download page:

1. Select **Windows**.
2. Find the **Prometheus** section.
3. Download the `.zip` file.

You will also see other Prometheus-related packages, but for now you only need the main ZIP package.

---

# **Step 2 — Extract the ZIP File**

After downloading:

1. Go to your **Downloads** folder.
2. Extract the ZIP file to a suitable location.

Inside the extracted folder, you will find important files such as:

* `prometheus.exe` → The main Prometheus executable.
* `prometheus.yml` → The Prometheus configuration file.

---

# **Prometheus Configuration File (`prometheus.yml`)**

The file:

```yaml id="x1f9k2"
prometheus.yml
```

is the configuration file used by Prometheus.

For local learning purposes:

* You can use the default configuration.
* No changes are required initially.

---

# **Step 3 — Run Prometheus**

1. Open a **Command Prompt (CMD)** window.
2. Navigate to the folder where you extracted Prometheus.

Example:

```bash id="g8m2n1"
cd C:\Prometheus
```

3. Run the executable:

```bash id="a7q4z9"
prometheus.exe
```

---

# **Step 4 — Verify That Prometheus Is Running**

When you see a message similar to:

```text id="v3n8c5"
Server is ready to receive web requests
```

it means Prometheus is running successfully.

---

# **Step 5 — Access the Web Interface**

Open your browser and navigate to:

```text id="r6w2t4"
http://localhost:9090
```

You should now see the **Prometheus web interface**.

---

# **What Can You Do in the Prometheus UI?**

From the UI, you can:

* Query metrics
* Create dashboards
* Run PromQL queries
* Visualize monitored data

---

# **Important Ports**

## **Port 9090**

Main web interface port for Prometheus.

## **Port 9091**

Commonly used by related components such as Pushgateway.

You may encounter additional ports later in the course depending on the services being used.

---

# **Important Note About Execution**

Prometheus only runs while the CMD window remains open.

If you close the terminal:

* Prometheus stops running.
* You must restart it by running `prometheus.exe` again.

---

# **Summary**

## **Complete Installation Process**

1. Download Prometheus.
2. Extract the ZIP file.
3. Open CMD.
4. Run `prometheus.exe`.
5. Access:

```text id="w0k8m7"
http://localhost:9090
```

---

# **Conclusion**

You now have **Prometheus running on Windows** for local development and learning purposes.

Later, you can continue learning about:

* Sending metrics to Prometheus
* Configuring exporters
* Using Pushgateway
* Visualizing metrics with Grafana
