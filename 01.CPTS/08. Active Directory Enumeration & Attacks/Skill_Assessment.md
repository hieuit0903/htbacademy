# Lab 1: 
# Hint: Remember! PtH is also a beautiful way.<br>
- In Skill #1, we were provided with a web shell to work with. <br>
<img width="975" height="448" alt="image" src="https://github.com/user-attachments/assets/db1623ba-19db-41f8-88d2-acdf69b03e7f" /> <br>
- Due to the limited capabilities of this web shell, I decided to use a Meterpreter shell instead.<br>
<img width="975" height="555" alt="image" src="https://github.com/user-attachments/assets/f9b11d02-e207-4ead-b290-3806cc9ed2f2" /> <br>
- We can use fping to discover other hosts in this local subnet. However, by looking at the DNS Server, I can initially guess that the Domain Controller is at IP 172.16.6.3. We could use nltest to confirm the IP of the DC, or continue scanning with tools like fping.<br>
<img width="819" height="294" alt="image" src="https://github.com/user-attachments/assets/0ccdabe2-8977-4490-94cd-6b1856047b49" /> <br>
- Exploit: Proceed to upload several tools such as Rubeus, PowerView, etc.
<img width="844" height="135" alt="image" src="https://github.com/user-attachments/assets/8ecaf1b9-4a66-4301-860e-3270f9444ae9" /> <br>
- Use Rubeus to perform Kerberoasting on the user svc_sql.<br>
<img width="975" height="658" alt="image" src="https://github.com/user-attachments/assets/db520a11-38a6-492b-82b0-2011f141bdc1" /> <br>
- Use Hashcat to crack the hash we just obtained; at this point, we successfully retrieve the plain-text password.<br>
<img width="975" height="501" alt="image" src="https://github.com/user-attachments/assets/65bd0a1d-0475-4ccc-ba38-5c29cdca5434" /> <br>
- With the information we've gathered, let's proceed to search for sensitive data to answer the questions. We'll remotely execute a PowerShell script block on MS01 since we already have the credentials for the user svc_sql.<br>
<img width="975" height="526" alt="image" src="https://github.com/user-attachments/assets/a74591ae-6088-4308-bac7-f19bf74a8a93" /> <br>
- For convenience, I’ll use proxychains in combination with the jump host, which is the Kali Linux machine, to run secretdump (note: in a real-world pentest scenario, this may vary). Using secretdump, I will extract the cached logon credentials from the target machine. Then, I’ll proceed to crack these password hashes using hashcat. And we will have a new user that is tpetty<br>
<img width="975" height="547" alt="image" src="https://github.com/user-attachments/assets/a76d770d-1dba-438d-b72d-dad6d3b2e794" /> <br>
- We will look for some interesting ACLs assigned to the user tpetty in the system — specifically, the DCSync rights. First, we need to convert this username into its corresponding SID.
<img width="975" height="377" alt="image" src="https://github.com/user-attachments/assets/81acac7f-d0ff-4acf-9b5c-a7c8be4e8005" /> <br>
- Since we have DCSync rights, we will use secretdump against the Domain Controller. At this point, we will retrieve the hash of the Administrator account on the DC.
<img width="975" height="233" alt="image" src="https://github.com/user-attachments/assets/e034c60b-bd77-4e67-9a37-03e252844a39" /> <br>
- Cracking the hash did not yield good results, so I decided to perform Pass-the-Hash with the Administrator user on the Domain Controller.
<img width="972" height="339" alt="image" src="https://github.com/user-attachments/assets/9f5ecc78-d08f-4e85-9521-2984c94eaf2a" /> <br>
- And now, we all done!

# Lab 2:
# Hint: Enumeration for initial access is very important!
- Initial enumeration using the LLMNR/NBT-NS poisoning technique allowed us to capture the hash of user AB920.<br>
<img width="975" height="297" alt="image" src="https://github.com/user-attachments/assets/a25401d4-24db-4ee7-b0e0-90c6cbfd8426" /> <br>
- Use Hashcat to crack the hash we just obtained; at this point, we successfully retrieve the plain-text password. <br>
<img width="975" height="405" alt="image" src="https://github.com/user-attachments/assets/f8530338-9cdc-4535-a391-4b5ec992574f" /> <br>
- Continue using fping to identify the alive hosts in this internal subnet, in which .240 is the IP address of our jump host.<br>
<img width="504" height="306" alt="image" src="https://github.com/user-attachments/assets/7746fd1f-17ae-43e0-b2af-7c7016bf716f" /> <br>
- Continuing the enumeration process, we will scan each IP to identify the exact services or NetBIOS Computer names associated with them, making the attack easier. Among them, the Domain Controller (DC) has the IP address 172.16.7.3.<br>
<img width="916" height="429" alt="image" src="https://github.com/user-attachments/assets/87c57890-887f-4d64-9fc9-65a80d76dcc7" /> <br>
- Using various methods to remotely access the MS01 machine, I decided to use Evil-WinRM to establish the connection.<br>
<img width="975" height="268" alt="image" src="https://github.com/user-attachments/assets/3d7abc78-a88d-4df4-bec8-a389684084f9" /> <br>
- The question asks us to find additional credentials for another user. From the jump host, we use crackmapexec to list the user accounts.<br>
<img width="975" height="439" alt="image" src="https://github.com/user-attachments/assets/3d6b63aa-3908-443b-b117-6ab365575584" /> <br>
- We proceed to extract only the samAccountName from the list of users.<br>
<img width="676" height="276" alt="image" src="https://github.com/user-attachments/assets/8d4349b9-59c1-41db-9e31-2fd0fa52e841" /> <br>
- Continue using crackmapexec to enumerate the password policy, which will be helpful for password spraying.<br>
<img width="972" height="404" alt="image" src="https://github.com/user-attachments/assets/8172181f-7706-4625-afbb-f6993c1d8dc6" /> <br>
- Proceed to spray a few basic passwords, and we successfully identify the next user: BR086.<br>
<img width="973" height="245" alt="image" src="https://github.com/user-attachments/assets/1bd07b86-5a48-401b-a023-9460011d3601" /> <br>
- Proceed to enumerate this user by checking what directory permissions they have.<br>
<img width="947" height="329" alt="image" src="https://github.com/user-attachments/assets/d76eaa11-8cd7-4942-85ca-31e052b652e9" /> <br>
- We've found a web.config file. Maybe something interested in there.<br>
<img width="642" height="106" alt="image" src="https://github.com/user-attachments/assets/cd2ba834-008c-414f-b6db-ea0a09f60fd2" /> <br>
- And yup! While reading the file, I found database credentials for the connection. <br>
<img width="891" height="538" alt="image" src="https://github.com/user-attachments/assets/519cace8-6469-4f33-9730-aa5270f32a3a" /> <br>
- During the initial Nmap scan, we discovered that host .60 has the MSSQL port open, so we'll use mssqlclient to access this database.<br>
<img width="959" height="316" alt="image" src="https://github.com/user-attachments/assets/24b24c01-cdb4-4d88-a814-18784610b6d6" /> <br>
- As shown in the database exploitation module, we proceed to enable xp_cmdshell and check the privileges of this user. We discover that the user has the SetImpersonatePrivilege right. <br>
<img width="816" height="539" alt="image" src="https://github.com/user-attachments/assets/352910c8-5fb7-40a9-9b96-d8b7bd84a1a4" /> <br>
- We can use Juicy Potato or PrintSpoofer to exploit this privilege escalation vulnerability. In this case, we'll proceed with PrintSpoofer64. First, upload the payload to the MSSQL server, and don’t forget to also upload Netcat (nc.exe) to facilitate the reverse shell connection during exploitation.<br>
<img width="975" height="285" alt="image" src="https://github.com/user-attachments/assets/311d116e-9fc1-47cf-9d9b-89da6a371cde" /> <br>
- We have enough tools for the exploit. Now, let's break the door. Open a listener and execute the command prompt as shown below.<br>
<img width="820" height="476" alt="image" src="https://github.com/user-attachments/assets/18ff58ad-709b-4c74-b16f-109397d92874" /> <br>
- Here we go. Got the shell! <br>
<img width="673" height="429" alt="image" src="https://github.com/user-attachments/assets/63a41ec8-845b-4a77-a808-edece8829985" /> <br>
- To speed up the enumeration process, I used Mimikatz on this server and obtained credentials for the user mssqlsvc. I tried cracking the password but it wasn’t effective, so we’ll proceed with a pass-the-hash attack using this account.<br>
<img width="795" height="426" alt="image" src="https://github.com/user-attachments/assets/0ca9dce2-dfbd-4705-ac20-1126e6aa6cca" /> <br>
- Performed a pass-the-hash attack on MS01 and successfully retrieved the Administrator flag from the MS01 machine.<br>
<img width="710" height="407" alt="image" src="https://github.com/user-attachments/assets/186c0ec4-018d-4f1c-9948-e2ed668f8929" /> <br>
<img width="788" height="159" alt="image" src="https://github.com/user-attachments/assets/25413ae7-9b95-419f-9346-d6aa3604edf9" /> <br>
- Back on MS01, we will look for domain admin users who have GenericAll permissions.<br>
<img width="967" height="357" alt="image" src="https://github.com/user-attachments/assets/5d3a4b21-4a46-41e0-95a6-17e1356d86a8" /> <br>
- We’ve obtained the user’s SID, now we just need to convert it into a readable format. And we got new a user: CT059 <br>
<img width="975" height="159" alt="image" src="https://github.com/user-attachments/assets/045b2cc5-bdf5-4686-a79a-e63fba1c15d9" /> <br>
- Let's go back to MS01. We will continue to use the LLMNR/NBT-NS Poisoning technique with Inveigh to capture the hash of user CT059.<br>
<img width="975" height="369" alt="image" src="https://github.com/user-attachments/assets/516990ea-812d-487d-9b73-cb42d53a1008" /> <br>
<img width="975" height="330" alt="image" src="https://github.com/user-attachments/assets/9f83501a-a303-4d3f-a7d9-5b65266ed92d" /> <br>
- Crack this NTLMv2 hash and we got a clear-text password.<br>
<img width="975" height="496" alt="image" src="https://github.com/user-attachments/assets/787e10b8-6b63-421f-97bc-5f708b28a6e0" /> <br>
- Since user CT059 is part of the Domain Admins group, it is highly likely that they have the privilege to reset passwords for other users. Therefore, I proceeded to reset the Administrator account’s password for quick access. (Note: In real-world scenarios or penetration testing environments, this approach is extremely risky. A safer and more professional method would be to create a new user and assign administrative privileges to that account, instead of directly modifying the Administrator or other active user accounts.) <br>
<img width="967" height="270" alt="image" src="https://github.com/user-attachments/assets/f6fc83de-5272-4cf2-89a3-6ad832779088" /> <br>
- After successfully changing the password, we can now simply log in to the Domain Controller using the Administrator account.<br>
<img width="729" height="509" alt="image" src="https://github.com/user-attachments/assets/2e4928a5-81a8-456e-9a91-0949ee9fcf35" /> <br>
- Since we already have the highest privileged user, dumping other hashes is no longer a challenge. It's now just a matter of choosing the right tool to perform the task.<br>
<img width="907" height="735" alt="image" src="https://github.com/user-attachments/assets/802f1293-1c5f-4fbe-b119-ce19db2fa3a6" /> <br>

































