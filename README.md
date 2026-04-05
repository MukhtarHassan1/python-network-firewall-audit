🛡️ Python Based Linux Network Firewall & Security Auditor
A high-performance, multi-threaded Linux systems utility developed in Python for real-time network traffic filtering and security auditing. By interfacing directly with Linux AF_INET sockets, this project implements Multi-Level Security (MLS) and Dynamic Rate-Limiting to harden Ubuntu-based backend services against unauthorized access and Denial of Service (DoS) attacks. It features a professional-grade audit logging system designed for Linux environment forensics and a PyQt5-based control plane for real-time rule manipulation.
📋 Table of Contents:
1. Core Capabilities
2. System Architecture
3. Technical Stack
4. Installation & Setup
5. Usage Guide
6. Penetration Testing & Auditing
7. Security Features
🚀 Core Capabilities:
Dynamic Rate-Limiting: Automatically detects and blacklists IPs exceeding RATE_LIMIT thresholds within a rolling time window.Multi-Level Security (MLS): Intercepts requests and validates X-Sec-Level headers against trusted IP registries.Admin Control Suite: A PyQt5-based dashboard providing real-time visibility into traffic logs and manual override (Block/Unblock) capabilities.Thread-Safe Logging: Implements a centralized, thread-safe auditing system that records every ALLOWED and BLOCKED event for forensic analysis.
🏗️ System ArchitectureThe system operates as a transparent proxy layer between the User/Attacker and the Protected Backend Service.Firewall Server (firewall_server.py): The engine. Uses Python socket and threading to handle concurrent connections.Admin GUI (firewall_gui.py): The control plane. Communicates with the server via a dedicated admin port to update the BLACKLIST in memory.Request Simulator (firewall_simulator.py): The testing suite. Generates randomized traffic to stress-test the rate-limiter and MLS logic.Shutterstock Explore 
🛠️ Technical StackLanguage: Python 3.x (Core Logic: socket, threading, collections)Interface: PyQt5 (Administrative Dashboard)Testing: Nmap (Service Discovery), Curl (Exploitation), Kali Linux (Environment)Log Format: Standardized Security Audit Logs (.txt)
📦 Installation & SetupPrerequisitesUbuntu/Debian or Kali Linux (Recommended)Python 3.8+Nmap (For security auditing)1. Clone & InstallBashgit clone https://github.com/YourUsername/python-network-firewall-audit.git
cd python-network-firewall-audit
pip install -r requirements.txt
2. Launch the EnvironmentThe system requires two components to be running:Start the Server:Bashpython src/firewall_server.py
Start the Admin Dashboard:Bashpython src/firewall_gui.py
🛡️ Penetration Testing & AuditingThis project was validated using a professional penetration testing methodology:PhaseToolObjectiveReconnaissanceNmapValidating port stealth and service version hiding.DoS SimulationCurl LoopTesting the threshold-based rate-limiting trigger.Access ControlCustom HeadersVerifying MLS interception for High security resources.Example Audit Command:Bash# Test rate limiting (Triggering a Block)
for i in $(seq 1 10); do curl -I http://127.0.0.1:9090; done
🔐 Security FeaturesMemory-Efficient Blacklisting: Uses Python sets for $O(1)$ lookup time during high-traffic bursts.Hardened Admin Login: Requires authentication for GUI access to prevent unauthorized rule modification.Auto-Recovery: Includes logic to reset request counts and unblock IPs through the admin interface.
