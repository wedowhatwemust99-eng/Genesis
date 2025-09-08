#!/usr/bin/env python3
"""
🛡️ FILE INTEGRITY MONITOR - Detect Mysterious Code Changes
===========================================================
Monitors GGUF GUI files for mysterious deletions/modifications
WITHOUT using git or uploading anything to the internet!
"""

import hashlib
import json
import os
import time
from datetime import datetime
from pathlib import Path

class FileIntegrityMonitor:
    def __init__(self):
        self.monitor_file = Path("file_integrity.json")
        self.watched_files = [
            "gguf_gui.py",
            "gguf_extractor.py", 
            "gguf_cli.py"
        ]
        
    def calculate_file_hash(self, filepath):
        """Calculate SHA256 hash of file"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            return f"ERROR: {e}"
    
    def create_baseline(self):
        """Create baseline hashes for all watched files"""
        baseline = {
            "created": datetime.now().isoformat(),
            "files": {}
        }
        
        for filename in self.watched_files:
            if os.path.exists(filename):
                file_hash = self.calculate_file_hash(filename)
                file_size = os.path.getsize(filename)
                
                baseline["files"][filename] = {
                    "hash": file_hash,
                    "size": file_size,
                    "last_modified": os.path.getmtime(filename),
                    "status": "BASELINE"
                }
                print(f"🛡️ Baseline created for {filename}: {file_hash[:16]}...")
        
        with open(self.monitor_file, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        print(f"✅ Baseline saved to {self.monitor_file}")
        return baseline
    
    def check_integrity(self):
        """Check if any files have been mysteriously modified"""
        if not self.monitor_file.exists():
            print("⚠️ No baseline found. Creating baseline...")
            return self.create_baseline()
        
        with open(self.monitor_file, 'r') as f:
            baseline = json.load(f)
        
        changes_detected = False
        
        print(f"🔍 Checking file integrity against baseline from {baseline['created']}")
        
        for filename in self.watched_files:
            if not os.path.exists(filename):
                print(f"❌ FILE MISSING: {filename}")
                changes_detected = True
                continue
            
            current_hash = self.calculate_file_hash(filename)
            current_size = os.path.getsize(filename)
            current_modified = os.path.getmtime(filename)
            
            if filename in baseline["files"]:
                baseline_hash = baseline["files"][filename]["hash"]
                baseline_size = baseline["files"][filename]["size"]
                
                if current_hash != baseline_hash:
                    print(f"🚨 MYSTERIOUS CHANGE DETECTED: {filename}")
                    print(f"   📊 Size: {baseline_size} → {current_size}")
                    print(f"   🔐 Hash: {baseline_hash[:16]}... → {current_hash[:16]}...")
                    print(f"   ⏰ Modified: {datetime.fromtimestamp(current_modified)}")
                    changes_detected = True
                else:
                    print(f"✅ INTACT: {filename}")
            else:
                print(f"🆕 NEW FILE: {filename}")
                changes_detected = True
        
        if changes_detected:
            print("\n🕵️‍♂️ MYSTERIOUS CHANGES DETECTED!")
            print("This could be:")
            print("   - VSCode extensions auto-formatting")
            print("   - Microsoft silent updates")
            print("   - OneDrive sync issues")
            print("   - Auto-cleanup tools")
        else:
            print("\n🛡️ ALL FILES INTACT - No mysterious changes!")
        
        return changes_detected

if __name__ == "__main__":
    monitor = FileIntegrityMonitor()
    
    print("🛡️ FILE INTEGRITY MONITOR - Protecting Against Mysterious Changes")
    print("="*70)
    
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "baseline":
        monitor.create_baseline()
    else:
        monitor.check_integrity()
