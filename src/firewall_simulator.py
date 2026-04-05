import sys
import time
import threading
import random
from collections import defaultdict
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton,
                             QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit,
                             QHBoxLayout, QProgressBar, QDialog, QFormLayout)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont

# Configuration settings
RATE_LIMIT = 5  # Max requests per IP per minute
BLACKLIST = set()
LOG_FILE = "firewall_logs.txt"
SECURITY_LEVELS = {"low": 1, "medium": 2, "high": 3}  # Example levels
TRUSTED_IPS = {"192.168.1.1", "10.0.0.10"}  # Predefined trusted IPs
ADMIN_CREDENTIALS = {"admin": "123"}  # Hardcoded admin credentials

# Request tracking
request_count = defaultdict(int)
blocked_ips = set()
traffic_stats = []  # To store traffic data for simulation purposes

# Logging function
def log_event(event, ip, reason="N/A"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    log_message = f"[{timestamp}] {event}: IP={ip}, Reason={reason}\n"
    with open(LOG_FILE, "a") as log:
        log.write(log_message)
    print(log_message.strip())

# Rate limiting enforcement
def rate_limiter(ip):
    request_count[ip] += 1
    if request_count[ip] > RATE_LIMIT:
        BLACKLIST.add(ip)
        blocked_ips.add(ip)
        log_event("BLOCKED", ip, "Rate limit exceeded")
        return False
    return True

# IP blacklist management
def add_to_blacklist(ip):
    BLACKLIST.add(ip)
    log_event("MANUAL BLOCK", ip, "Manually added to blacklist")

def remove_from_blacklist(ip):
    if ip in BLACKLIST:
        BLACKLIST.remove(ip)
        log_event("UNBLOCKED", ip, "Manually removed from blacklist")

# Multi-Level Security enforcement
def enforce_mls(ip, requested_level):
    if ip in BLACKLIST:
        log_event("BLOCKED", ip, "Blacklisted IP")
        return False
    if requested_level > SECURITY_LEVELS.get("medium", 1) and ip not in TRUSTED_IPS:
        log_event("BLOCKED", ip, "Insufficient security level")
        return False
    log_event("ALLOWED", ip, "Access granted")
    return True

# Generate random IPs for simulation
def generate_random_ip():
    return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Login")
        self.setGeometry(400, 200, 300, 150)

        layout = QFormLayout()

        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter Admin ID")
        layout.addRow("Admin ID:", self.id_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.verify_credentials)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def verify_credentials(self):
        admin_id = self.id_input.text()
        password = self.password_input.text()
        if ADMIN_CREDENTIALS.get(admin_id) == password:
            self.accept()
        else:
            self.id_input.clear()
            self.password_input.clear()
            self.id_input.setPlaceholderText("Invalid credentials, try again")

from PyQt5.QtCore import QThread, pyqtSignal

class RequestSimulator(QThread):
    update_progress = pyqtSignal(int)
    update_traffic = pyqtSignal(list)
    simulation_complete = pyqtSignal()  # Signal to indicate simulation is complete

    def __init__(self):
        super().__init__()
        self.total_requests = 0  # Counter for total IPs processed
        self.max_requests = 60  # Maximum number of IPs to process
        self.running = True  # Control flag for the simulation loop

    def run(self):
        sample_ips = [generate_random_ip() for _ in range(10)] + list(TRUSTED_IPS)
        while self.running and self.total_requests < self.max_requests:
            traffic_updates = []
            for ip in sample_ips:
                if self.total_requests >= self.max_requests:
                    self.running = False
                    break
                allowed = rate_limiter(ip)
                level = random.choice(list(SECURITY_LEVELS.values()))
                if allowed:
                    result = enforce_mls(ip, level)
                    traffic_updates.append((time.strftime("%H:%M:%S"), ip, "ALLOWED" if result else "BLOCKED"))
                self.update_progress.emit(int((self.total_requests / self.max_requests) * 100))  # Update progress
                self.total_requests += 1
            self.update_traffic.emit(traffic_updates)  # Emit traffic updates
            time.sleep(1)  # Reduce sleep time for smoother updates
        self.update_progress.emit(100)  # Ensure progress bar is set to 100%
        self.simulation_complete.emit()  # Emit signal indicating completion

class FirewallSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MLS Firewall Simulator")
        self.setGeometry(100, 100, 1000, 700)

        # Main layout
        main_layout = QVBoxLayout()

        # Header label
        header = QLabel("MLS Firewall Simulator")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(header)

        # Traffic table
        self.traffic_table = QTableWidget()
        self.traffic_table.setColumnCount(3)
        self.traffic_table.setHorizontalHeaderLabels(["Time", "IP", "Status"])
        self.traffic_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.traffic_table)

        # IP management layout
        ip_layout = QHBoxLayout()

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP to blacklist")
        ip_layout.addWidget(self.ip_input)

        self.block_button = QPushButton("Block IP")
        self.block_button.clicked.connect(self.handle_block_ip)
        ip_layout.addWidget(self.block_button)

        self.unblock_button = QPushButton("Unblock IP")
        self.unblock_button.clicked.connect(self.handle_unblock_ip)
        ip_layout.addWidget(self.unblock_button)

        main_layout.addLayout(ip_layout)

        # Progress bar for request simulation
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # Start simulation button
        self.start_button = QPushButton("Start Simulation")
        self.start_button.clicked.connect(self.start_simulation)
        main_layout.addWidget(self.start_button)

        # Set main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Traffic stats
        self.traffic_stats = []

    def handle_block_ip(self):
        ip = self.ip_input.text()
        if ip:
            add_to_blacklist(ip)
            self.ip_input.clear()

    def handle_unblock_ip(self):
        ip = self.ip_input.text()
        if ip:
            remove_from_blacklist(ip)
            self.ip_input.clear()

    def start_simulation(self):
        self.simulator_thread = RequestSimulator()
        self.simulator_thread.update_progress.connect(self.update_progress_bar)
        self.simulator_thread.update_traffic.connect(self.handle_traffic_update)
        self.simulator_thread.simulation_complete.connect(self.on_simulation_complete)
        self.simulator_thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def handle_traffic_update(self, updates):
        self.traffic_stats.extend(updates)
        self.update_traffic_table()

    def update_traffic_table(self):
        self.traffic_table.setRowCount(len(self.traffic_stats))
        for row, (timestamp, ip, status) in enumerate(self.traffic_stats):
            self.traffic_table.setItem(row, 0, QTableWidgetItem(timestamp))
            self.traffic_table.setItem(row, 1, QTableWidgetItem(ip))
            self.traffic_table.setItem(row, 2, QTableWidgetItem(status))


    def on_simulation_complete(self):
        self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = LoginDialog()
    if login.exec_() == QDialog.Accepted:
        window = FirewallSimulator()
        window.show()
        sys.exit(app.exec_())
