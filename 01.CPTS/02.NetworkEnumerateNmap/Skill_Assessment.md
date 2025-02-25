# This section does not have a skill assessment lab, so I decided to provide a quick write-up for the last three labs in this module.
# The easy lab:
- This lab asked me to find the OS name of this machine. So, I tried an Nmap ACK scan and noticed that the TTL value was 63. Since it's close to 64, I guessed there was an 80%~90% chance the OS was Linux. However, when I entered the answer, it was incorrect. Maybe I needed to specify the distro name. So, I performed banner grabbing on some known ports like 80 and found that the HTTP server was running on Ubuntu.
![Image](https://github.com/user-attachments/assets/67e0fc66-3829-4eda-a52d-f905e5a81012)
![Image](https://github.com/user-attachments/assets/964c3407-cae7-4f93-8e02-810718bee1be)
# The medium lab:
- This lab asked me to submit the DNS server version of the target as the answer. I performed a TCP scan on port 53, but it was filtered, so I switched to a UDP scan on the same port and found the DNS server information
![Image](https://github.com/user-attachments/assets/a03212c6-e469-44fa-9ad2-cd8261985f28)
# The hard lab:
- I didn't document this challenge clearly, but try reviewing the Firewall IDS/IPS Evasion section to find a successful Nmap command and a way to get final flag. Good luck to you, just read it carefully.
