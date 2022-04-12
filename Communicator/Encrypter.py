import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encrypter:
    def genKey(self, passPhrase, salt):
        passPhrase = passPhrase.encode()
        salt = salt.encode()  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(passPhrase))  # Can only use kdf once
        return key

    def decrypt(self, strData, key):
        try:
            fernet = Fernet(key)
            return fernet.decrypt(strData.encode()).decode()
        except Exception as e:
            return None

    def encrypt(self, strData, key):
        try:
            fernet = Fernet(key)
            return fernet.encrypt(strData.encode()).decode()
        except Exception as e:
            print(e)
            return strData