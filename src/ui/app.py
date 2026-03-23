from textual.app import App

from src.ui.screens import WelcomeScreen


class CasinoApp(App):
    """Casino Playground - main Textual application."""

    CSS_PATH = "styles.tcss"
    TITLE = "Casino Playground"

    def on_mount(self):
        self.push_screen(WelcomeScreen())
