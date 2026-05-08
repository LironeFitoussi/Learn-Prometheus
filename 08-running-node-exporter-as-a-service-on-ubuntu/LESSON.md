# **Running Node Exporter as a Linux Service**

Previously, Node Exporter was started manually by executing its binary file. The problem with this approach is:

> If the terminal session closes, Node Exporter stops running.

To solve this, Node Exporter should run as a:

# **systemd Service**

This ensures:

* Automatic startup on boot
* Background execution
* Better production reliability
* Easier monitoring and management



---

# **1. Why Use a Service?**

Without a service:

```text id="0n8m2n"
Terminal Closed → Node Exporter Stops
```

With a service:

```text id="m0q0pa"
Server Restart → Node Exporter Automatically Starts Again
```

---

# **2. Understanding the Service File**

The service file defines:

* Which user runs Node Exporter
* Which group it belongs to
* Where the binary is located
* How Linux should start the service

Typical service file location:

```text id="z0bxkt"
/etc/systemd/system/node.service
```

---

# **3. Important Service File Sections**

## Unit Section

Contains:

* Description
* Documentation link
* Startup dependencies

Example:

```ini id="h0q7vh"
[Unit]
Description=Node Exporter
Documentation=https://prometheus.io/docs/
After=network.target
```

---

## Service Section

Defines:

* User
* Group
* Startup command

Example:

```ini id="mqf6pw"
[Service]
User=prometheus
Group=prometheus
ExecStart=/var/lib/node/node_exporter
```

---

## Install Section

Defines startup behavior:

```ini id="s2y4jh"
[Install]
WantedBy=multi-user.target
```

---

# **4. Create the Group**

Create a system group:

```bash id="1i3g8s"
sudo groupadd --system prometheus
```

---

# **5. Create the User**

Create a non-login service account:

```bash id="cf1jlwm"
sudo useradd --no-create-home --shell /bin/false -g prometheus prometheus
```

Explanation:

| Option               | Purpose           |
| -------------------- | ----------------- |
| `--no-create-home`   | No home directory |
| `--shell /bin/false` | Prevent login     |
| `-g prometheus`      | Assign group      |

---

# **6. Create Directory for Node Exporter**

Create the directory used in the service file:

```bash id="m9m7go"
sudo mkdir /var/lib/node
```

---

# **7. Move the Binary File**

Move the Node Exporter binary:

```bash id="57ofe3"
sudo mv node_exporter /var/lib/node/
```

Important:

> Keep the trailing slash `/`

Otherwise Linux may rename the file instead of placing it inside the directory.

---

# **8. Create the Service File**

Open the service file using Nano:

```bash id="v2xh6q"
sudo nano /etc/systemd/system/node.service
```

---

# **9. Example Node Exporter Service File**

Paste the following:

```ini id="6c2n4v"
[Unit]
Description=Node Exporter
Documentation=https://prometheus.io/docs/
After=network.target

[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/var/lib/node/node_exporter

[Install]
WantedBy=multi-user.target
```

Save:

```text id="p2dy3g"
CTRL + O
```

Exit:

```text id="vsw1pm"
CTRL + X
```

---

# **10. Set Ownership**

Grant ownership to the Prometheus user:

```bash id="w0qpsa"
sudo chown -R prometheus:prometheus /var/lib/node
```

---

# **11. Set Permissions**

Grant read and execute permissions:

```bash id="v7go7f"
sudo chmod -R 755 /var/lib/node
```

---

# **12. Reload systemd**

Reload daemon configuration:

```bash id="dd5f9n"
sudo systemctl daemon-reload
```

---

# **13. Start the Service**

Start Node Exporter:

```bash id="br6c21"
sudo systemctl start node
```

---

# **14. Enable Auto-Start**

Enable startup on boot:

```bash id="iy2qg0"
sudo systemctl enable node
```

---

# **15. Verify the Service**

Check status:

```bash id="v5c78t"
sudo systemctl status node
```

Expected output:

```text id="6w58fc"
active (running)
```

---

# **16. Why This Matters in Production**

In production systems:

* Exporters must survive reboots
* Monitoring must stay online
* Services must restart automatically

Using `systemd` provides:

* Reliability
* Process management
* Automatic startup
* Logging integration

---

# **17. Typical Production Architecture**

```text id="cjlwm1"
Linux Server
    ↓
Node Exporter Service
    ↓
Prometheus Scrapes Metrics
```

---

# **18. Key Linux Concepts Used**

| Command     | Purpose             |
| ----------- | ------------------- |
| `groupadd`  | Create group        |
| `useradd`   | Create service user |
| `mv`        | Move binary         |
| `nano`      | Edit service file   |
| `chown`     | Change ownership    |
| `chmod`     | Change permissions  |
| `systemctl` | Manage services     |

---

# **19. Summary**

To run Node Exporter reliably:

1. Create a service account
2. Move the binary to a permanent directory
3. Create a systemd service file
4. Set permissions
5. Start and enable the service

---

# **Key Takeaways**

* Running manually is not suitable for production
* `systemd` keeps Node Exporter running in the background
* Services automatically restart after reboot
* Proper ownership and permissions are required
* Node Exporter becomes a persistent monitoring component
