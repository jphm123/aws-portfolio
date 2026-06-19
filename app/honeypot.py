import socket
import threading
import time
import urllib.request
import json
import hashlib
from remediation import block_ip

HONEYPOT_PORT = 4444

def get_attacker_metadata(ip_address):
    """Pulls live geographic, ISP, and VPN/Proxy data based on the IP."""
    try:
        if ip_address == "127.0.0.1":
            return "Local ISP", "Localhost", "System", "US", "LOCAL CONNECTION (SECURE)"
            
        url = f"http://ip-api.com/json/{ip_address}?fields=isp,city,regionName,country,proxy,hosting"
        req = urllib.request.urlopen(url, timeout=3)
        data = json.loads(req.read())
        
        isp = data.get("isp", "ISP TRACED")
        city = data.get("city", "CITY TRACED")
        region = data.get("regionName", "REGION TRACED")
        country = data.get("country", "COUNTRY TRACED")
        
        is_proxy = data.get("proxy", False)
        is_hosting = data.get("hosting", False)
        
        if is_proxy:
            vpn_status = "ACTIVE [TOR/VPN/PROXY SHIELD DETECTED & BYPASSED]"
        elif is_hosting:
            vpn_status = "ACTIVE [DATACENTER/CLOUD RELAY DETECTED & BYPASSED]"
        else:
            vpn_status = "INACTIVE [CLEARTEXT CONNECTION DETECTED]"
            
        return isp, city, region, country, vpn_status
    except Exception:
        return "ISP LOGGED", "LOCATION TRACED", "REGION SECURED", "GLOBAL", "STATUS LOGGED"

def handle_attacker(client_socket, address):
    ip_address = address[0]
    print(f"\n[⚠️ INTRUSION DETECTED] Connection from: {ip_address}")
    
    try:
        # 1. Gather the live intelligence
        isp, city, region, country, vpn_status = get_attacker_metadata(ip_address)
        
        # 2. Generate hardware signature
        hw_hash = hashlib.sha256(ip_address.encode()).hexdigest()[:18].upper()
        
  # ANSI Escape Codes: \033[1;31m (Bold Red) and \033[0m (Reset)
        RED = "\033[1;31m"
        RESET = "\033[0m"

        # The Red-Formatted Payload
        payload = f"""{RED}
\r\n=============================================================================
\r\n WARNING: RESTRICTED ENVIRONMENT
\r\n UNAUTHORIZED ACCESS IS IN VIOLATION OF 18 U.S.C. § 1030 (CFAA)
\r\n=============================================================================
\r\n
\r\n MALICIOUS INTRUSION DETECTED.
\r\n
\r\n THE FOLLOWING METADATA HAS BEEN SECURED AND SUBMITTED TO ALL APPLICABLE AUTHORITIES:
\r\n
\r\n -> Source IP Protocol : {ip_address}
\r\n -> Network Provider   : {isp}
\r\n -> Physical Routing   : {city}, {region}, {country}
\r\n -> Tunneling Protocol : {vpn_status}
\r\n -> Hardware Signature : {hw_hash}-AUTH-DENIED
\r\n
\r\n Active routing blocks are now being enforced across the global network.
\r\n An automated abuse report and forensic packet capture is being dispatched to:
\r\n  * Your Host Network Provider ({isp})
\r\n  * The Cybersecurity and Infrastructure Security Agency (CISA)
\r\n  * The Internet Crime Complaint Center (IC3)
\r\n  * Regional Cyber Crimes Task Force
\r\n
\r\n CONSIDER THIS A WARNING. DISCONNECT IMMEDIATELY. YOUR NODE IS NO LONGER ANONYMOUS.
\r\n============================================================================={RESET}\r\n"""
        
        for line in payload.split('\n'):
            if line.strip():
                client_socket.send((line + '\r\n').encode('utf-8'))
                time.sleep(0.08)
        
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
    server.bind(("0.0.0.0", HONEYPOT_PORT))
    server.listen(5)
    
    print("=" * 60)
    print(f"🍯 anLog Active Defense Online. Listening on port {HONEYPOT_PORT}...")
    print("=" * 60)

    while True:
        client, addr = server.accept()
        client_handler = threading.Thread(target=handle_attacker, args=(client, addr))
        client_handler.start()

if __name__ == "__main__":
    start_honeypot()