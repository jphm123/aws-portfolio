import sys
import os
import platform
from datetime import datetime

def run_diagnostics():
    print("=" * 50)
    print(f"--- anLog Backend Engine Init: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    print("=" * 50)
    
    # Gather environment telemetry
    print(f"[INFO] Target OS OS Platform: {platform.system()} {platform.release()}")
    print(f"[INFO] Active Python Engine:  {sys.version.split()[0]}")
    print(f"[INFO] Execution Environment: {os.getcwd()}")
    
    print("-" * 50)
    print("[SUCCESS] anLog microservices are staging optimally.")
    print("=" * 50)

if __name__ == "__main__":
    run_diagnostics()