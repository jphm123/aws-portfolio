import socket
import datetime
import threading
from remediation import block_ip

HONEYPOT_PORT = 2222

def handle_attacker(client_socket, address):
    ip_address = address[0]
    print(f"\n[⚠️ INTRUSION DETECTED] Connection from: {ip_address}")
    
    try:
        # Send a fake Ubuntu SSH banner to trick the bot
        client_socket.send(b"SSH-2.0-OpenSSH_8.9p1 Ubuntu-3ubuntu0.1\r\n")
        
        # Safety Check: Prevent locking ourselves out during testing
        if ip_address == "127.0.0.1":
            print("[INFO] Local test detected. Bypassing firewall injection.")
        else:
            print(f"[ACTION] Routing {ip_address} to Remediation Engine...")
            block_ip(ip_address)

    except Exception as e:
        pass
    finally:
        client_socket.close()

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to all network interfaces on port 2222
    server.bind(("0.0.0.0", HONEYPOT_PORT))
    server.listen(5)
    
    print("=" * 60)
    print(f"🍯 anLog Honeypot Active. Listening on port {HONEYPOT_PORT}...")
    print("=" * 60)

    while True:
        client, addr = server.accept()
        # Handle the attack in the background so we can catch multiple at once
        client_handler = threading.Thread(target=handle_attacker, args=(client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_honeypot()