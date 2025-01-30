import flet as ft

from utils import HashManager


class HashingPage:
    def __init__(self):
        self.text_field = ft.TextField(label="Введите текст", hint_text="Введите текст для вычисления хеша")
        self.file_picker = ft.FilePicker(on_result=self.handle_file_selection)
        self.file_picker_button = ft.ElevatedButton(
            text="Выбрать файл",
            on_click=lambda e: self.file_picker.pick_files()
        )
        self.hash_button = ft.ElevatedButton(
            text="Вычислить хеш",
            on_click=self.calculate_hash
        )
        self.result_sha256 = ft.TextField(
            label="SHA-256",
            hint_text="Здесь появится хеш SHA-256",
            read_only=True
        )
        self.result_sha512 = ft.TextField(
            label="SHA-512",
            hint_text="Здесь появится хеш SHA-512",
            read_only=True
        )
        self.result_label = ft.Text(value="", color=ft.colors.RED)

    def handle_file_selection(self, e: ft.FilePickerResultEvent):
        if e.files:
            print(f"Выбранный файл: {e.files[0].path}")

    def calculate_hash(self, e):
        data = None
        try:
            file = self.file_picker.result.files[0].path if self.file_picker.result.files else None
        except AttributeError:
            file = None

        if not file and not self.text_field.value:
            self.result_label.value = "Введите текст или выберите файл для хеширования!"
            self.result_label.color = ft.colors.RED
            self.result_label.update()
            return

        if file:
            try:
                with open(file, "rb") as file_read:
                    data = file_read.read()
            except Exception as ex:
                self.result_label.value = f"Ошибка чтения файла: {ex}"
                self.result_label.color = ft.colors.RED
                self.result_label.update()
                return
        elif self.text_field.value:
            data = self.text_field.value.encode()

        try:
            hash_response = HashManager.get_hashes(data)
            self.result_sha256.value = hash_response.sha256
            self.result_sha512.value = hash_response.sha512
            self.result_label.value = "Хеши успешно вычислены!"
            self.result_label.color = ft.colors.GREEN
        except Exception as ex:
            self.result_label.value = f"Ошибка хеширования: {ex}"
            self.result_label.color = ft.colors.RED

        self.result_sha256.update()
        self.result_sha512.update()
        self.result_label.update()

    def build(self):
        return ft.Column(
            [
                self.text_field,
                ft.Row([self.file_picker_button, self.file_picker]),
                self.hash_button,
                self.result_sha256,
                self.result_sha512,
                self.result_label
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        )