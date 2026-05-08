# **Installing Prometheus on Ubuntu/Linux**

This lesson explains how to install **Prometheus** on an **Ubuntu** or any Linux-based server, including downloading the package, creating users and directories, configuring the service, and starting Prometheus successfully. 

---

# **1. Prerequisites**

Before starting, make sure you have:

* A **Linux server** (Ubuntu recommended)
* Internet access
* `sudo` privileges
* Access to the **Prometheus download page**
* Access to the provided **Prometheus service file**

---

# **2. Download the Prometheus Package**

Go to the Prometheus download page:

[Prometheus Downloads](https://prometheus.io/download/?utm_source=chatgpt.com)

Choose:

* **Operating System:** Linux
* **Architecture:**

  * `amd64` → Intel/AMD processors
  * `arm64` → ARM-based servers

> Selecting the correct architecture is important.
> If the binary cannot execute later, it usually means the wrong architecture was downloaded.

Copy the download link for the package.

---

# **3. Install wget (If Needed)**

Check whether `wget` is installed:

```bash
wget
```

If the command is not found:

```bash
sudo apt-get install wget
```

It is also recommended to update the package index:

```bash
sudo apt-get update
```

---

# **4. Download Prometheus**

Use `wget` with the copied download URL:

```bash
sudo wget <PROMETHEUS_DOWNLOAD_LINK>
```

Verify the package exists:

```bash
ls
```

---

# **5. Create Prometheus User and Group**

Prometheus should run under its own system user.

## Create Group

```bash
sudo groupadd --system prometheus
```

## Create User

```bash
sudo useradd --system -g prometheus prometheus
```

---

# **6. Create Required Directories**

## Main Data Directory

```bash
sudo mkdir /var/lib/prometheus
```

## Configuration and Rules Directories

```bash
sudo mkdir -p /etc/prometheus/rules
sudo mkdir -p /etc/prometheus/rules.d
sudo mkdir -p /etc/prometheus/files_sd
```

These directories are used for:

* **Rules**
* **Alerting**
* **Service discovery files**

---

# **7. Extract the Prometheus Package**

Extract the downloaded archive:

```bash
sudo tar xvf prometheus-*.tar.gz
```

Enter the extracted directory:

```bash
cd prometheus-*
```

---

# **8. Understand the Package Contents**

Inside the extracted folder you will find:

| File/Folder         | Purpose                     |
| ------------------- | --------------------------- |
| `prometheus`        | Main Prometheus binary      |
| `promtool`          | Validation and utility tool |
| `prometheus.yml`    | Main configuration file     |
| `console_libraries` | UI support files            |
| `consoles`          | Web console files           |

---

# **9. Move Binary Files**

Move Prometheus binaries into the system executable path:

```bash
sudo mv prometheus promtool /usr/local/bin/
```

Verify installation:

```bash
prometheus --version
```

If successful, the version number is displayed.

---

# **10. Move Configuration Files**

Move the configuration file:

```bash
sudo mv prometheus.yml /etc/prometheus/
```

Move console files:

```bash
sudo mv consoles /etc/prometheus
sudo mv console_libraries /etc/prometheus
```

---

# **11. Create the Prometheus Service File**

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/prometheus.service
```

Example service configuration:

```ini
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple

ExecStart=/usr/local/bin/prometheus \
  --config.file /etc/prometheus/prometheus.yml \
  --storage.tsdb.path /var/lib/prometheus/ \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

Save and exit.

---

# **12. Set Ownership and Permissions**

Grant ownership to the Prometheus user:

```bash
sudo chown -R prometheus:prometheus /etc/prometheus
```

```bash
sudo chown prometheus:prometheus /var/lib/prometheus
```

Set permissions:

```bash
sudo chmod -R 775 /etc/prometheus
```

---

# **13. Start and Enable Prometheus**

Reload systemd:

```bash
sudo systemctl daemon-reload
```

Start Prometheus:

```bash
sudo systemctl start prometheus
```

Enable automatic startup on boot:

```bash
sudo systemctl enable prometheus
```

---

# **14. Verify the Service**

Check service status:

```bash
sudo systemctl status prometheus
```

You should see:

```text
active (running)
```

---

# **15. Access the Prometheus Web UI**

Open the browser:

```text
http://<SERVER_IP>:9090
```

You should now see the **Prometheus dashboard**.

---

# **16. Important Networking Note**

If the server is hosted on:

* AWS
* Azure
* Google Cloud

Make sure **port 9090** is allowed in:

* Security Groups
* Firewall Rules
* Network ACLs

---

# **Summary of Main Commands**

```bash
sudo apt-get update
sudo apt-get install wget

sudo wget <download_link>

sudo groupadd --system prometheus
sudo useradd --system -g prometheus prometheus

sudo mkdir /var/lib/prometheus
sudo mkdir -p /etc/prometheus/rules
sudo mkdir -p /etc/prometheus/rules.d
sudo mkdir -p /etc/prometheus/files_sd

sudo tar xvf prometheus-*.tar.gz

sudo mv prometheus promtool /usr/local/bin/
sudo mv prometheus.yml /etc/prometheus/

sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus
```

---

# **Key Takeaways**

* Prometheus requires:

  * A dedicated user/group
  * Configuration directories
  * A systemd service file
* The web UI runs on **port 9090**
* Correct CPU architecture selection is critical
* `systemctl` manages the Prometheus service lifecycle
