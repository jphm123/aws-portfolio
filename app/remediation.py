import platform
import subprocess
import datetime

def block_ip(ip_address):
    print("=" * 60)
    print(f"🚨 [ALERT] THREAT DETECTED: {ip_address}")
    print(f"🕒 Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    
    current_os = platform.system()
    
    # --- WINDOWS: LOCAL TESTING MODE ---
    if current_os == "Windows":
        print("[INFO] Windows developer environment detected.")
        print("[ACTION] Simulating network level block...")
        print(f"[DRY-RUN EXECUTION] -> sudo ufw deny from {ip_address}")
        print("\n✅ [SUCCESS] Threat neutralized (Simulation Mode).")
        return True
        
    # --- LINUX: LIVE PRODUCTION MODE ---
    elif current_os == "Linux":
        print("[INFO] AWS Ubuntu production environment detected.")
        print("[ACTION] Injecting permanent firewall rule...")
        
        try:
            # The actual Linux command to permanently ban an IP
            command = ["sudo", "ufw", "deny", "from", ip_address]
            
            # Execute the command at the system level
            result = subprocess.run(command, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"\n✅ [SUCCESS] UFW updated: {ip_address} is permanently blackholed.")
                return True
            else:
                print(f"\n❌ [ERROR] Firewall injection failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"\n☠️ [FATAL] System execution error: {e}")
            return False

if __name__ == "__main__":
    # We will feed a dummy "attacker" IP into the engine to test it
    test_attacker_ip = "198.51.100.42"
    
    print("Starting anLog Remediation Engine...")
    block_ip(test_attacker_ip)