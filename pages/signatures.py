import json

import flet as ft

from utils import RSAManager, HashManager


class SignaturesPage:
    def __init__(self):
        self.file_picker = ft.FilePicker(on_result=self.handle_file_selection)

        self.password_field = ft.TextField(
            label="Пароль к выбранному ключу", hint_text="Введите пароль", password=True
        )

        self.file_picker_button = ft.ElevatedButton(
            text="Выбрать файл",
            on_click=lambda e: self.file_picker.pick_files()
        )

        self.encryption_method = ft.Dropdown(
            label="Метод шифрования",
            options=[
                ft.dropdown.Option("RSA")
            ],
            on_change=self.load_keys
        )

        self.algorithm_dropdown = ft.Dropdown(
            label="Выберите алгоритм",
            options=[
                ft.dropdown.Option("SHA-256"),
                ft.dropdown.Option("SHA-512")
            ],
            value="SHA-256"
        )

        self.keys_dropdown = ft.Dropdown(label="Доступные ключи", options=[])

        self.progress_bar = ft.ProgressBar(width=300, visible=False)

        self.sign_button = ft.ElevatedButton(
            text="Создать сертификат",
            on_click=self.create_signature
        )
        self.result_label = ft.Text(value="", color=ft.colors.RED)

    @staticmethod
    def handle_file_selection(e: ft.FilePickerResultEvent):
        if e.files:
            print(f"Выбранный файл: {e.files[0].path}")

    def load_keys(self, e):
        keys_file = "rsa_keys.json"
        try:
            with open(keys_file, "r") as file:
                keys = json.load(file)
                self.keys_dropdown.options = [ft.dropdown.Option(key) for key in keys]
        except FileNotFoundError:
            self.keys_dropdown.options = []
            self.result_label.value = f"Файл {keys_file} не найден!"
            self.result_label.color = ft.colors.RED
        except Exception as ex:
            self.keys_dropdown.options = []
            self.result_label.value = f"Ошибка загрузки ключей: {ex}"
            self.result_label.color = ft.colors.RED
        self.keys_dropdown.update()
        self.result_label.update()

    def create_signature(self, e: ft.ControlEvent):

        self.progress_bar.visible = True
        file = self.file_picker.result.files[0].path if self.file_picker.result else None
        password = self.password_field.value
        method = self.encryption_method.value
        key_name = self.keys_dropdown.value
        algorithm = self.algorithm_dropdown.value

        if not file:
            self.result_label.value = "Выберите файл для создания сертификата!"
            self.result_label.color = ft.colors.RED
            self.result_label.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            return

        if not password:
            self.result_label.value = "Введите пароль для выбранного ключа!"
            self.result_label.color = ft.colors.RED
            self.result_label.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            return

        if not method:
            self.result_label.value = "Выберите метод шифрования!"
            self.result_label.color = ft.colors.RED
            self.result_label.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            return

        if not key_name:
            self.result_label.value = "Выберите ключ для шифрования!"
            self.result_label.color = ft.colors.RED
            self.result_label.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            return

        try:
            with open(file, "rb") as file_read:
                data = file_read.read()
                rsa_manager = RSAManager(key_name=key_name, password=password)
                public_key = rsa_manager.public_key().export_key().decode()
                hash_values = HashManager().get_hashes(data=data)

                if algorithm == "SHA-256":
                    encryptData = rsa_manager.encrypt(plain_bytes=hash_values.sha256.encode())
                    resultData = {
                        "encryptData": encryptData,
                        "algorithm": algorithm,
                    }
                    result_data = json.dumps(resultData)

                elif algorithm == "SHA-512":
                    encryptData = rsa_manager.encrypt(plain_bytes=hash_values.sha512.encode())
                    resultData = {
                        "encryptData": encryptData,
                        "algorithm": algorithm,
                    }
                    result_data = json.dumps(resultData)

            sig_file_path = f"{file}.sig"
            with open(sig_file_path, "w") as sig_file:
                sig_file.write(result_data)

            public_key_file_path = f"{file}.pem"
            with open(public_key_file_path, "w") as public_key_file:
                public_key_file.write(public_key)

            self.result_label.value = (f"Сертификат создан ({algorithm}): {sig_file_path}\n"
                                       f"Экспортирован публичный ключ: {public_key_file_path}")
            self.result_label.color = ft.colors.GREEN

        except Exception as ex:
            self.result_label.value = f"Ошибка создания сертификата: {ex}"
            self.result_label.color = ft.colors.RED

        self.progress_bar.visible = False
        self.progress_bar.update()
        self.result_label.update()

    def build(self):
        return ft.Column(
            [
                self.encryption_method,
                self.keys_dropdown,
                self.password_field,
                ft.Row([self.file_picker_button, self.file_picker]),
                self.algorithm_dropdown,
                self.sign_button,
                self.progress_bar,
                self.result_label
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
