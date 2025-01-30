import json

import flet as ft

from utils import RSAManager, HashManager


class CheckSignaturesPage:
    def __init__(self):
        self.file_picker = ft.FilePicker(on_result=self.handle_file_selection)
        self.sign_file_picker = ft.FilePicker(on_result=self.handle_file_selection)

        self.password_field = ft.TextField(
            label="Пароль к выбранному ключу", hint_text="Введите пароль", password=True
        )

        self.file_picker_button = ft.ElevatedButton(
            text="Выбрать файл",
            on_click=lambda e: self.file_picker.pick_files()
        )

        self.sign_file_picker_button = ft.ElevatedButton(
            text="Выбрать подпись",
            on_click=lambda e: self.sign_file_picker.pick_files()
        )

        self.encryption_method = ft.Dropdown(
            label="Метод шифрования",
            options=[
                ft.dropdown.Option("RSA")
            ],
            on_change=self.load_keys
        )

        self.keys_dropdown = ft.Dropdown(label="Доступные ключи", options=[])

        self.progress_bar = ft.ProgressBar(width=300, visible=False)

        self.check_sign_button = ft.ElevatedButton(
            text="Проверить сертификат",
            on_click=self.create_signature
        )
        self.result_label = ft.Text(value="", color=ft.colors.RED)

    @staticmethod
    def handle_file_selection(e: ft.FilePickerResultEvent):
        if e.files:
            pass

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
        try:
            file = self.file_picker.result.files[0].path if self.file_picker.result.files else None
            sign_file = self.sign_file_picker.result.files[0].path if self.sign_file_picker.result else None

        except AttributeError:
            file = None
            sign_file = None

        password = self.password_field.value
        method = self.encryption_method.value
        key_name = self.keys_dropdown.value

        if not file:
            self.result_label.value = "Выберите файл для проверки сертификата!"
            self.result_label.color = ft.colors.RED
            self.result_label.update()
            self.progress_bar.visible = False
            self.progress_bar.update()
            return

        if not sign_file:
            self.result_label.value = "Выберите файл сертификата!"
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

        with open(file, "rb") as file_read:
            data = file_read.read()
            hash_values = HashManager().get_hashes(data=data)

        with open(sign_file, 'rb') as sign_file_read:
            data = sign_file_read.read()
            json_data = json.loads(data)

            encryptData: str = json_data['encryptData']
            algorithm: str = json_data['algorithm']

        rsa_manager = RSAManager(key_name=key_name, password=password)
        try:
            decrypt_hash = rsa_manager.decrypt(encryptData.encode())

            if algorithm == "SHA-256":
                hash_value = hash_values.sha256
                if hash_value == decrypt_hash:
                    self.result_label.value = 'Проверка подписи прошла успешно!'
                else:
                    self.result_label.value = 'Файл не соответствует подписи!'

            else:
                # SHA-512
                hash_value = hash_values.sha512
                if hash_value == decrypt_hash:
                    self.result_label.value = 'Проверка подписи прошла успешно!'
                else:
                    self.result_label.value = 'Файл не соответствует подписи!'

        except Exception as ex:
            self.result_label.value = f'Ошибка во время проверки подписи: {ex}'

        self.result_label.color = ft.colors.GREEN

        self.progress_bar.visible = False
        self.progress_bar.update()
        self.result_label.update()

    def build(self):
        return ft.Column(
            [
                self.encryption_method,
                self.keys_dropdown,
                self.password_field,
                ft.Row([self.file_picker_button,
                        self.file_picker,
                        self.sign_file_picker_button,
                        self.sign_file_picker]),
                self.check_sign_button,
                self.progress_bar,
                self.result_label
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
