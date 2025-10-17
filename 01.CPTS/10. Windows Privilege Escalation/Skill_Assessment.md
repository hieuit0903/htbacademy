# Part 1:
- We have determined that this website has a command injection vulnerability. Now we will use msfvenom to create a Meterpreter payload to obtain a reverse shell.<br>
<img width="975" height="351" alt="image" src="https://github.com/user-attachments/assets/3bb89b57-0619-4907-8989-44259b198721" /> <br>
- This shell is quite restricted for downloading files using curl or wget, so I will use certutil to download the file. You can check the LOLBAS project to see how to use it (and I will also include the exploitation commands at the end of this write-up).<br>
<img width="975" height="249" alt="image" src="https://github.com/user-attachments/assets/f6ad0f54-60e8-47de-bf49-aa5e3f335bea" /> <br>
- After successfully uploading, proceed to use msfconsole to set up a handler to listen for connections (I may have overused Metasploit modules in previous write-ups, but that’s probably fine because I’m not a black-hat hacker — I’m just an ordinary penetration tester. I need to complete the job as quickly as possible and deliver final results to my client. What matters is understanding how these Metasploit modules operate).<br>
<img width="573" height="338" alt="image" src="https://github.com/user-attachments/assets/f4843729-1505-4c8e-b3d2-027951982cfa" /> <br>
- I successfully to get the meterpreter shell. <br>
<img width="975" height="568" alt="image" src="https://github.com/user-attachments/assets/67ca9648-4cf1-4017-80b4-b4cb5eda7077" /> <br>
- Proceed to check the hotfixes to answer the first question.<br>
<img width="975" height="163" alt="image" src="https://github.com/user-attachments/assets/85ad0ca1-d341-4640-af46-56d087cf0bf5" /> <br>
- After answering question 1, proceed to find a way to escalate privileges on this system. The first thing I usually do is check what privileges the user I have initial access as possesses. And boom — I obtained the ImpersonatePrivilege; I immediately thought of using JuicyPotato or PrintSpoof to try to exploit it for escalation and see if it works. <br>
<img width="975" height="413" alt="image" src="https://github.com/user-attachments/assets/cd547e74-24ab-4d68-8acb-5d769a4ca3d6" /> <br>
- After going through a series of steps — preparing the "weapons" (the exploit tools) — I uploaded them to the target machine and ran the exploit commands. Well, it failed and returned a COM error. At first I thought JuicyPotato couldn't exploit it, so I switched to PrintSpoofer, which also failed. I was pretty stuck at this point, so I re-read the exploitation section and Googled the error, and found that the socket was being closed unexpectedly or the COM connection failed → no DCOM service responded → the SYSTEM token was not returned. It’s possible this machine has already blocked/removed that COM, and when I searched further I found a list of CLSIDs for Windows Server 2016. I’ll need to brute-force all those CLSIDs to find which COM object works.<br>
<img width="975" height="107" alt="image" src="https://github.com/user-attachments/assets/df432ed2-79f1-4dc3-ac5f-ee02b3133cba" /> <br>
- I downloaded the CLSDI.list file (I put the link below). I wrote a PowerShell script to brute-force the entire list. There was another problem: the list is quite long, and running it (or using the author's provided .bat script) could cause this Meterpreter shell to die, so I reluctantly split the CLSID list into multiple files to run them separately. Near the last file I ran, I found a CLSID that worked. (if it succeeds it will return NT AUTHORITY\SYSTEM.)<br>
<img width="657" height="288" alt="image" src="https://github.com/user-attachments/assets/3c2f4547-c50d-4d35-9875-4dba3489aa6c" /> <br>
<img width="498" height="110" alt="image" src="https://github.com/user-attachments/assets/2b3e5585-acaf-4027-aafd-3d03cb9794a4" /> <br>
- Now, I run the exploit with this CLSID, and finaly got the NT Authority\system shell <br>
<img width="975" height="181" alt="image" src="https://github.com/user-attachments/assets/9b0b8955-215c-4838-8e90-09f3b11ff516" /> <br>
- Now, just answer the questions, using the admin rights to find the keyword is easier than using normal rights :v <br>
<img width="975" height="272" alt="image" src="https://github.com/user-attachments/assets/8b4185f1-2147-4ded-b3d3-a6cdce9a05c3" /> <br>
<img width="970" height="582" alt="image" src="https://github.com/user-attachments/assets/d759eaa5-b11b-44d2-af4c-4c6d2a7bed67" /> <br>

**Ref:** maybe you will learn more things about the COM problems. <br>
[1] https://forum.hackthebox.com/t/academy-windows-privilege-escalation-skills-assessment-part-i/243540/82 <br>
[2] https://forum.hackthebox.com/t/juicypotato-shield-com-recv-failed-with-error-10038/2991/7 <br>
[3] https://raw.githubusercontent.com/ohpe/juicy-potato/refs/heads/master/CLSID/Windows_Server_2016_Standard/CLSID.list <br>

# Part 2:
- I used various techniques to search — because the keyword was too noisy I employed almost every method in this module — and when I reached unattend.xml I discovered that this file exists.<br>
<img width="798" height="270" alt="image" src="https://github.com/user-attachments/assets/32a0c272-e17e-48e6-a087-59a23cca47b7" /> <br>
- Read the file and I found the password. <br>
<img width="547" height="388" alt="image" src="https://github.com/user-attachments/assets/84f73ac3-2e7c-4a9d-ae1a-b13eca1ac42e" /> <br>
- At the privilege escalation step. As usual, the first thing I do is check the user's permissions — something looked familiar, but there wasn't anything immediately useful to exploit. <br>
<img width="723" height="234" alt="image" src="https://github.com/user-attachments/assets/3ea502d3-67c0-4217-9609-313db339f50a" /> <br>
- Now I checked the hotfix of this machine, and give it to GPT, and this machie got the the vuln related to CVE-2020-0668.<br>
<img width="832" height="345" alt="image" src="https://github.com/user-attachments/assets/43328078-b915-4745-a80b-a61ba11fb2b7" /> <br>
- Check winver to confirm — this means the CVE might be exploitable, but we need to find a service with misconfigured permissions. <br>
<img width="492" height="195" alt="image" src="https://github.com/user-attachments/assets/b43b5bb4-ab33-4e72-9c0f-ed44d0fa63df" /> <br>
 - And....I think you guys will know it, just a exploit step in the section.<br>
 <img width="897" height="345" alt="image" src="https://github.com/user-attachments/assets/5b647ca6-a8ac-4ab8-8188-c9bc3f695c98" /> <br>
- Similar to the guide of this section, I created a payload using msfvenom and downloaded it to the target machine.<br>
<img width="975" height="104" alt="image" src="https://github.com/user-attachments/assets/7887272b-1a19-47c9-91bf-ec4a442686a0" /> <br>
- Now for the exploit compilation phase — based on the Git link that HTB provided, proceed to compile this exploit.
- First, you need to framework version of this source.
<img width="732" height="142" alt="image" src="https://github.com/user-attachments/assets/5063ab16-03bd-4006-a3ce-4e503d84c372" /> <br>
- I'll use Mono to compile it, because the version is 4.x, and I'm using Linux attackbox.<br>
<img width="975" height="227" alt="image" src="https://github.com/user-attachments/assets/88a52270-6315-4bdf-b780-a662c1c5f43a" /> <br>
- After install the Mono, proceed to compile the source.<br>
<img width="975" height="434" alt="image" src="https://github.com/user-attachments/assets/42328091-aeaf-49dd-8969-ea458451feb7" /> <br>
- I got 4 files after compile successfully and I uploaded these file to the target machine. <br>
<img width="975" height="117" alt="image" src="https://github.com/user-attachments/assets/86a9b26f-a19f-445f-8f66-847dc961163d" /> <br>
- Exploit the machine...<br>
<img width="975" height="282" alt="image" src="https://github.com/user-attachments/assets/fa11f020-a309-4084-9197-f40c8fe9398d" /> <br>
- So, check the permission of the maintenance.exe. You must have full permission of the current user. <br>
<img width="975" height="152" alt="image" src="https://github.com/user-attachments/assets/b9684b61-246e-40aa-9f28-4ab88545db33" /> <br>
- Then restart this service and use Metasploit's handler module to obtain a shell (Metasploit again :v).<br>
<img width="975" height="199" alt="image" src="https://github.com/user-attachments/assets/aece16e5-5420-4790-891e-e48ded48495a" /> <br>
- One thing is this shell is very prone to losing connection — I don’t know why, maybe I did something wrong — so I created an additional reverse_tcp payload and uploaded it to the target machine. As soon as I obtained a Meterpreter shell from the CVE exploit, I used execute -f to run the payload I created in order to get a more persistent shell (this approach is a bit roundabout but I think it will work).<br>
<img width="975" height="282" alt="image" src="https://github.com/user-attachments/assets/838b22dd-74bb-4ba6-b8f9-6bfec72fc29d" /> <br>
- To be quick I used hashdump to grab the entire SAM (you can reg save it and use secretdump to extract). <br>
<img width="975" height="248" alt="image" src="https://github.com/user-attachments/assets/eadca69f-26b2-436d-b3c8-c3338488bbdc" /> <br>
- I discovered the user mentioned in the question had been disabled. I pulled the hash and used Hashcat to crack it, and obtained the cleartext password.<br>
<img width="801" height="342" alt="image" src="https://github.com/user-attachments/assets/2d13be7e-98ea-42a7-9a99-f2c57c761571" /> <br>
- **Bonus**: After finishing I suddenly realized (actually from reading Medium — I tend to read other people's write-ups after I finish a box to see if I can learn anything new and to see how they explain it), there is an easier privilege escalation method using Always Install Elevated settings. OK, you can practice that part yourselves.<br>
<img width="882" height="273" alt="image" src="https://github.com/user-attachments/assets/f1b7220b-6bce-4fa4-b8d9-d85a4d92f622" /> <br>



















