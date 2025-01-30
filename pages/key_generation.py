import flet as ft
from utils import AESManager, RSAManager


class KeyGenerationPage:
    def __init__(self):
        self.key_name_field = ft.TextField(label="Название ключа", hint_text="Введите название ключа")
        self.key_password_field = ft.TextField(
            label="Пароль для ключа", hint_text="Введите пароль для ключа", password=True
        )
        self.generate_button = ft.ElevatedButton(
            icon=ft.Icons.KEY,
            text="Сгенерировать ключи",
            on_click=self.generate_keys
        )
        self.result_label = ft.Text(value="", color=ft.colors.GREEN)
        self.loading_indicator = ft.ProgressRing(visible=False)

    def generate_keys(self, e: ft.ControlEvent):
        self.loading_indicator.visible = True
        self.loading_indicator.update()

        key_name = self.key_name_field.value
        key_password = self.key_password_field.value

        if not key_name or not key_password:
            self.result_label.value = "Пожалуйста, заполните все поля!"
            self.result_label.color = ft.colors.RED
        else:
            try:
                aes = AESManager(key_name=key_name, password=key_password)
                aes.encrypt(b'123')
                rsa = RSAManager(key_name=key_name, password=key_password)
                rsa.encrypt(b'123')

                self.result_label.value = f"Ключ '{key_name}' успешно сгенерирован!"
                self.result_label.color = ft.colors.GREEN
                self.key_name_field.value = ""
                self.key_password_field.value = ""
            except Exception as ex:
                self.result_label.value = f"Ошибка генерации ключей: {ex}"
                self.result_label.color = ft.colors.RED

        self.loading_indicator.visible = False
        self.loading_indicator.update()
        self.result_label.update()
        self.key_name_field.update()
        self.key_password_field.update()

    def build(self):
        return ft.Column(
            [
                self.key_name_field,
                self.key_password_field,
                ft.Row(
                    [self.generate_button, self.loading_indicator],
                    alignment=ft.MainAxisAlignment.START,
                ),
                self.result_label,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )
