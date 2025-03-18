# Hint:
- Host 1: Choose the right payload.
- Host 2: Remember how you accessed the blog.
- Host 3: It's too easy when using Metasploit.
# Host 1:
- Accessing the IP of host 1 on port 8080, we reach the Tomcat page. Next, we attempt to access the Tomcat Manager App. At this point, we don't have the credentials to log in to the Tomcat manager page.<br>
![image](https://github.com/user-attachments/assets/e212b2a0-3ac4-4a0d-bae5-77c4d2a6a7a7) <br>
- Looking at our Foothold machine, we found a file named access-creds.txt. It is likely that this file contains login credentials for various applications.<br>
![image](https://github.com/user-attachments/assets/096595b2-7e54-463c-b62d-5bfcd50ba73c) <br>
- Proceed to log in and look for a place where we can upload a shell. The Tomcat Manager previously had a vulnerability related to file uploads.<br>
- After identifying the vulnerable file upload location, we attempt to upload a shell. This application only accepts files with the .war extension. Therefore, we will use msfvenom to generate a reverse shell with a .war extension.<br>
![image](https://github.com/user-attachments/assets/bd55258b-5da1-40c6-9c60-a0c7c96a64a6) <br>
- Proceed to upload the shell file. <br>
![image](https://github.com/user-attachments/assets/4e61279d-c4eb-4bc5-a986-bc513fb9ec7b) <br>
- At this point, we see that after deploying the WAR file, Tomcat has automatically extracted and deployed it as an application directory displayed as /shell02.<br>
![image](https://github.com/user-attachments/assets/95776c18-cefc-4be0-af52-5e7534c8c880) <br>
- Set up an nc handler and access the path of the file we just uploaded. <br>
![image](https://github.com/user-attachments/assets/eba85334-fa23-47aa-bf37-f41af2eb721a) <br>
- We have obtained a shell on host1.<br>
![image](https://github.com/user-attachments/assets/05714c31-be79-41c3-9d2d-ca9987fcdb0f) <br>

# Host 2:
- On host2, we access blog.inlanefreight.local, which requires login credentials stored on our jump machine. After logging in, we find a post mentioning that this blog has an RCE vulnerability, referenced in Exploit-DB with ID 50064. <br>
![image](https://github.com/user-attachments/assets/54f86694-64e8-4ec8-8714-d1579b00e38f) <br>
- After accessing the blog post link, we see that this is an exploit code that we can import into Metasploit for exploitation.<br>
![image](https://github.com/user-attachments/assets/95b1f1fe-8094-46e5-95a4-6beac942c76d) <br>
- Download the exploit code and save the file with the .rb extension (this is the extension used for Metasploit modules). After moving the file to the appropriate directory (/usr/share/metasploit-framework/modules/exploits/.../.../), access msfconsole and run reload_all to reload the exploit modules. Then, configure the basic target information.<br>
![image](https://github.com/user-attachments/assets/8901a39e-f34d-4f76-9a2f-80d9725a79c0) <br>
- The next step is to choose a payload for this exploit module.<br>
![image](https://github.com/user-attachments/assets/af125c8c-8307-4152-9191-4c4c76e58667) <br>
- After running the exploit, it was unsuccessful. I'm thinking about what might have gone wrong.
![image](https://github.com/user-attachments/assets/a9710bcc-35d8-490d-861d-79245ed6940b) <br>
- I suddenly realized that I was accessing the blog using a virtual host, so we need to set the vhost parameter for the exploit module. After setting it and running the exploit—boom! We have obtained a shell on host02.<br>
![image](https://github.com/user-attachments/assets/2c65e49d-2e56-4965-95f6-de5413ad3e46) <br>

# Host 3:
- According to the hint for host3, this machine has a vulnerability related to 'blue' and was quite well-known in 2017. From this, we can immediately think of EternalBlue, a famous vulnerability associated with the WannaCry malware.<br>
- Since my internet is quite slow, making VPN and remote access to the Foothold machine sluggish, I decided to use Metasploit's exploit module to speed up the process.<br>
![image](https://github.com/user-attachments/assets/f83fb785-0518-4289-b436-cc30902b2f08) <br>
- Bonus: If you want to exploit it manually without using Metasploit, host3 also has port 80 open, and we can upload files freely without any restrictions.<br>
![image](https://github.com/user-attachments/assets/99211b0a-4653-4d31-b5ba-f61b8d148941)













