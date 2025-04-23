# Skill Assessment:
- According to the challenge description, we are given a webshell on the foothold server. We will use this foothold server to pivot and enumerate other hosts. Proceed to answer the questions after gathering information from the foothold server.<br>
![image](https://github.com/user-attachments/assets/235fa95e-aa0a-46b5-b851-26874da2ae83) <br>
- While reading a file in the home directory of the webadmin user, we discovered login credentials for another server. <br>
<img width="289" alt="image" src="https://github.com/user-attachments/assets/cee9cede-4d9c-41c6-bb9c-b808e1d5e091" /> <br>
- I will use Metasploit to perform pivoting (refer back to the lesson content for detailed steps). After configuring the proxy, I will scan for online hosts within the 172.16.5.0/16 IP range. I discovered two IPs — one belonging to the foothold server and another belonging to a different machine.<br>
<img width="191" alt="image" src="https://github.com/user-attachments/assets/5c41a77f-66ff-43c9-b095-e7673589bce8" /> <br>
- I performed an Nmap scan on the .35 server and found several open ports, including RDP, SMB, and others.<br>
![image](https://github.com/user-attachments/assets/68635206-a42e-44b2-a2b1-09a386d9d6df)
- Using the credentials found in the file, I successfully logged in to the discovered server via RDP.<br>
![image](https://github.com/user-attachments/assets/4915a071-68f3-4573-a07e-81b9c5ec2ad3) <br>
- At this point, I proceeded to enumerate the server and found the first flag file. I then read its contents and submitted the answer.<br>
![image](https://github.com/user-attachments/assets/1877d1d6-c8a7-47f9-97c6-1f9b8d153e2a) <br>
- The task requires identifying a vulnerable user, and the hint suggests dumping credentials from the LSASS process. I transferred Mimikatz to the target server and used it to dump the LSASS process. From the output, I was able to extract additional credentials belonging to the user vfrank.<br>
![image](https://github.com/user-attachments/assets/d9513306-b694-48f4-99a6-4aaed0ec6033) <br>
- I proceeded to use the runas command to launch a command prompt as the user vfrank.<br>
![image](https://github.com/user-attachments/assets/761898d4-103e-4a81-92af-9c8d9f72206e) <br>
- Next, we need to enumerate which hosts are active within the 172.16.6.0 range. During this step, we discovered that two hosts are online: 172.16.6.25 and 172.16.6.45.<br>
![image](https://github.com/user-attachments/assets/c5960ffa-f0b7-4c92-9627-5826c6fc674d) <br>
![image](https://github.com/user-attachments/assets/4a6a0480-6d8d-436c-9b1a-03a24f5d772a) <br>
- From the CMD session running as vfrank, we will proceed to RDP into the servers at 172.16.6.25 and 172.16.6.45 to retrieve the flag files.<br>
![image](https://github.com/user-attachments/assets/81e73800-1220-4478-aea2-e88490f79281) <br>
![image](https://github.com/user-attachments/assets/00adc0a7-558c-4eaa-901a-399b8afe6faa) <br>
- There is a shared drive on this machine. Accessing it, we are able to obtain the final flag.<br>
![image](https://github.com/user-attachments/assets/af8a3e2b-b903-4047-8966-aebb7c40b12f)












