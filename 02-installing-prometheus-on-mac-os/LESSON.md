# Installing Prometheus on Mac OS

# Installing Prometheus on macOS Using Homebrew

## Introduction

The easiest and most recommended way to install **Prometheus** on a Mac computer is by using a package manager called **Homebrew**.

Homebrew simplifies software installation and service management on macOS.

---

# Verify Homebrew Installation

Before installing Prometheus, check whether Homebrew is already installed on your system.

Open the terminal and run:

```bash id="3fgh5z"
brew --version
```

If Homebrew is installed, you will see output similar to:

```text id="zkv9tq"
Homebrew 4.x.x
```

If you receive an error such as:

```text id="mq3e1p"
brew: command not found
```

then Homebrew is not installed on your Mac.

---

# Install Homebrew

If Homebrew is missing, go to the official website:

[Homebrew Official Website](https://brew.sh/?utm_source=chatgpt.com)

Follow the installation instructions provided on the website.

Once installation is complete, verify it again using:

```bash id="h4w9tu"
brew --version
```

---

# Install Prometheus

After confirming that Homebrew is installed, run:

```bash id="1hr5kj"
brew install prometheus
```

Homebrew will download and install Prometheus on your Mac.

---

# Prometheus Configuration Files

Prometheus configuration files are usually located under:

```text id="4j89zr"
/usr/local/etc
```

Navigate to the directory:

```bash id="k2c8xy"
cd /usr/local/etc
```

List the files:

```bash id="af8npl"
ls
```

You will see several important configuration files.

---

# Important Configuration Files

## Web Configuration File

One important file is:

```text id="c5fw2u"
web.yml
```

This file contains the configuration for the Prometheus web interface.

Inside this file, you may find references to:

* SSL certificates
* HTTPS configuration
* Authentication settings

---

# Self-Signed Certificates

The configuration may reference files such as:

```text id="2m9kqa"
cert.pem
```

and

```text id="7n1wlo"
key.pem
```

These are self-signed SSL certificates used for HTTPS access.

You can open the configuration file using:

```bash id="z7gf2d"
sudo nano web.yml
```

---

# Using HTTP Instead of HTTPS

By default, Prometheus may be configured to allow only HTTPS access.

For local development environments, HTTPS is usually unnecessary.

Additionally, self-signed certificates can cause issues when connecting tools such as **Grafana**, because Grafana expects certificates signed by a trusted Certificate Authority (CA).

To avoid these issues, you can comment out the certificate lines in `web.yml` by adding `#` at the beginning of the lines.

Example:

```yaml id="mn4xsa"
# tls_server_config:
#   cert_file: cert.pem
#   key_file: key.pem
```

This allows Prometheus to run over standard HTTP instead of HTTPS.

---

# Prometheus Main Configuration

Another important file is:

```text id="qf8e6w"
prometheus.yml
```

Open it using:

```bash id="w4v7ha"
nano prometheus.yml
```

This file contains:

* Scraping configuration
* Rule files
* Targets to monitor
* Additional Prometheus settings

---

# Default Login Credentials

The default login credentials for Prometheus are:

| Username | Password |
| -------- | -------- |
| admin    | password |

---

# Starting Prometheus as a Service

To start Prometheus in the background as a macOS service, run:

```bash id="b8c4ry"
brew services start prometheus
```

This launches Prometheus automatically in the background.

---

# Accessing the Prometheus Web Interface

Open your browser and navigate to:

```text id="8q1nfd"
http://localhost:9090
```

You should now see the Prometheus web interface.

> Note: The original lecture mentioned port `1990`, but the default Prometheus port is typically `9090`.

---

# Login Information

If prompted for credentials, use:

```text id="m8j4yr"
Username: admin
Password: password
```

If you previously logged in, your browser session may automatically authenticate you.

---

# Summary

In this section, you learned how to:

* Install Homebrew
* Install Prometheus using Homebrew
* Locate Prometheus configuration files
* Configure HTTP instead of HTTPS
* Start Prometheus as a background service
* Access the Prometheus web interface locally on macOS