import socket
import sys
import hashlib
import datetime

# The final cyberpunk banner layout with clear impact text
BANNER = """\033[95m
┌────────────────────────────────────────────────────────────────────────────────────────────────┐
  [!!] CONNECTION QUARANTINED // ACTIVE NETWORK INVERSION ENGAGED 
└────────────────────────────────────────────────────────────────────────────────────────────────┘

    You poked a dark-routing node thinking it was empty. 
    The socket has trapped your sequence. We are extracting your network blueprint right now.

    >>> EXTRAPOLATING CLIENT INTRUSION METADATA <<<

    [⚡] CAPTURED NETWORK IP     : {ip_address} 
        -> Meaning: Your precise digital address on the public web.
        
    [⚡] CARRIER HOSTNAME       : {hostname} 
        -> Meaning: Your localized ISP node. We know your provider and territory.
        
    [⚡] CLIENT DEVICE KERNEL   : {os_guess} (TTL={ttl_val}) 
        -> Meaning: Handshake packet fingerprints exposed your machine's core operating system.
        
    [⚡] EVENT TIMELINE MARKER  : {timestamp} 
        -> Meaning: Microsecond-accurate forensic log entry pinned to your connection session.
        
    [⚡] EXTRAPOLATED HOST HASH : {hardware_hash} 
        -> Meaning: A unique target signature bound to your connection routing logic.
        
    [⚡] DECK IDENTIFIER SYNC   : {threat_uuid} 
        -> Meaning: Global threat tracking token generated and locked to this intrusion.


    [!] IMMEDIATE NETWORK RETALIATION EXECUTED:
    
    1. INBOUND PORT MIRRORING  : Every packet you send is being duplicated, mirrored, and forensically logged.
    2. DESTRUCTIVE GATEWAY BGP : Network routing poisoning requests submitted to block your IP segment.
    3. INFRASTRUCTURE SHADOWING: Automated defense profiles pushed to global security syndicates.


    ALL THESE IDENTIFIERS HAVE BEEN COLLECTED AND YOUR IDENTITY HAS BEEN COMPROMISED. 
    CONSIDER THIS A WARNING.

──────────────────────────────────────────────────────────────────────────────────────────────────
\033[0m"""

def get_hostname(ip):
    """Attempts to resolve the attacker's public IP to an ISP hostname."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "UNRESOLVED_ISP_NODE_MAPPED"

def analyze_ttl(ttl):
    """Passively fingerprints the Operating System category using standard TTL initial values."""
    if ttl is None:
        return "UNIDENTIFIED_KERNEL_TARGET"
    
    if 64 < ttl <= 128:
        return "MICROSOFT_WINDOWS_ENVIRONMENT (NT_KERNEL)"
    elif 0 < ttl <= 64:
        return "UNIX/LINUX/MAC_OS_ENVIRONMENT (POSIX_KERNEL)"
    else:
        return "RESTRICTED_OS_ARCH_DETECTED"

def generate_convincing_hash(ip, salt):
    """Generates a realistic, scary-looking cryptographic tracking signature."""
    hash_object = hashlib.sha256(f"{ip}{salt}".encode())
    return hash_object.hexdigest().upper()[:24]

def generate_uuid(ip):
    """Generates a fake but realistic threat index identifier."""
    hash_object = hashlib.md5(ip.encode())
    h = hash_object.hexdigest().upper()
    return f"{h[:8]}-{h[8:12]}-4{h[13:16]}-{h[16:20]}-{h[20:]}"

def start_honeypot(host='0.0.0.0', port=4444):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.setsockopt(socket.IPPROTO_IP, socket.IP_RECVTTL, 1)
    except Exception as e:
        print(f"[*] Warning: Advanced IP_RECVTTL flag not supported natively on this host subsystem: {e}")

    try:
        server_socket.bind((host,
