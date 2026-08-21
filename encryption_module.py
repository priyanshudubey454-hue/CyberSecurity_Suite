from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

class EncryptionManager:
    def __init__(self):
        self.aes_key = b'0123456789012345'  # 16 bytes for AES
        self.des_key = b'01234567'          # 8 bytes for DES
        
        # Generate RSA keys
        self.rsa_key = RSA.generate(2048)
        self.rsa_public_key = self.rsa_key.publickey()
    
    def encrypt_aes(self, text):
        try:
            cipher = AES.new(self.aes_key, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
            return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def decrypt_aes(self, encrypted_text):
        try:
            raw = base64.b64decode(encrypted_text)
            iv = raw[:16]
            ct = raw[16:]
            cipher = AES.new(self.aes_key, AES.MODE_CBC, iv=iv)
            return unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def encrypt_des(self, text):
        try:
            cipher = DES.new(self.des_key, DES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), DES.block_size))
            return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def decrypt_des(self, encrypted_text):
        try:
            raw = base64.b64decode(encrypted_text)
            iv = raw[:8]
            ct = raw[8:]
            cipher = DES.new(self.des_key, DES.MODE_CBC, iv=iv)
            return unpad(cipher.decrypt(ct), DES.block_size).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"
    
    def encrypt_rsa(self, text):
        try:
            cipher = PKCS1_OAEP.new(self.rsa_public_key)
            ct_bytes = cipher.encrypt(text.encode('utf-8'))
            return base64.b64encode(ct_bytes).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)} (Try shorter text, RSA has size limit)"
    
    def decrypt_rsa(self, encrypted_text):
        try:
            raw = base64.b64decode(encrypted_text)
            cipher = PKCS1_OAEP.new(self.rsa_key)
            return cipher.decrypt(raw).decode('utf-8')
        except Exception as e:
            return f"Error: {str(e)}"