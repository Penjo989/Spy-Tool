import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encrypter:
    def __init__(self):
        self.fernet = None

    def genKey(self, passPhrase, salt):
        passPhrase = passPhrase.encode()
        salt = salt.encode()
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(passPhrase))
        return key

    def setKey(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, strData):
        return self.fernet.encrypt(strData.encode()).decode()

    def decrypt(self, strData):
        try:
            return self.fernet.decrypt(strData.encode()).decode()
        except Exception as e:
            print(e)
            return None
