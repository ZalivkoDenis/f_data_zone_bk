from __future__ import annotations

from pathlib import Path

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP

RSA_KEYS_BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY_PATH_PUBLIC: Path = RSA_KEYS_BASE_DIR / "rsa_public_local_secret.key"
SECRET_KEY_PATH_PRIVATE: Path = RSA_KEYS_BASE_DIR / "rsa_local_secret.key"

SECRET_KEY_PUBLIC: bytes = open(SECRET_KEY_PATH_PUBLIC, "rb").read()
SECRET_KEY_PRIVATE: bytes = open(SECRET_KEY_PATH_PRIVATE, "rb").read()


def encrypt_data(data: bytes) -> bytes:
    """
    Encrypt the data with the AES session key and the public RSA key.
    :param data: Байты для шифрования. Если шифруется строка, нужно передавать "Hello World!".encode()
    :return: Зашифрованная строка в байтах.
    """
    recipient_key = RSA.import_key(SECRET_KEY_PUBLIC)
    session_key = get_random_bytes(16)

    # Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    # Encrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, text_tag = cipher_aes.encrypt_and_digest(data)

    out_data = enc_session_key + cipher_aes.nonce + text_tag + ciphertext

    return out_data


def decrypt_data(data: bytes) -> bytes:
    """
    Decrypt encrypted data. Using PRIVATE RSA key!!!
    :param data: Зашифрованные байты
    :return: Расшифрованные байты. Если нужна строка, то необходимо выполнить result.decode()
    """
    private_key = RSA.import_key(SECRET_KEY_PRIVATE)

    psize = private_key.size_in_bytes()

    enc_session_key = data[:psize]
    nonce = data[psize : psize + 16]
    text_tag = data[psize + 16 : psize + 32]
    ciphertext = data[psize + 32 :]

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)

    # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    data = cipher_aes.decrypt_and_verify(ciphertext, text_tag)
    return data


if __name__ == "__main__":
    passwords = [
        "password",
        "qwerty",
        "123456",
        "123456789",
        "1234567890" * 14,
        "",
    ]

    edata: list[bytes] = []

    for _ in passwords:
        edata_item = encrypt_data(_.encode())
        print(f"{_} ({len(edata_item)}): {edata_item}")
        edata.append(edata_item)

    print()
    print("*" * 10, "DECODE", "*" * 10)
    print()

    for _ in edata:
        print(f"{decrypt_data(_).decode()}")
