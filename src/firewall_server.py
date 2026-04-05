import socket
import threading
import time
from collections import defaultdict

# ---------------- CONFIG ----------------
RATE_LIMIT = 5
BLACKLIST = set()
TRUSTED_IPS = {"127.0.0.1"}  # add specific IPs if you want to allow "high" level
SECURITY_LEVELS = {"low": 1, "medium": 2, "high": 3}
LOG_FILE = "firewall_logs.txt"

# Backend service protected by firewall (runs on SAME Windows machine)
BACKEND_HOST = "127.0.0.1"
BACKEND_PORT = 8080

# Firewall listening port (attackers connect here)
FIREWALL_HOST = "0.0.0.0"
FIREWALL_PORT = 9090

request_count = defaultdict(int)
lock = threading.Lock()

# ---------------- LOGGING ----------------
def log_event(event, ip, reason="N/A"):
    # Keep same format so your GUI parser continues to work
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    msg = f"[{timestamp}] {event}: IP={ip}, Reason={reason}\n"
    print(msg.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg)

# ---------------- FIREWALL LOGIC ----------------
def rate_limiter(ip):
    request_count[ip] += 1
    if request_count[ip] > RATE_LIMIT:
        BLACKLIST.add(ip)
        log_event("BLOCKED", ip, "Rate limit exceeded")
        return False
    return True

def enforce_mls(ip, level):
    if ip in BLACKLIST:
        log_event("BLOCKED", ip, "Blacklisted")
        return False

    # Block high-security requests unless IP is trusted
    if level > SECURITY_LEVELS["medium"] and ip not in TRUSTED_IPS:
        log_event("BLOCKED", ip, "MLS violation")
        return False

    log_event("ALLOWED", ip, "Access granted")
    return True

# ---------------- HTTP HELPERS ----------------
def recv_until_headers_end(conn, max_bytes=65536):
    conn.settimeout(3)
    data = b""
    while b"\r\n\r\n" not in data and len(data) < max_bytes:
        chunk = conn.recv(4096)
        if not chunk:
            break
        data += chunk
    return data

def parse_security_level_from_headers(header_bytes):
    # Default low
    level = SECURITY_LEVELS["low"]
    try:
        header_text = header_bytes.decode("iso-8859-1", errors="replace")
        for line in header_text.split("\r\n"):
            if line.lower().startswith("x-sec-level:"):
                val = line.split(":", 1)[1].strip()
                if val.isdigit():
                    level = int(val)
                elif val.lower() in SECURITY_LEVELS:
                    level = SECURITY_LEVELS[val.lower()]
                break
    except:
        pass
    return level

def http_forbidden(conn):
    body = b"403 Forbidden (Blocked by firewall)\n"
    resp = (
        b"HTTP/1.1 403 Forbidden\r\n"
        b"Content-Type: text/plain\r\n"
        b"Connection: close\r\n"
        + f"Content-Length: {len(body)}\r\n\r\n".encode()
        + body
    )
    try:
        conn.sendall(resp)
    except:
        pass

# ---------------- PROXY HANDLER ----------------
def proxy_to_backend(client_conn, initial_data):
    # Forward request to backend, then stream response back
    backend = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    backend.settimeout(5)
    backend.connect((BACKEND_HOST, BACKEND_PORT))

    # Send the request we already received (headers etc.)
    backend.sendall(initial_data)

    # If client sent only headers and will send body (POST), forward remaining data too
    client_conn.settimeout(1)
    try:
        while True:
            more = client_conn.recv(4096)
            if not more:
                break
            backend.sendall(more)
            # For typical demo (GET/curl), this will stop quickly
            if len(more) < 4096:
                break
    except:
        pass

    # Relay backend response to client
    try:
        while True:
            chunk = backend.recv(4096)
            if not chunk:
                break
            client_conn.sendall(chunk)
    finally:
        backend.close()

# ---------------- CLIENT HANDLER ----------------
def handle_client(conn, addr):
    ip = addr[0]
    try:
        data = recv_until_headers_end(conn)
        if not data:
            conn.close()
            return

        level = parse_security_level_from_headers(data)

        with lock:
            allowed = rate_limiter(ip) and enforce_mls(ip, level)

        if not allowed:
            http_forbidden(conn)
            return

        # Allowed -> forward to internal protected service
        proxy_to_backend(conn, data)

    except Exception as e:
        log_event("ERROR", ip, str(e))
        try:
            http_forbidden(conn)
        except:
            pass
    finally:
        conn.close()

def start_firewall(host=FIREWALL_HOST, port=FIREWALL_PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(50)
    print(f"[+] Firewall proxy listening on {host}:{port} -> {BACKEND_HOST}:{BACKEND_PORT}")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

# ---------------- ADMIN CONTROL (GUI) ----------------
def handle_admin(conn):
    try:
        cmd = conn.recv(1024).decode(errors="ignore").strip()
        parts = cmd.split()

        with lock:
            if len(parts) == 2 and parts[0] == "BLOCK":
                BLACKLIST.add(parts[1])
                log_event("MANUAL BLOCK", parts[1], "Blocked via GUI")
                conn.sendall(b"OK: IP BLOCKED\n")

            elif len(parts) == 2 and parts[0] == "UNBLOCK":
                BLACKLIST.discard(parts[1])
                request_count[parts[1]] = 0
                log_event("UNBLOCKED", parts[1], "Unblocked via GUI")
                conn.sendall(b"OK: IP UNBLOCKED\n")

            else:
                conn.sendall(b"ERROR: INVALID COMMAND\n")
    finally:
        conn.close()

def start_admin_server(host="127.0.0.1", port=9999):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)
    print(f"[+] Admin control listening on {host}:{port}")

    while True:
        conn, _ = s.accept()
        threading.Thread(target=handle_admin, args=(conn,), daemon=True).start()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    threading.Thread(target=start_admin_server, daemon=True).start()
    start_firewall()
