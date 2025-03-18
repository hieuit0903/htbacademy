# Hint:
- Lab 1: Buffer overFlow.
- Lab 2: Perform an Nmap scan carefully.
# Sessions Section Lab:
- Since the challenge has already given us some information about this machine, stating that it is running a website, we proceed to access it and check the source code. Upon inspection, we discover that the web server is running elFinder.<br>
- Access msfconsole and search for an exploit module for elFinder. After selecting the module, configure the necessary parameters.<br>
![image](https://github.com/user-attachments/assets/cf24c23f-fd26-4faf-8b44-409c4ef67b27) <br>
- Exploitation successful.<br>
![image](https://github.com/user-attachments/assets/b627ec2e-dc5a-4be9-ae39-4645aa36bb7f) <br>
![image](https://github.com/user-attachments/assets/71c94555-2aac-427e-a833-89c8f8c2a2e8) <br>
- However, we only obtained a low-privilege shell, so we need to escalate privileges. The hint suggests that the sudo version on this machine is outdated, meaning there might be an exploit available for this version.<br>
![image](https://github.com/user-attachments/assets/39266d03-7498-4017-b31b-11c9839cdaf4) <br>
- After researching, I found that this version is vulnerable to a buffer overflow exploit.<br>
![image](https://github.com/user-attachments/assets/25ecaa23-16f9-4171-94fd-71cfc00ee9e2) <br>
- Since I'm already using Metasploit, I decided to look for an exploit module for privilege escalation.<br>
![image](https://github.com/user-attachments/assets/a497cad5-b015-45c5-b081-6dfc0e2f4ec4) <br>
![image](https://github.com/user-attachments/assets/9e13fb04-35b9-4f34-90ac-ed689698a1e6) <br>

# Meterpreter Section Lab:
- Proceed with an Nmap scan and discover that this machine is running a web service on port 5000.<br>
![image](https://github.com/user-attachments/assets/a8ba2e25-6395-4b51-a3df-95a8075f1da2) <br>
- Detected that the running service is FortiLogger." Now, let's check for known vulnerabilities related to FortiLogger
![image](https://github.com/user-attachments/assets/bd67b76c-3f61-4126-bda2-49b3034ff56e) <br>
- Find the exploit module on Metasploit, set the required parameters, and execute the exploit.
![image](https://github.com/user-attachments/assets/d96277c6-83ec-4113-a20f-d553a64a02cc) <br>
![image](https://github.com/user-attachments/assets/0c3bb2e5-3dd7-4348-bd03-667b2b345fdb) <br>









