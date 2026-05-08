# **Part 2 — AWS Infrastructure Setup + Installing Prometheus + Installing Node Exporter**

In this part, we will:

* Create the AWS infrastructure
* Configure networking and security groups
* Install Prometheus
* Install Node Exporter

At the end of this part:

✅ Prometheus will run on port `9090`
✅ Node Exporter will run on port `9100`
❌ Prometheus will NOT scrape Node Exporter yet (this comes in Part 3)

---

# **Architecture**

We will create:

```text id="8bvr2m"
EC2 #1 → Prometheus Server
EC2 #2 → Application Server
```

Node Exporter will run on the Application Server.

---

# **PART 2.1 — Create AWS Infrastructure**

# **1. Open AWS EC2 Console**

Go to:

[AWS Console](https://aws.amazon.com/console/?utm_source=chatgpt.com)

Navigate to:

```text id="xmv4ff"
EC2 Dashboard
```

---

# **2. Launch Prometheus Server**

Click:

```text id="z1jlsf"
Launch Instance
```

---

# **3. Configure Prometheus EC2**

## Name

```text id="xudjkn"
prometheus-server
```

---

## AMI (Operating System)

Choose:

```text id="l74kgz"
Ubuntu Server 24.04 LTS
```

(or Ubuntu 22.04)

---

## Instance Type

Choose:

```text id="djlwm5"
t2.micro
```

---

# **4. Create SSH Key Pair**

Under:

```text id="ljqm86"
Key Pair → Create New Key Pair
```

Example:

```text id="jlwm9s"
prometheus-key
```

Download:

```text id="3j7v8g"
prometheus-key.pem
```

Store this file safely.

---

# **5. Create Prometheus Security Group**

Create new security group:

```text id="mfkxzd"
prometheus-sg
```

---

## Add Inbound Rules

| Type       | Port | Source |
| ---------- | ---- | ------ |
| SSH        | 22   | My IP  |
| Custom TCP | 9090 | My IP  |

---

## Why These Ports?

| Port | Purpose           |
| ---- | ----------------- |
| 22   | SSH access        |
| 9090 | Prometheus web UI |

---

# **6. Launch the Prometheus Server**

Click:

```text id="rlxjlwm"
Launch Instance
```

---

# **7. Launch Application Server**

Create another EC2 instance.

---

## Name

```text id="t9jlwm"
application-server
```

---

## AMI

Ubuntu Server again.

---

## Instance Type

```text id="yjlwm4"
t2.micro
```

---

# **8. Create Application Security Group**

Create:

```text id="1jlwm7"
application-sg
```

---

## Add Inbound Rules

| Type       | Port | Source        |
| ---------- | ---- | ------------- |
| SSH        | 22   | My IP         |
| Custom TCP | 9100 | prometheus-sg |

---

# **Important Security Note**

Do NOT expose port `9100` publicly.

BAD:

```text id="jlwm7t"
0.0.0.0/0
```

GOOD:

```text id="0jlwm2"
prometheus-sg
```

This ensures only the Prometheus server can access Node Exporter.

---

# **9. Understand Public vs Private IPs**

Each EC2 instance gets:

| Type       | Example   |
| ---------- | --------- |
| Public IP  | 54.x.x.x  |
| Private IP | 172.x.x.x |

Use:

| Use Case                   | IP Type |
| -------------------------- | ------- |
| SSH from laptop            | Public  |
| Internal AWS communication | Private |

---

# **PART 2.2 — Connect to the Servers**

# **10. Connect to Prometheus Server**

Open terminal.

Move to the folder containing your `.pem` file.

---

## Set Permissions

```bash id="jlwm8z"
chmod 400 prometheus-key.pem
```

---

## SSH into Prometheus Server

```bash id="3jlwm8"
ssh -i prometheus-key.pem ubuntu@PROMETHEUS_PUBLIC_IP
```

---

# **11. Update Ubuntu**

```bash id="jlwm7y"
sudo apt update
```

```bash id="mjlwm8"
sudo apt upgrade -y
```

---

# **PART 2.3 — Install Prometheus**

# **12. Download Prometheus**

Go to:

[Prometheus Downloads](https://prometheus.io/download/?utm_source=chatgpt.com)

Copy the Linux AMD64 download URL.

Example:

```bash id="jlwm9x"
wget https://github.com/prometheus/prometheus/releases/download/v3.5.3/prometheus-3.5.3.linux-amd64.tar.gz
```

---

# **13. Extract the Archive**

```bash id="jlwm4a"
tar -xvf prometheus-*.tar.gz
```

---

# **14. Enter the Directory**

```bash id="zjlwm9"
cd prometheus-*
```

---

# **15. Create Prometheus User**

```bash id="mjlwm0"
sudo useradd --no-create-home --shell /bin/false prometheus
```

---

# **16. Create Required Directories**

```bash id="jlwm5u"
sudo mkdir /etc/prometheus
```

```bash id="0jlwm3"
sudo mkdir /var/lib/prometheus
```

---

# **17. Move Files**

```bash id="vjlwm1"
sudo mv prometheus promtool /usr/local/bin/
```

```bash id="sjlwm6"
sudo mv consoles console_libraries prometheus.yml /etc/prometheus/
```

---

# **18. Set Ownership**

```bash id="xjlwm5"
sudo chown -R prometheus:prometheus /etc/prometheus
```

```bash id="qjlwm4"
sudo chown -R prometheus:prometheus /var/lib/prometheus
```

---

# **19. Create Prometheus Service**

```bash id="cjlwm1"
sudo nano /etc/systemd/system/prometheus.service
```

Paste:

```ini id="7jlwm2"
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

[Service]
User=prometheus
Group=prometheus
Type=simple

ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus/ \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries

[Install]
WantedBy=multi-user.target
```

---

# **20. Start Prometheus**

```bash id="5jlwm8"
sudo systemctl daemon-reload
```

```bash id="1jlwm9"
sudo systemctl enable prometheus
```

```bash id="kjlwm2"
sudo systemctl start prometheus
```

---

# **21. Verify Prometheus Service**

```bash id="hjlwm7"
sudo systemctl status prometheus
```

Expected:

```text id="7jlwm5"
active (running)
```

---

# **22. Access Prometheus UI**

Open browser:

```text id="tjlwm4"
http://PROMETHEUS_PUBLIC_IP:9090
```

You should now see the Prometheus dashboard.

At this point:

✅ Prometheus is installed
✅ Prometheus web UI works
❌ No scraping configured yet

---

# **PART 2.4 — Install Node Exporter**

# **23. SSH into Application Server**

```bash id="njlwm6"
ssh -i prometheus-key.pem ubuntu@APPLICATION_PUBLIC_IP
```

---

# **24. Update Ubuntu**

```bash id="rjlwm1"
sudo apt update && sudo apt upgrade -y
```

---

# **25. Download Node Exporter**

Go to:

[Prometheus Downloads](https://prometheus.io/download/?utm_source=chatgpt.com)

Find:

```text id="fjlwm9"
Node Exporter
```

Copy Linux AMD64 URL.

Example:

```bash id="wjlwm8"
wget https://github.com/prometheus/node_exporter/releases/download/v1.11.1/node_exporter-1.11.1.linux-amd64.tar.gz
```

---

# **26. Extract the Archive**

```bash id="7jlwm8"
tar -xvf node_exporter-*.tar.gz
```

---

# **27. Create Node Exporter User**

```bash id="jjlwm3"
sudo useradd --no-create-home --shell /bin/false node_exporter
```

---

# **28. Move Binary**

```bash id="gjlwm0"
sudo mv node_exporter-*/node_exporter /usr/local/bin/
```

---

# **29. Set Ownership**

```bash id="9jlwm1"
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter
```

---

# **30. Create Node Exporter Service**

```bash id="pjlwm2"
sudo nano /etc/systemd/system/node_exporter.service
```

Paste:

```ini id="4jlwm0"
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
```

---

# **31. Start Node Exporter**

```bash id="8jlwm7"
sudo systemctl daemon-reload
```

```bash id="2jlwm6"
sudo systemctl enable node_exporter
```

```bash id="6jlwm5"
sudo systemctl start node_exporter
```

---

# **32. Verify Node Exporter**

```bash id="ljlwm8"
sudo systemctl status node_exporter
```

Expected:

```text id="3jlwm9"
active (running)
```

---

# **33. Verify Metrics Endpoint**

On the application server:

```bash id="0jlwm1"
curl localhost:9100/metrics
```

You should see many metrics exposed.

---

# **34. Optional Browser Test**

Temporarily test:

```text id="vjlwm7"
http://APPLICATION_PUBLIC_IP:9100/metrics
```

ONLY if your firewall allows your IP temporarily.

After testing:

✅ Remove public access again
✅ Keep access restricted to Prometheus server only

---

# **Final State After Part 2**

You now have:

| Component                         | Status  |
| --------------------------------- | ------- |
| AWS infrastructure                | Ready   |
| EC2 networking                    | Ready   |
| Prometheus installed              | Yes     |
| Prometheus UI                     | Working |
| Node Exporter installed           | Yes     |
| Node Exporter metrics endpoint    | Working |
| Prometheus scraping Node Exporter | Not yet |

---

# **What Comes Next (Part 3)**

In Part 3 we will:

* Edit `prometheus.yml`
* Add `scrape_configs`
* Configure target IPs
* Restart Prometheus
* Verify `/targets`
* Confirm metrics scraping works
