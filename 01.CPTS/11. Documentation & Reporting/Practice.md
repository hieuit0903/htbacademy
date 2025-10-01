- Identify the IP of the DC — you can find it in the report, but I’ll put it here: 172.16.5.5. This machine is really slow; I even used Pwnbox to remote into it instead of VPN on my host, which annoyed me because every action lagged while I was writing the detailed write-up.<br>
- Use LLMNR/NBT-NS poisoning from Linux: <br>
```
sudo responder -I ens224 -wrf
```
- Watch the responder console output — you’ll see accounts such as networkcluster, backupagent, svc_qualys, ... (when you see these, you can make an initial guess about which users might have high privileges; if you’re unsure, run BloodHound to verify).<br>
- Crack the captured hashes for the relevant user and log directly into the Domain Controller using evil-winrm.<br>
- Once on the DC and after obtaining admin credentials, use secretdump to dump hashes:<br>
```
secretsdump.py 'INLANEFREIGHT.LOCAL/BACKUPAGENT:Recovery7'@172.16.5.5 >> hash.txt
```
- After obtaining the hash for svc_reporting, crack it with Hashcat using mode 1000 (NTLM).
- Back in the Evil-WinRM admin console, run **net user svc_reporting** to see which groups this account belongs to — you’ll quickly spot the special/privileged group.
