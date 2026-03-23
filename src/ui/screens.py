from textual.screen import Screen
from textual.containers import Center, Vertical
from textual.widgets import Header, Footer, Button, Static
from textual.app import ComposeResult

from src.core.player import Player


class WelcomeScreen(Screen):
    """Splash screen shown on app startup."""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "Welcome to Casino Playground!\n\n"
            "A collection of card and casino games\n"
            "right in your terminal.",
            id="welcome",
        )
        with Center():
            yield Button("Enter Casino", id="enter")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "enter":
            self.app.pop_screen()
            self.app.push_screen(LobbyScreen())


class LobbyScreen(Screen):
    """Game selection lobby."""

    def __init__(self):
        super().__init__()
        self.player = Player("Player 1")

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Casino Lobby", id="lobby-title")
        yield Static(f"Chips: {self.player.chips}", id="lobby-chips")
        with Center():
            with Vertical():
                yield Button("Blackjack", id="blackjack")
                yield Button("Quit", id="quit")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "blackjack":
            from src.games.blackjack.screen import BlackjackScreen

            self.app.push_screen(BlackjackScreen(self.player))
        elif event.button.id == "quit":
            self.app.exit()

    def on_screen_resume(self):
        """Refresh chips display when returning from a game."""
        chips_label = self.query_one("#lobby-chips", Static)
        chips_label.update(f"Chips: {self.player.chips}")
