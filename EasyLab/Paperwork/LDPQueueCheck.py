import socket

HOST = "<Target_IP"
PORT = 1515

s = socket.create_connection((HOST, PORT))

s.send(b"\x02archive_intake\n")

print(repr(s.recv(1024)))

s.close()
