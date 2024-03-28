from cryptography.fernet import Fernet
from django.conf import settings


class EncryptionClass:
    encryption_key = settings.ENCRYPTION_KEY
    cipher_suite = Fernet(encryption_key)

    @classmethod
    def encrypt_data(cls, data):
        encrypted_data = cls.cipher_suite.encrypt(data.encode())
        return encrypted_data

    @classmethod
    def decrypt_data(cls, encrypted_data):
        decrypted_data = cls.cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data
