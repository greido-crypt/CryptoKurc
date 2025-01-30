import flet as ft

from pages import KeyGenerationPage, EncryptionPage, DecryptionPage, HashingPage, SignaturesPage, CheckSignaturesPage


class NavigationBar:
    def __init__(self, page: ft.Page, container: ft.Container):
        self.__page = page
        self.__container = container
        self.__navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.KEY, label="Генерация ключей"),
                ft.NavigationBarDestination(icon=ft.Icons.LOCK, label="Шифрование"),
                ft.NavigationBarDestination(icon=ft.Icons.LOCK_OPEN, label="Расшифровка"),
                ft.NavigationBarDestination(icon=ft.Icons.FINGERPRINT, label="Хэширование"),
                ft.NavigationBarDestination(icon=ft.Icons.VERIFIED, label="Сделать подпись"),
                ft.NavigationBarDestination(icon=ft.Icons.VERIFIED_USER, label="Проверить подпись"),
            ],
            on_change=lambda e: self.change_navigation(e)
        )

    def change_navigation(self, e: ft.ControlEvent):
        if e.data == "0":
            # self.__page.go('/key-generation')
            controls = KeyGenerationPage().build()
            self.__page.remove(*self.__page.controls)
            self.__page.add(controls)

        elif e.data == "1":
            # self.__page.go('/encryption')
            controls = EncryptionPage().build()
            self.__page.remove(*self.__page.controls)
            self.__page.add(controls)

        elif e.data == "2":
            # self.__page.go('/decryption')
            controls = DecryptionPage().build()
            self.__page.remove(*self.__page.controls)
            self.__page.add(controls)

        elif e.data == "3":
            # self.__page.go('/hashing')
            controls = HashingPage().build()
            self.__page.remove(*self.__page.controls)
            self.__page.add(controls)

        elif e.data == "4":
            # self.__page.go('/signatures')
            controls = SignaturesPage().build()
            self.__page.remove(*self.__page.controls)
            self.__page.add(controls)

        elif e.data == "5":
            # self.__page.go('/signatures')
            controls = CheckSignaturesPage().build()
            self.__page.remove(*self.__page.controls)
            self.__page.add(controls)

        self.__page.update()

    def build(self):
        return self.__navigation_bar
