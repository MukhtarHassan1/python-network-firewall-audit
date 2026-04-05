🛡️ Linux Network Firewall & Security Auditor
A high-performance, multi-threaded Linux systems utility developed in Python for real-time network traffic filtering and security auditing. By interfacing directly with Linux AF_INET sockets, this project implements Multi-Level Security (MLS) and Dynamic Rate-Limiting to harden Ubuntu-based backend services against unauthorized access and Denial of Service (DoS) attacks. It features a professional-grade audit logging system designed for Linux environment forensics and a PyQt5-based control plane for real-time rule manipulation.

📌 Table of Contents
🚀 Core Capabilities
🏗️ System Architecture
🛠️ Tech Stack
📦 Installation & Setup
▶️ Usage Guide
🛡️ Security Features
🧪 Penetration Testing & Auditing

🚀 Core Capabilities
🔹 Dynamic Rate Limiting

Automatically detects suspicious traffic and blocks IPs exceeding request thresholds within a defined time window.

🔹 Multi-Level Security (MLS)

Validates incoming requests using custom headers (X-Sec-Level) and enforces access control based on predefined trust levels.

🔹 Admin Control Dashboard

A PyQt5-based GUI that provides:

Real-time traffic logs
Manual IP blocking/unblocking
System monitoring
🔹 Thread-Safe Logging

Centralized logging system that records:

✅ Allowed requests
❌ Blocked requests
For auditing and forensic analysis.
🏗️ System Architecture

The system acts as a secure proxy layer between clients and backend services.

Client / Attacker
        ↓
   Firewall Server
        ↓
 Protected Backend
Components:
firewall_server.py
Core engine
Handles concurrent connections using threading
Applies rate limiting & MLS rules
firewall_gui.py
Admin dashboard (control panel)
Communicates with server via admin port
firewall_simulator.py
Generates test traffic
Used for stress testing & validation
🛠️ Tech Stack
Category	Technology
Language	Python 3.x
Networking	socket, threading
Data Handling	collections
GUI	PyQt5
Testing Tools	Nmap, Curl
OS	Linux (Kali/Ubuntu Recommended)
📦 Installation & Setup
🔹 Prerequisites
Python 3.8+
Linux Environment (Kali Linux / Ubuntu recommended)
Nmap (for testing)
🔹 1. Clone Repository
git clone https://github.com/YourUsername/linux-firewall-auditor.git
cd linux-firewall-auditor
🔹 2. Install Dependencies
pip install -r requirements.txt
🔹 3. Run the System

Start the Firewall Server:

python src/firewall_server.py

Start the Admin Dashboard:

python src/firewall_gui.py

(Optional) Run Traffic Simulator:

python src/firewall_simulator.py
▶️ Usage Guide
Start the server
Launch the GUI dashboard
Monitor incoming traffic in real-time
Manually block/unblock suspicious IPs
Use simulator or external tools to test attacks
🛡️ Security Features
⚡ O(1) IP Lookup using Python sets
🔐 Admin Authentication for GUI access
🔁 Auto Recovery Mechanism for resetting request counts
📊 Real-Time Monitoring & Logging
🚫 DoS Protection via Rate Limiting
🧩 Header-Based Access Control (MLS)
🧪 Penetration Testing & Auditing

This system was validated using real-world security testing techniques:

Phase	Tool	Objective
Reconnaissance	Nmap	Detect open ports & services
DoS Simulation	Curl	Trigger rate-limiting
Access Control	Headers	Validate MLS enforcement
🔹 Example: Rate Limiting Test
for i in $(seq 1 10); do curl -I http://127.0.0.1:9090; done
