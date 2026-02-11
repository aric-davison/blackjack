from textual.app import App, ComposeResult
from textual.screen import Screen, ModalScreen
from textual.containers import Center, Horizontal
from textual.widgets import Header, Footer, Button, Static
from textual.binding import Binding
from black_jack import create_deck, shuffle_deck, dealing_card, calculate_hand_value, check_winner
from card_widget import CardWidget

SUIT_SYMBOLS = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}


class BlackjackApp(App):
    CSS_PATH = "ui.tcss"
    BINDINGS = [
        Binding("enter", "start_game", "Start Game"),
        Binding("h", "hit", "Hit"),
        Binding("s", "stand", "Stand"),
        Binding("enter", "play_again", "Play Again"),
        Binding("escape", "exit", "Exit"),
                
    ]


    def on_mount(self):
        self.push_screen(WelcomeScreen())
        
class WelcomeScreen(Screen):
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Welcome to Blackjack!\n" \
        "Press \\[ENTER] to start the game.\n " \
        "The goal is to get as close to 21 as possible without going over.\n" \
        "Face cards are worth 10, and Aces can be worth 1 or 11.", id="welcome")
        with Center():
            yield Button("Start Game", id="start")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "start":
            self.app.push_screen(GameScreen())

class GameScreen(Screen):
    def __init__(self):
        super().__init__()
        self.deck = create_deck()
        shuffle_deck(self.deck)
        self.player_hand = [dealing_card(self.deck), dealing_card(self.deck)]
        self.dealer_hand = [dealing_card(self.deck), dealing_card(self.deck)]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Dealer's Hand:", id="dealer-label")
        yield Horizontal(id="dealer-cards")
        yield Static("", id="dealer-value")
        yield Static("Your Hand:", id="player-label")
        yield Horizontal(id="player-cards")
        yield Static("", id="player-value")
        with Center():
            with Horizontal():
                yield Button("Hit", id="hit")
                yield Button("Stand", id="stand")
        yield Footer()

    def on_mount(self):
        self.update_display()

    def make_card(self, card, face_up=True):
        rank, suit, _value = card
        return CardWidget(rank, SUIT_SYMBOLS[suit], face_up=face_up)

    def update_display(self, reveal_dealer=False):
        # Update dealer cards
        dealer_cards = self.query_one("#dealer-cards")
        dealer_cards.remove_children()
        for i, card in enumerate(self.dealer_hand):
            if i == 1 and not reveal_dealer:
                dealer_cards.mount(self.make_card(card, face_up=False))
            else:
                dealer_cards.mount(self.make_card(card))

        # Update dealer value
        if reveal_dealer:
            self.query_one("#dealer-value", Static).update(
                f"Value: {calculate_hand_value(self.dealer_hand)}"
            )
        else:
            visible = self.dealer_hand[:1]
            self.query_one("#dealer-value", Static).update(
                f"Value: {calculate_hand_value(visible)}"
            )

        # Update player cards
        player_cards = self.query_one("#player-cards")
        player_cards.remove_children()
        for card in self.player_hand:
            player_cards.mount(self.make_card(card))

        # Update player value
        self.query_one("#player-value", Static).update(
            f"Value: {calculate_hand_value(self.player_hand)}"
        )

    def end_game(self):
        result = check_winner(self.player_hand, self.dealer_hand)
        self.update_display(reveal_dealer=True)
        self.app.push_screen(ResultModal(result))

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "hit":
            self.player_hand.append(dealing_card(self.deck))
            self.update_display()
            if calculate_hand_value(self.player_hand) >= 21:
                self.end_game()
        elif event.button.id == "stand":
            while calculate_hand_value(self.dealer_hand) < 17:
                self.dealer_hand.append(dealing_card(self.deck))
            self.end_game()

class ResultModal(ModalScreen):
    def __init__(self, result: str):
        super().__init__()
        self.result = result

    def compose(self) -> ComposeResult:
        yield Static(self.result, id="result")
        with Center():
            with Horizontal():
                yield Button("Play Again", id="play-again")
                yield Button("Exit", id="exit")
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "play-again":
            self.app.pop_screen()  # Close the modal
            self.app.push_screen(GameScreen())  # Start a new game
        elif event.button.id == "exit":
            self.app.exit()  # Exit the application





if __name__ == "__main__":
    app = BlackjackApp()
    app.run()