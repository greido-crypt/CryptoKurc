import flet as ft
import json
from utils import AESManager, RSAManager

class EncryptionPage:
    def __init__(self):
        self.text_field = ft.TextField(label="Текст для шифрования", hint_text="Введите текст для шифрования")

        self.password_field = ft.TextField(
            label="Пароль к выбранному ключу", hint_text="Введите пароль", password=True
        )

        self.file_picker = ft.FilePicker(on_result=self.handle_file_selection)
        self.file_picker_button = ft.ElevatedButton(
            text="Выбрать файл для кодировки",
            on_click=lambda e: self.file_picker.pick_files()
        )

        self.encryption_method = ft.Dropdown(
            label="Метод шифрования",
            options=[
                ft.dropdown.Option("AES"),
                ft.dropdown.Option("RSA")
            ],
            on_change=self.load_keys
        )

        self.keys_dropdown = ft.Dropdown(label="Доступные ключи", options=[])

        self.encrypt_button = ft.ElevatedButton(
            text="Начать шифрование",
            on_click=self.start_encryption
        )

        self.progress_bar = ft.ProgressBar(width=300, visible=False)

        self.result_label = ft.Text(value="", color=ft.colors.GREEN)

        self.encrypted_text = ft.TextField(
            label="Результат шифрования",
            hint_text="Здесь появится зашифрованный текст",
            multiline=True,
            read_only=True
        )

    def handle_file_selection(self, e: ft.FilePickerResultEvent):
        if e.files:
            print(f"Выбранный файл: {e.files[0].path}")


    def load_keys(self, e):
        method = self.encryption_method.value
        keys_file = "aes_keys.json" if method == "AES" else "rsa_keys.json"
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

    def start_encryption(self, e):
        self.progress_bar.visible = True
        self.progress_bar.update()

        text = self.text_field.value
        password = self.password_field.value

        try:
            file = self.file_picker.result.files[0].path if self.file_picker.result.files else None
        except AttributeError:
            file = None

        method = self.encryption_method.value
        key_name = self.keys_dropdown.value

        if not text and not file:
            self.result_label.value = "Введите текст или выберите файл для шифрования!"
            self.result_label.color = ft.colors.RED
        elif not password:
            self.result_label.value = "Введите пароль для шифрования!"
            self.result_label.color = ft.colors.RED
        elif not method:
            self.result_label.value = "Выберите метод шифрования!"
            self.result_label.color = ft.colors.RED
        elif not key_name:
            self.result_label.value = "Выберите ключ для шифрования!"
            self.result_label.color = ft.colors.RED
        else:
            try:
                if file:
                    with open(file, "rb") as file_read:
                        plain_bytes = file_read.read()
                else:
                    plain_bytes = text.encode()

                if method == "AES":
                    aes_manager = AESManager(key_name=key_name, password=password)
                    result = aes_manager.encrypt(plain_bytes)
                else:
                    rsa_manager = RSAManager(key_name=key_name, password=password)
                    result = rsa_manager.encrypt(plain_bytes)

                self.encrypted_text.value = result
                self.result_label.value = f"Данные успешно зашифрованы методом {method}!"
                self.result_label.color = ft.colors.GREEN

                if file:
                    encrypted_file_path = f"{file}.enc"
                    with open(encrypted_file_path, "wb") as file_write:
                        file_write.write(result.encode())
                    print(f"Зашифрованный файл сохранен как: {encrypted_file_path}")

            except Exception as ex:
                self.result_label.value = f"Ошибка шифрования: {ex}"
                self.result_label.color = ft.colors.RED

        self.progress_bar.visible = False
        self.progress_bar.update()
        self.result_label.update()
        self.encrypted_text.update()

    def build(self):
        return ft.Column(
            [
                self.text_field,
                ft.Row([self.file_picker_button, self.file_picker]),
                self.encryption_method,
                self.keys_dropdown,
                self.password_field,
                self.encrypt_button,
                self.progress_bar,
                self.result_label,
                self.encrypted_text
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
