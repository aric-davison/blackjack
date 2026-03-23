from textual.screen import Screen, ModalScreen
from textual.containers import Center, Horizontal
from textual.widgets import Header, Footer, Button, Static
from textual.app import ComposeResult

from src.core.player import Player
from src.ui.card_widget import CardWidget
from src.games.blackjack.game import BlackjackGame

CARD_DELAY = 0.6


class BlackjackScreen(Screen):
    CSS_PATH = "styles.tcss"

    def __init__(self, player):
        super().__init__()
        self.player = player
        self.game = BlackjackGame()
        self.game.start_round(self.player)
        self._animating = False

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            f"Chips: {self.player.chips} | Bet: {self.player.current_bet}",
            id="chips-display",
        )
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
        return CardWidget(card.rank, card.suit_symbol, face_up=face_up)

    def _set_buttons_enabled(self, enabled):
        """Enable or disable the hit/stand buttons."""
        self.query_one("#hit", Button).disabled = not enabled
        self.query_one("#stand", Button).disabled = not enabled

    def update_display(self, reveal_dealer=False):
        # Dealer cards
        dealer_area = self.query_one("#dealer-cards")
        dealer_area.remove_children()
        for i, card in enumerate(self.game.dealer_hand.cards):
            if i == 1 and not reveal_dealer:
                dealer_area.mount(self.make_card(card, face_up=False))
            else:
                dealer_area.mount(self.make_card(card))

        # Dealer value
        if reveal_dealer:
            self.query_one("#dealer-value", Static).update(
                f"Value: {self.game.dealer_hand.get_value()}"
            )
        else:
            first_card_value = self.game.dealer_hand.cards[0].value
            self.query_one("#dealer-value", Static).update(
                f"Value: {first_card_value}"
            )

        # Player cards
        player_area = self.query_one("#player-cards")
        player_area.remove_children()
        for card in self.game.player_hand.cards:
            player_area.mount(self.make_card(card))

        # Player value
        self.query_one("#player-value", Static).update(
            f"Value: {self.game.player_hand.get_value()}"
        )

        # Chips
        self.query_one("#chips-display", Static).update(
            f"Chips: {self.player.chips} | Bet: {self.player.current_bet}"
        )

    def _animate_hit(self):
        """Animate a player hit: show card face-down, then flip after delay."""
        busted = self.game.player_hit()
        # Show the new card face-down first
        new_card = self.game.player_hand.cards[-1]
        player_area = self.query_one("#player-cards")
        face_down = self.make_card(new_card, face_up=False)
        player_area.mount(face_down)

        def reveal_card():
            # Replace face-down with face-up and update value
            self.update_display()
            if busted or self.game.player_hand.get_value() == 21:
                if not busted:
                    self.game.player_hand.stood = True
                self._animate_stand()
            else:
                self._animating = False
                self._set_buttons_enabled(True)

        self.set_timer(CARD_DELAY, reveal_card)

    def _animate_stand(self):
        """Animate the dealer's turn: reveal hole card, then draw cards one by one."""
        # Step 1: Reveal the hole card
        self.update_display(reveal_dealer=True)

        def dealer_draw_loop():
            if self.game.dealer_should_hit():
                # Deal one card face-down
                self.game.dealer_hit()
                dealer_area = self.query_one("#dealer-cards")
                new_card = self.game.dealer_hand.cards[-1]
                face_down = self.make_card(new_card, face_up=False)
                dealer_area.mount(face_down)

                def reveal_and_continue():
                    # Flip the card face-up
                    self.update_display(reveal_dealer=True)
                    # Schedule next draw
                    self.set_timer(CARD_DELAY, dealer_draw_loop)

                self.set_timer(CARD_DELAY, reveal_and_continue)
            else:
                # Dealer is done drawing — finish the round
                self.game.finish_round()
                self.update_display(reveal_dealer=True)
                # Brief pause before showing result
                self.set_timer(CARD_DELAY, self._show_result)

        # Pause after hole card reveal, then start dealer draws
        self.set_timer(CARD_DELAY, dealer_draw_loop)

    def _show_result(self):
        """Show the result modal and re-enable buttons."""
        self._animating = False
        self.app.push_screen(ResultModal(self.game.result, self.player))

    def end_game(self):
        self.update_display(reveal_dealer=True)
        self.app.push_screen(ResultModal(self.game.result, self.player))

    def on_button_pressed(self, event: Button.Pressed):
        if self._animating:
            return
        self._animating = True
        self._set_buttons_enabled(False)

        if event.button.id == "hit":
            self._animate_hit()
        elif event.button.id == "stand":
            self._animate_stand()


class ResultModal(ModalScreen):
    def __init__(self, result, player):
        super().__init__()
        self.result = result
        self.player = player

    def compose(self) -> ComposeResult:
        yield Static(self.result, id="result")
        yield Static(f"Chips: {self.player.chips}", id="result-chips")
        with Center():
            with Horizontal():
                yield Button("Play Again", id="play-again")
                yield Button("Back to Lobby", id="back-lobby")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "play-again":
            self.app.pop_screen()  # Close modal
            self.app.pop_screen()  # Close old BlackjackScreen
            self.app.push_screen(BlackjackScreen(self.player))
        elif event.button.id == "back-lobby":
            self.app.pop_screen()  # Close modal
            self.app.pop_screen()  # Back to lobby
