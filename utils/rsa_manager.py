import base64
import json
import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from .aes_manager import AESManager


class RSAManager:
    def __init__(self,
                 key_name: str,
                 password: str):
        self.__key_name = key_name
        self.__aes_manager = AESManager(key_name=key_name, password=password)

    @staticmethod
    def __generate_key_pair() -> RsaKey:
        private_key = RSA.generate(2048)

        return private_key

    def __get_private_key(self):
        try:
            private_key = self.__load_private_key()
        except FileNotFoundError:
            private_key = self.__generate_key_pair()
            # self.__save_public_key()
            self.__save_private_key(private_key.export_key())

        return private_key

    def encrypt(self, plain_bytes: bytes) -> str:
        private_key = self.__get_private_key()
        public_key = self.public_key()
        cipher = PKCS1_OAEP.new(public_key)
        ciphertext = cipher.encrypt(plain_bytes)
        return base64.b64encode(ciphertext).decode(errors='ignore')

    def decrypt(self, encrypted_data: bytes) -> str:
        private_key = self.__get_private_key()
        cipher = PKCS1_OAEP.new(private_key)
        ciphertext = base64.b64decode(encrypted_data)
        return cipher.decrypt(ciphertext).decode(errors='ignore')

    def __save_private_key(self, private_key: bytes):
        encrypted_key = self.__aes_manager.encrypt(plain_bytes=private_key)
        file_path = "rsa_keys.json"

        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = {}
        else:
            data = {}

        data[self.__key_name] = encrypted_key

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def __save_public_key(self):
        public_key = self.public_key().export_key()
        public_key_file_path = f"{self.__key_name}.pem"
        with open(public_key_file_path, "wb") as public_key_file:
            public_key_file.write(public_key)

    def __load_private_key(self) -> RSA.RsaKey:
        file_path = "rsa_keys.json"

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден.")

        with open(file_path, "r") as file:
            data = json.load(file)
            if self.__key_name in data:
                encrypted_key: str = data[self.__key_name]
                decrypted_key = self.__aes_manager.decrypt(encrypted_key.encode())
                return RSA.import_key(decrypted_key)
            else:
                raise FileNotFoundError("Приватный ключ с указанным именем не найден.")

    def public_key(self) -> RSA.RsaKey:
        private_key = self.__get_private_key()
        return private_key.public_key()
