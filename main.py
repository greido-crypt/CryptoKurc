import flet as ft

from models import NavigationBar


async def main(page: ft.Page):
    page.title = "Crypto App"
    page.window.resizable = True
    page.theme_mode = ft.ThemeMode.DARK

    mainContainer = ft.Container()

    page.navigation_bar = NavigationBar(page=page, container=mainContainer).build()

    page.add(mainContainer)

if __name__ == "__main__":
    ft.app(target=main,
           assets_dir='assets',
           port=1337)
