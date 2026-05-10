# **Monitoring Windows with Prometheus Using WMI Exporter**



Unlike Linux, [Prometheus](https://prometheus.io?utm_source=chatgpt.com) does not provide an official Windows exporter out of the box. However, many users:

* run Prometheus on Windows laptops
* manage Windows servers in production
* want to collect Windows system metrics

To solve this, the Prometheus community provides third-party exporters built on top of:

# **WMI (Windows Management Instrumentation)**

---

# **What Is WMI?**

**WMI** stands for:

```text id="2qf8mt"
Windows Management Instrumentation
```

It is a built-in Windows feature used for:

* system management
* administrative automation
* monitoring operating system data
* accessing hardware and software information

Applications and scripts can query WMI to retrieve system metrics and operational data.

---

# **How the Windows Exporter Works**

The exporter:

1. Collects metrics from WMI
2. Converts them into Prometheus metrics format
3. Exposes them through an HTTP endpoint
4. Allows Prometheus to scrape and store those metrics

---

# **Downloading the Windows Exporter**

The easiest way to obtain the exporter is through the Prometheus Community project.

Search for:

```text id="8g7j0w"
WMI Exporter
```

or directly use the community Windows exporter project.

The exporter can be downloaded from the release page.

---

# **Available Download Options**

Inside the releases page, you will see several downloadable assets.

---

## **ZIP File**

If you want to:

* run the exporter directly
* avoid installation
* use a portable version

download:

```text id="m5fx3s"
windows_exporter-<version>-amd64.zip
```

For:

* 64-bit Windows → use `amd64`
* 32-bit Windows → use `386`

---

## **MSI Installer**

If you want a standard Windows installation experience, download:

```text id="l2m7hv"
windows_exporter-<version>.msi
```

This installs the exporter as a Windows application/service.

---

# **Running the Exporter**

After downloading the ZIP file:

1. Extract it
2. Move it to any folder
3. Run the exporter executable

---

# **Default Port**

The Windows exporter uses:

```text id="v1g1gk"
9182
```

Unlike many Prometheus exporters that use:

```text id="p3k0zh"
9100
```

---

# **Important Networking Note**

If your Prometheus server runs on another machine, ensure that:

```text id="m0j8k4"
Port 9182 is accessible
```

through:

* firewalls
* network rules
* security groups

This is a very common issue during setup.

---

# **Verify the Exporter Is Running**

Open your browser and visit:

```text id="3kchwn"
http://localhost:9182
```

You should see the exporter homepage.

---

# **View Metrics**

Open:

```text id="4v8vlt"
http://localhost:9182/metrics
```

You will see a large list of Windows metrics collected from WMI.

Examples include:

* CPU usage
* memory metrics
* disk metrics
* process statistics
* Windows service data

---

# **Configuring Prometheus**

Now we must configure Prometheus to scrape the exporter.

---

# **Locate the Configuration File**

Inside the Prometheus installation folder, locate:

```text id="p2r3mb"
prometheus.yml
```

This is the main Prometheus configuration file.

---

# **Use a Proper Text Editor**

Because YAML formatting depends heavily on:

* indentation
* spaces
* alignment

avoid editing the file using plain Notepad.

Recommended editors:

* [Visual Studio Code](https://code.visualstudio.com?utm_source=chatgpt.com)
* [Notepad++](https://notepad-plus-plus.org?utm_source=chatgpt.com)

Incorrect indentation can prevent Prometheus from starting.

---

# **Edit `scrape_configs`**

Inside `prometheus.yml`, locate:

```yaml id="9y8zjg"
scrape_configs:
```

You will already see a default scrape job called:

```yaml id="w6j9yr"
job_name: "prometheus"
```

This allows Prometheus to monitor itself.

---

# **Duplicate the Existing Job**

Copy the existing job and modify it.

---

## **Example Configuration**

```yaml id="8k9q5h"
scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "wmi_exporter"
    static_configs:
      - targets: ["localhost:9182"]
```

---

# **Save the Configuration**

After editing:

1. Save the file
2. Close the editor

---

# **Restart Prometheus**

Stop and start Prometheus again so it reloads the configuration.

---

# **Verify the Configuration Loaded Successfully**

When Prometheus starts correctly, you should see a message similar to:

```text id="fwx1jl"
Server is ready to receive web requests
```

If Prometheus fails to start:

* the YAML formatting is likely incorrect
* indentation or spacing errors are the most common cause

---

# **Verify Targets in Prometheus**

Open Prometheus:

```text id="k1d61w"
http://localhost:9090
```

---

## **Check Targets**

1. Open the **Status** menu
2. Click **Targets**

You should now see:

| Job          | Status |
| ------------ | ------ |
| Prometheus   | UP     |
| WMI Exporter | UP     |

If the status is:

```text id="5drwx1"
UP
```

then Prometheus is successfully scraping Windows metrics.

---

# **What Metrics Can Be Collected?**

Using the Windows exporter, Prometheus can monitor:

* CPU usage
* RAM utilization
* disk performance
* filesystem usage
* Windows services
* processes
* network traffic
* system uptime

---

# **Why This Setup Is Useful**

This allows you to:

* practice Prometheus locally on Windows
* monitor production Windows servers
* build Grafana dashboards
* create alerts for Windows infrastructure

without needing Linux systems.

---

# **Useful Ports**

| Service          | Port   |
| ---------------- | ------ |
| Prometheus       | `9090` |
| Windows Exporter | `9182` |

---

# **Key Takeaways**

## **Prometheus Has No Official Windows Exporter**

Instead, use:

* community exporters
* WMI-based exporters

---

## **Windows Exporter Uses WMI**

WMI provides:

* Windows system data
* administrative metrics
* monitoring information

---

## **Default Exporter Port**

```text id="m6z6q9"
9182
```

---

## **Prometheus Configuration File**

```text id="j0h7y5"
prometheus.yml
```

---

## **Verify Scraping**

Go to:

```text id="d5vx3m"
Status → Targets
```

and ensure the exporter status is:

```text id="2r6n2m"
UP
```

---

This setup enables complete Windows monitoring using:

* [Prometheus](https://prometheus.io?utm_source=chatgpt.com)
* [Windows Exporter](https://github.com/prometheus-community/windows_exporter?utm_source=chatgpt.com)
* [Grafana](https://grafana.com?utm_source=chatgpt.com)
* Windows WMI infrastructure
