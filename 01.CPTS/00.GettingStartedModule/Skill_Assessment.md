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
  After map the domain to our hosts. Let's try to browse it again. And we can success to access the website
![Image](https://github.com/user-attachments/assets/024e1e65-42e2-499b-9146-4a9b747375d3)
- Now, it's time to find more informations about this site, I want to save my time so I've used ffuf for quick <br>
![Image](https://github.com/user-attachments/assets/a410f70b-c886-409a-937f-143ccd355d01) <br>
  I found some interesting directories. Now, let's take a look at them. If we visit /admin, it redirects us to the login page. I do not know anything about the username or password, so I decided to go back and check other directories for credentials. There was nothing special in the backups, plugins, or themes directories. But when we got to /data/users, we found admin credentials there
![Image](https://github.com/user-attachments/assets/ccc32c5d-3fb8-4fa1-b538-0d1152bf171a) <br>
It seems that this is the admin login information, and the password has been hashed using the MD5 algorithm.
Using Hashcat or some online cracking tools, we cracked the MD5 hash. After that, we found that the username is 'admin' and the password is 'admin'.
