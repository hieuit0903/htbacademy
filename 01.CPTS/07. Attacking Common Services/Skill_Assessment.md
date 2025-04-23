# Hint:
# Easy Lab: I forgot to capture so I will update it later.
# Medium Lab:
- Be careful — make sure to use -p- in your Nmap scan and take a break with a cup of coffee while waiting for the results. I made the mistake of only scanning the top 1000 ports and wasted a lot of time brute-forcing.<br>
- After scanning all ports, I found that the FTP service was actually running on a non-standard port (30021 and 2121). HTB tricked us here — I spent almost 3 hours brute-forcing this service and even went down the rabbit hole of DNS exploitation. I overthought things and failed right at the recon step. Totally my fault.<br>
![image](https://github.com/user-attachments/assets/1a1132dc-7692-4838-a718-cb0b3dc4de85)<br>
- After discovering that the FTP service allows anonymous login, I accessed it and looked for more information. Inside, I found a folder named simon and a file named note, which contains several lines that appear to be possible passwords.<br>
- I downloaded this file and used it to perform a brute-force attack against the FTP and POP3 services, using simon as the username and each line in the note as a potential password.<br>
![image](https://github.com/user-attachments/assets/71cf877d-102b-4727-972d-27693056e85e) <br>
- As expected, we successfully discovered valid credentials to log in to the FTP service running on port 2121.<br>
![image](https://github.com/user-attachments/assets/6ce7b799-79a2-4d62-8726-b65129e3555c) <br>
- This lab is labeled as medium, but in my opinion, it feels fairly easy—as long as you pay close attention to the recon phase. Most of the challenge lies in thorough scanning and enumeration.<br>
![image](https://github.com/user-attachments/assets/ac7dce88-7f6b-484b-aa38-49c5d07fd201) <br>

# Hard Lab:
- Proceed to perform an Nmap scan on the target machine to identify open ports and running services. <br>
![image](https://github.com/user-attachments/assets/dfbbe9f5-7128-441e-929f-e12b64b20319) <br>
- Brute force using the username "simon" as required by the question in the assignment.<br>
![image](https://github.com/user-attachments/assets/1be96fea-f13b-4b63-b9dc-06939b2bd69d) <br>
- Found a shared directory belonging to the user "simon".<br>
![image](https://github.com/user-attachments/assets/86e32e8d-6527-4720-9864-c697c091b97a) <br>
- Logged in with the user "simon" and proceeded to search for information within the SMB share.<br>
![image](https://github.com/user-attachments/assets/2203996a-602b-40d3-a0cd-3bd13aea1b72) <br>
- Using the information found in the SMB share, proceed to search for the password for the user "fiona".<br>
![image](https://github.com/user-attachments/assets/7328bf1d-b637-4931-9308-9a8d89cabd8d) <br>
- Next, we found a reference to a database in John's folder, suggesting that this user may have login privileges to the database. We attempted to brute-force the MSSQL login with the user "john" and the password found in John's folder. However, brute-forcing with users "john," "fiona," or "simon" using the credential files from the SMB share all failed. Therefore, we decided to brute-force RDP to check if we could gain access to the RDP service.<br>
![image](https://github.com/user-attachments/assets/ea1d49dc-aa7c-4fdb-ab1d-0774719e0ff7) <br>
- After successfully accessing the RDP, I tried logging into MSSQL Management Studio using Windows Authentication, but encountered an error. Therefore, I switched to using mssqlclient with the -windows-auth parameter to log in. Upon further reconnaissance, I discovered that I did not have permission to access any databases on this MSSQL server, and I was also unable to execute xp_cmdshell. As a result, I decided to conduct a deeper investigation.<br>
![image](https://github.com/user-attachments/assets/c6ed2669-8a0e-4c25-b2e5-0f3632721a04) <br>
- After discovering that there are two users we can impersonate, and noting that the contents of the text file for user John in the SMB share were related to the database, it seems likely that John is a database administrator. Therefore, I decided to impersonate user John to attempt gaining elevated privileges on the MSSQL server.<br>
![image](https://github.com/user-attachments/assets/70eb7872-2f84-48a5-b0f9-4dd4d0c5d522) <br>
- Even though we impersonated John, we still didn't have any privileges on the DB server. We decided to check if there were any linked servers, and we discovered a local test DB server. However, when we tried using user Fiona, it returned an error with NT Authority, indicating that Fiona didn't have permission on this DB server. This gave us a clue that there might be a way to escalate privileges or find another user with the appropriate permissions.<br>
![image](https://github.com/user-attachments/assets/2e0e830a-f31c-4485-b9b0-c176143c8a01) <br>
- After impersonating the user John, we discovered that we now had full sysadmin privileges on the DB server. This gave us complete control over the database, allowing us to execute commands, query sensitive data, and potentially escalate further or extract the flag.<br>
![image](https://github.com/user-attachments/assets/dd64ba18-140e-4f2a-b9e2-59e5c7d84802) <br>
- If we attempt the xp_cmdshell command and find that the component is disabled, we can re-enable it and reconfigure the database to allow execution of shell commands.<br>
![image](https://github.com/user-attachments/assets/2f86e9ef-23ef-4bef-87ec-814f190b169b) <br>
- Execute the following query with the EXECUTE command: "EXECUTE('EXEC sp_configure ''show advanced options'', 1; RECONFIGURE; EXEC sp_configure ''xp_cmdshell'', 1; RECONFIGURE;') AT [LOCAL.TEST.LINKED.SRV];". Then, try running the command whoami, and we have successfully enabled xp_cmdshell.<br>
![image](https://github.com/user-attachments/assets/3f9c7fa4-27e9-4550-8e0e-cece5af3512c) <br>
- Now we just need to locate the path containing the flag.txt file and read the result.<br>
![image](https://github.com/user-attachments/assets/3f1e612f-602e-4255-92bc-93eb2b7f5a25) <br>












