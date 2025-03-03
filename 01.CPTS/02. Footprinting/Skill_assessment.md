# Hints:
- Read these hints and try to solve it yourself before referring to the write-up. <br>
- Easy lab: It is a port outside the well-known 1000 ports. <br>
- Medium lab: Try logging in as another user. <br>
- Hard lab: Using UDP scan. <br>
# The easy lab:
- Performing an Nmap scan on the target revealed the following open ports, including FTP. Since FTP is a protocol prone to misconfigurations, we should check whether any misconfigurations exist in this service. <br>
 ![Image](https://github.com/user-attachments/assets/c60a1d35-8a13-43f8-821c-b95088aabdf0) <br>
- We have been provided with the information 'ceil', so let's try using it for the FTP service. We successfully logged in, but there is no useful information here. <br>
 ![Image](https://github.com/user-attachments/assets/59a45c08-e0c3-400c-b10d-4db72e312897)
 - Now, let's proceed with DNS enumeration. From the banner, we can see that this company’s domain is inlanefreight.htb. We perform DNS enumeration to gather more information. However, after attempting a zone transfer, we did not obtain any useful information. <br>
 ![Image](https://github.com/user-attachments/assets/e74f4266-f897-4c3f-b7bb-afe6f0e4b57d) <br>
 - However, when I checked back on the ongoing Nmap scan, I discovered another open port: 2121. Based on my assumption, this could be another FTP server. I proceeded to use the previously obtained credentials to log into this FTP server. <br>
 ![Image](https://github.com/user-attachments/assets/5523f368-e9ce-47de-8039-60ec8fd463e3) <br>
 - Login was successful, and I listed some interesting directories, including the .ssh directory. I proceeded to download the SSH authorized key and used it to log in without needing a password. <br>
 ![image](https://github.com/user-attachments/assets/74f6ae90-728c-47fc-a9de-edae754829b3) <br>
 - Now, we just need to locate and read flag.txt somewhere within the directories on this server.
 ![image](https://github.com/user-attachments/assets/3bda6cb3-529b-4a14-9e15-c8017a42599c) <br>
 # The medium lab:
 - I forgot to capture the video so I'll update it later.
 # The hard lab:
 - Performed an Nmap scan and found open ports for IMAP, POP3, and SSH.
 - In this lab, we don't have any credentials to log in to the IMAP or POP3 server, so let's try to find them. I spent around two hours trying to find other open ports for enumeration, but Nmap still hadn't finished. I was stuck without any hints from HTB. <br>
 ![image](https://github.com/user-attachments/assets/4dc4d40f-c7f4-479a-9729-8dc7789916fa) <br>
 - After that, I performed a UDP scan, which took a long time. So, I decided to look for hints in the HTB forum, where I found a suggestion about the SNMP protocol. I then specifically scanned this port and discovered that it was open. <br>
 ![image](https://github.com/user-attachments/assets/07ef55e8-de35-4bc4-948f-4faa30025dad) <br>
 - I used snmpwalk to enumerate SNMP with some common community strings like public and private, but nothing worked. So, I performed community string enumeration using onesixtyone. After that, I found the correct community string. I then went back and used snmpwalk with that string. <br>
 ![image](https://github.com/user-attachments/assets/8e628f48-7c61-40d7-b792-c3a306825f42) <br>
 - After snmpwalk finishes, we find some information related to credentials.
 ![image](https://github.com/user-attachments/assets/0196dc6e-00bb-4c6d-ad7d-a32975f06a8c) <br>
 - The first protocol I tried to exploit was POP3 on port 110. I logged in successfully and found an email containing a key. I suspected it might be an SSH key, so I copied it to my machine and used it to log in via SSH. <br>
 ![image](https://github.com/user-attachments/assets/b3147df9-1ef4-413a-b97f-b8c049812bf6) <br>
 - Logged in successfully! Now, let's look around for anything that might reveal the password of the HTB user. <br>
 ![image](https://github.com/user-attachments/assets/89e6f861-f26d-49af-b392-8c8cbcf23c7c) <br>
 - I tried reading some emails and checking the Maildir directory, but found nothing interesting. <br>
 ![image](https://github.com/user-attachments/assets/d2cd1fcc-0b09-496c-a99b-aa00fde42879) <br>
 - So, I listed hidden files and decided to check the Bash history. From there, I discovered that this machine runs MySQL and that the current user can log in to the MySQL server. Next, I checked the MySQL history and found a users database. Let's log in to MySQL and query the table to retrieve the password for the HTB user. <br>
 ![image](https://github.com/user-attachments/assets/afae2c17-df52-4167-b2c7-32a9bfd60929) <br>
 ![image](https://github.com/user-attachments/assets/05a1d20c-7f0d-4ad2-a3d9-083a5d8b99db) <br>
 - From here, use SQL query to retrieve the password.
 ![image](https://github.com/user-attachments/assets/6cc80a20-76e9-493a-bfb8-d7bbe04a1c3c) <br>









 



