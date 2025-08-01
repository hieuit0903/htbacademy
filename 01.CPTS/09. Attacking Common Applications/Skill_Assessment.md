# Lab 1:
# Hint: Using metasploit for quick exploit
- Perform an nmap scan on the target and discover that it is running Tomcat version 9.0.0.M1. After researching online, I found that this version has a vulnerability related to CGI exploitation and that there is a Metasploit module available to exploit it.<br>
<img width="792" height="520" alt="image" src="https://github.com/user-attachments/assets/ad6da7d1-e445-42c3-a540-d83d78b3a486" /> <br>
- The next step is to find the location of the CGI executable script file.<br>
<img width="816" height="454" alt="image" src="https://github.com/user-attachments/assets/4790e503-cf70-4b72-8026-f8b9cd134f53" /> <br>
- To save time, I will use Metasploit to exploit it by simply providing the required information such as URI, RHOST, RPORT, etc. At this point, the exploitation will be successful. It is also possible to exploit it manually by uploading VBS payloads to the target machine and executing them using cscript.exe.<br>
<img width="913" height="1003" alt="image" src="https://github.com/user-attachments/assets/33060a75-ed17-4cbc-beeb-a6c4a6493d77" /> <br>

# Lab 2:
# Hint: Exploit-DB is a good place to find a script.
- Perform an Nmap scan and discover several notable ports, including the GitLab port 8081 and some web ports as stated in the task. Next, configure the vhost and access GitLab.<br>
<img width="789" height="428" alt="image" src="https://github.com/user-attachments/assets/77764510-7753-40ec-b965-fc80e29bed5e" /> <br>
- First, enumerate port 80 and find another vhost—answer question 1. Then configure the vhost and enumerate the WordPress site using wpscan. For now, leave these results aside and proceed to access GitLab. <br>
<img width="975" height="744" alt="image" src="https://github.com/user-attachments/assets/a85cef1f-bb16-460d-a5b9-7d5529caae87" /> <br>
- Configure the vhost and access GitLab. Register a new user to see if there is anything interesting inside.<br>
<img width="975" height="457" alt="image" src="https://github.com/user-attachments/assets/31d641c7-dbe0-424c-9866-8a65a45f361c" /> <br>
- Explore around to check if there are any publicly accessible projects. And we found that there are public projects named Virtual Host and Nagios, which suggests that this site is preparing to deploy a monitoring solution.<br>
<img width="975" height="319" alt="image" src="https://github.com/user-attachments/assets/c3559759-ba91-4a7b-a425-f7506a104d7f" /> <br>
- Proceed to gather information to answer the remaining questions. By further enumerating these two projects, we discovered a new vhost.<br>
<img width="856" height="409" alt="image" src="https://github.com/user-attachments/assets/e1ecc267-1221-47bd-8341-1bc2cdae9d25" /> <br>
- By searching for more information, we found an admin password for Nagios login.<br>
<img width="935" height="763" alt="image" src="https://github.com/user-attachments/assets/a32f0efe-5bb2-4cf7-9186-3007ee7554f4" /> <br>
- Proceed to map the vhost and use these credentials to log in to Nagios. After logging in, we found the version of the running Nagios instance.<br>
<img width="398" height="138" alt="image" src="https://github.com/user-attachments/assets/9e01feb7-d8a1-4468-8774-16ba7e1e5961" /> <br>
- After researching, we found that this version is affected by a CVE leading to RCE. However, the CVE requires admin privileges to exploit. Luckily, we already have admin credentials from the beginning. To proceed quickly, we will use the exploit from Exploit-DB to perform the attack.<br>
<img width="975" height="521" alt="image" src="https://github.com/user-attachments/assets/8cfc3af0-f114-4281-9016-f89976f0f60e" /> <br>
- Boom! We have obtained a shell as the www-data user. However, since the task only requires retrieving the flag in the current directory, there is no need to perform privilege escalation.<br>
<img width="975" height="154" alt="image" src="https://github.com/user-attachments/assets/1ee0d221-9e51-4ba3-b7ae-a827a9a52f4c" /> <br>

# Lab 3:
# Hint: :V
- Hack The Box is known for its vague questions, and sometimes the labs are label easy but take a lot of time to exploit. However, I couldn’t believe they would create a lab where you could find the flag in just a few steps. I was suspicious because the cube for this question was 0 instead of 1, unlike the previous labs. Just decompile the source code and look around—you’ll find the answer.<br>
<img width="975" height="592" alt="image" src="https://github.com/user-attachments/assets/0ea39499-49ff-4f6e-8d1b-e22376b47298" /> <br>












