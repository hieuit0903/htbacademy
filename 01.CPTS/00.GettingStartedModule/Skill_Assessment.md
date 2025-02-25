# This is the easy box, just read the Nibble section carefully. I'll give you more hints about it
- Hints:
You need to edit hosts file.
Find a way to login to the web admin. Just try anything from view page-source, information in other directory, guessing, crack hash,...

# Ok! Let's go through the write up:
- First I try to information gathering about the target by scanning the service which running on the server <br>
  From the img below I found the website running on this machine. Let's take visit to the site.
![Image](https://github.com/user-attachments/assets/8e54a54e-6bb7-484b-a080-0cb224ba69e6)
![Image](https://github.com/user-attachments/assets/2dfe80f6-48b0-40c9-a10d-4943717c6302) <br />
  Something wrong with the website. Let's try to click somewhere to find more infor. I just found the domain link to this website. Try to map this to our hosts file
![Image](https://github.com/user-attachments/assets/e6680708-ec1e-4c88-ac34-8a3a874ba26c) <br>
  After mapping the domain to our hosts, let's try browsing it again. This time, we successfully access the website.
![Image](https://github.com/user-attachments/assets/024e1e65-42e2-499b-9146-4a9b747375d3)
- Now, it's time to find more informations about this site, I want to save my time so I've used ffuf for quick <br>
![Image](https://github.com/user-attachments/assets/a410f70b-c886-409a-937f-143ccd355d01) <br>
  I found some interesting directories. Now, let's take a look at them. If we visit /admin, it redirects us to the login page. I do not know anything about the username or password, so I decided to go back and check other directories for credentials. There was nothing special in the backups, plugins, or themes directories. But when we got to /data/users, we found admin credentials there
![Image](https://github.com/user-attachments/assets/ccc32c5d-3fb8-4fa1-b538-0d1152bf171a) <br>
  It seems that this is the admin login information, and the password has been hashed using the MD5 algorithm.
Using Hashcat or some online cracking tools, we cracked the MD5 hash. After that, we found that the username is 'admin' and the password is 'admin'. <br />
  Now. Let's login with the credential we just found.
![Image](https://github.com/user-attachments/assets/51a3f430-5b92-4db3-92bc-9208a84d7277) <br />
  After logging in, I remembered exploiting CMS platforms like this, similar to WordPress, by leaving a web shell in one of the PHP files of the themes. Now, I will locate that file and insert the web shell. <br />
![Image](https://github.com/user-attachments/assets/079eed70-bdb3-4e52-b031-49d0a8c3d7fd) <br />
  I found the location to insert the web shell. Next, I will choose a payload to get a reverse shell to my machine instead of executing it through the web
![Image](https://github.com/user-attachments/assets/001c1df2-cdde-4585-a6ab-6c4296c48889) <br />
  Similar to exploiting WordPress, we now set up a Netcat listener on the port we configured in the web shell. Then, we navigate to the location and execute the file where we inserted the web shell. <br />
![Image](https://github.com/user-attachments/assets/a266affa-bbb3-43a6-b54a-a8493f4405b7) <br />
  We got a shell! Now, let's spawn a PTY shell for better functionality and navigate to the home directory to retrieve the user flag.
![Image](https://github.com/user-attachments/assets/c52b31f8-c5d0-4ec1-abbc-03283a00cffc) <br />
  Now to get the root flag, We need to escalate privileges from the www-data user to root. The first and simplest step is to check sudo -l. We see that the www-data user can run /usr/bin/php with sudo privileges without requiring a password. Now, let's use GTFOBins to find an exploitation payload and escalate to root.
![Image](https://github.com/user-attachments/assets/95c9fed6-d2eb-49fc-a3c5-b428681bef7c) <br />
CMD="/bin/sh" → Sets CMD to /bin/sh, meaning the shell will be executed. And sudo php -r "system('$CMD');" → Runs a PHP one-liner that executes system('/bin/sh'), effectively spawning a shell with superuser privileges (if php is allowed via sudo).
Now, we got a root shell, just find and read the root flag.
