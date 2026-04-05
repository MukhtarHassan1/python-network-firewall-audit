# 🛡️ Linux Network Firewall & Security Auditor

A high-performance, multi-threaded Python-based firewall system designed for real-time network traffic filtering, security auditing, and threat mitigation.

This project implements Multi-Level Security (MLS) and Dynamic Rate Limiting to protect backend services from unauthorized access and Denial-of-Service (DoS) attacks.

---

## 📌 Table of Contents

* Core Capabilities
* System Architecture
* Tech Stack
* Installation & Setup
* Usage Guide
* Security Features
* Penetration Testing & Auditing
* Project Structure
* License
* Author

---

## 🚀 Core Capabilities

### Dynamic Rate Limiting

Automatically detects and blocks IPs exceeding request thresholds within a defined time window.

### Multi-Level Security (MLS)

Validates incoming requests using custom headers (X-Sec-Level) and enforces access control based on trust levels.

### Admin Control Dashboard

PyQt5-based GUI providing:

* Real-time traffic logs
* Manual IP blocking/unblocking
* System monitoring

### Thread-Safe Logging

Logs all allowed and blocked requests for auditing and analysis.

---

## 🏗️ System Architecture

The system acts as a secure proxy layer between clients and backend services.

Client → Firewall Server → Backend Server

### Components

* firewall_server.py
  Core engine handling connections, rate limiting, and MLS logic

* firewall_gui.py
  Admin dashboard for monitoring and control

* firewall_simulator.py
  Traffic generator for testing

---

## 🛠️ Tech Stack

* Python 3.x
* socket, threading, collections
* PyQt5
* Nmap, Curl
* Linux (Ubuntu/Kali recommended)

---

## 📦 Installation & Setup

### Prerequisites

* Python 3.8+
* Linux environment
* Nmap

### Clone Repository

git clone https://github.com/YourUsername/linux-firewall-auditor.git
cd linux-firewall-auditor

### Install Dependencies

pip install -r requirements.txt

### Run the System

Start Server:
python src/firewall_server.py

Start GUI:
python src/firewall_gui.py

(Optional) Run Simulator:
python src/firewall_simulator.py

---

## ▶️ Usage Guide

1. Start the server
2. Launch the GUI
3. Monitor traffic
4. Block/unblock IPs
5. Test using simulator or tools

---

## 🛡️ Security Features

* O(1) IP lookup using sets
* Admin authentication
* Auto recovery logic
* Real-time logging
* DoS protection
* Header-based access control

---

## 🧪 Penetration Testing & Auditing

| Phase          | Tool    | Objective             |
| -------------- | ------- | --------------------- |
| Reconnaissance | Nmap    | Detect open ports     |
| DoS Simulation | Curl    | Trigger rate limiting |
| Access Control | Headers | Test MLS              |

### Example Test

for i in $(seq 1 10); do curl -I http://127.0.0.1:9090; done

---

## 📂 Project Structure

project-root/
│
├── src/
│   ├── firewall_server.py
│   ├── firewall_gui.py
│   └── firewall_simulator.py
│
├── logs/
│   └── audit_logs.txt
│
├── requirements.txt
├── README.md
└── LICENSE

---

## 📄 License

This project is licensed under the MIT License.

---

## ✍️ Author

Syed Mukhtar Ul Hassan
Software Engineering Student

GitHub: https://github.com/YourUsername
LinkedIn: https://linkedin.com/in/YourProfile

---
