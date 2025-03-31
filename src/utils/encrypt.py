from cryptography.fernet import Fernet
from src.settings import FERRET_KEY


def encrypt_data(data: str) -> str:
    f = Fernet(FERRET_KEY)
    byte_data = data.encode()
    byte_encrypted_data = f.encrypt(data=byte_data)
    encrypted_data = byte_encrypted_data.decode()
    return encrypted_data


def decrypt_data(token: str) -> str:
    f = Fernet(FERRET_KEY)
    decrypted_byte_data = f.decrypt(token=token)
    decrypted_data = decrypted_byte_data.decode()
    return decrypted_data
