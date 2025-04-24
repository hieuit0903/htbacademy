# Hint: 
- Remember to create a custom password list like the example in this module and take a cup of coffee.
# Easy Lab:
- Proceed to perform an Nmap scan on the target machine to identify open ports and running services. <br>
![image](https://github.com/user-attachments/assets/d1e5dd1d-a332-4508-a6fc-e79003d74dee) <br>
- Found the open port information, proceed to brute force using the provided username and password list. Successfully brute-forced the FTP service with the correct username and password.<br>
![image](https://github.com/user-attachments/assets/61165499-944c-46a4-8fbd-da6f9b3808f5) <br>
- Logged in successfully as user mike. And found an id_rsa file that may be used for SSH access.<br>
![image](https://github.com/user-attachments/assets/46a66acd-b8e3-4b72-9b1a-9cbce5075ff5)
- Perform John the Ripper to crack this SSH key by first converting it to the correct format using ssh2john, then crack it using the rockyou wordlist. Then we will find the passphrase for the SSH key.<br>
![image](https://github.com/user-attachments/assets/56e51763-edba-4dbd-be32-10548217b3c8)
- Logged in to SSH as user mike using the SSH key.<br>
![image](https://github.com/user-attachments/assets/967ebccc-e4ca-4921-8f0e-0c522c4ff0e8) <br>
- Now, just look around and find the root password in some interesting files.<br>
![image](https://github.com/user-attachments/assets/61472775-ae03-4ea4-9c99-af94c55dd453)

# Medium Lab:
- Proceed to perform an Nmap scan on the target machine to identify open ports and running services. <br>
![image](https://github.com/user-attachments/assets/f9c25a60-55bb-4799-af9b-d7d49b4e4c0b) <br>
- Found an SMB service, so we will use CrackMapExec to brute-force the credentials quickly <br>
![image](https://github.com/user-attachments/assets/47f175d7-96ef-4815-9db9-f0ac40b8e4fe) <br>
- After finding the credentials for the SMB service, continue using CrackMapExec to list the shares available for this user.<br>
![image](https://github.com/user-attachments/assets/7b49b6a3-4bba-4149-badd-f788965f0e8f) <br>
- We found a password-protected zip file, so we need to convert it to the correct format for cracking by using zip2john. And we need to use a custom password list for this crack. Just use the example in this module.<br>
![image](https://github.com/user-attachments/assets/d4c8f8e4-7001-40ff-84f4-0fa4b828be9c) <br>
![image](https://github.com/user-attachments/assets/0b3f1dc7-2807-47e5-a38c-10f0e5ea4b05) <br>
- Found the password of this zip file, let's unzip it and find a document file that is password protected again. Let's crack it by using John the Ripper again. <br>
![image](https://github.com/user-attachments/assets/daf6b37b-6726-452e-aa4f-d3b76d1972ca) <br>
- Open the document and we found the root password for a server.<br>
![image](https://github.com/user-attachments/assets/6a332d49-5bf2-40b5-91ac-02128f551d2b) <br>
- So let's use these credentials to SSH into the server.<br>
![image](https://github.com/user-attachments/assets/c5769a3e-8842-47e1-a638-957550cdaf5c) <br>
- Nothing interesting in this server, but we found a local database running on this server.<br>
![image](https://github.com/user-attachments/assets/168787fe-0f8d-425b-b7ed-9b8498caefc1) <br>
- So let's try to log in to this local MySQL using the user "jason," but we cannot access it. Therefore, we need to find some default passwords for the MySQL server.<br>
![image](https://github.com/user-attachments/assets/df58978f-8c51-4e38-a98d-29b98a5ecb85) <br>
- After querying the database, we found the user "denis" along with his password. Now, let's log in as denis and enumerate his directory.<br>
![image](https://github.com/user-attachments/assets/0f66243b-7960-46f2-ab8f-6c309cc89113) <br>
- We can see the id_rsa key in Denis's directory. Let's download this file and use John the Ripper to crack the SSH key.<br>
![image](https://github.com/user-attachments/assets/e97dc2d0-2d82-4afa-92d7-b85a14e0a196) <br>
![image](https://github.com/user-attachments/assets/f4bf94b2-436f-473f-9251-001cd83e2084) <br>
- After finding the passphrase for this key, I wondered which user I needed to log in as. Not Denis, since I could already log into his account using the password. So, I decided to use this key with the root user and successfully logged in.<br>
![image](https://github.com/user-attachments/assets/a64e2bd0-0604-4736-9bdf-793bd59105b7) <br>

# Hard Lab:
- As a normal day, let's perform an nmap scan to gather information for the attack.<br>
![image](https://github.com/user-attachments/assets/64417dcc-4e0c-4fb1-950f-bfe7a54f0174) <br>
- We know that user Johanna is present on many hosts. So, let's brute-force her password to access RDP. <br>
![image](https://github.com/user-attachments/assets/404c2acd-60fb-406a-830a-1beec85fe36f) <br>
- After logging in as Johanna, I found a KeePass file. I need to download it and crack it to find some information.<br>
![image](https://github.com/user-attachments/assets/73b45092-92c6-4672-9443-a864251ca197) <br>
- Successfully cracked the KeePass file and found the credentials for David. Now, let's use runas with David's credentials to open a command prompt.<br>
![image](https://github.com/user-attachments/assets/52f0468d-63b7-4f6a-a2a7-91b44a4d0825) <br>
- In David's directory, we found a VHD file protected by BitLocker. To proceed, we need to crack the BitLocker protection to access the contents of the VHD file.<br>
![image](https://github.com/user-attachments/assets/3c05c9ff-9780-4dc3-a003-cd71bf0526ff) <br>
![image](https://github.com/user-attachments/assets/a2c32cf8-2c92-45e3-8b81-fb1567b71f10) <br>
- Next, we import the VHD to our machine. Since I'm using a Windows machine as my host, I just need to copy the VHD file from my VM to my host Windows machine and import it.<br>
![image](https://github.com/user-attachments/assets/6e6a9ecf-9461-4abb-a14e-8dcb840029c0)<br>
- We found the SAM and SYSTEM files. It's wonderful, right? Next, we use secretdump to dump the information.<br>
![image](https://github.com/user-attachments/assets/a05a7647-21b4-4a87-9077-e71b7c20b8bc) <br>
![image](https://github.com/user-attachments/assets/abb7d75c-e4a1-44b1-9cae-184346ab262d) <br>
- At this time, I'll use Hashcat to crack the NTML Hash.<br>
![image](https://github.com/user-attachments/assets/1f88ca5f-460f-41b9-9a75-cd6f128e9218) <br>
- Now, just RDP to the machine by using the Administrator credentials.
![image](https://github.com/user-attachments/assets/99a8fe45-63f4-4a70-a8b3-35922ce048fb)























