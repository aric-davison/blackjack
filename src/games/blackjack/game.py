from src.core.deck import Deck
from src.core.player import Hand, Player


class BlackjackGame:
    """Manages the state and rules for a single blackjack round."""

    def __init__(self, num_decks=6):
        self.deck = Deck(num_decks)
        self.player = None
        self.player_hand = None
        self.dealer_hand = Hand()
        self.game_over = False
        self.result = ""

    def start_round(self, player, bet=10):
        """Deal initial cards for a new round."""
        self.player = player
        self.player.reset_hands()
        self.player.place_bet(bet)
        self.player_hand = player.hands[0]
        self.dealer_hand = Hand()

        # Deal 2 cards each, alternating
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())
        self.player_hand.add_card(self.deck.deal())
        self.dealer_hand.add_card(self.deck.deal())

        self.game_over = False
        self.result = ""

    def player_hit(self):
        """Player draws one card. Returns True if player busted."""
        self.player_hand.add_card(self.deck.deal())
        if self.player_hand.busted:
            self.game_over = True
            self.result = self._determine_winner()
        return self.player_hand.busted

    def player_stand(self):
        """Player stands. Dealer plays, then determine winner."""
        self.player_hand.stood = True
        self._dealer_play()
        self.finish_round()

    def dealer_should_hit(self):
        """Check if dealer must draw another card."""
        return self.dealer_hand.get_value() < 17

    def dealer_hit(self):
        """Dealer draws one card. Returns the card dealt."""
        card = self.deck.deal()
        self.dealer_hand.add_card(card)
        return card

    def finish_round(self):
        """Determine winner and settle bets."""
        self.game_over = True
        self.result = self._determine_winner()

    def _dealer_play(self):
        """Dealer hits while hand value < 17."""
        while self.dealer_hand.get_value() < 17:
            self.dealer_hand.add_card(self.deck.deal())

    def _determine_winner(self):
        """Check winner and settle bets."""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()

        if self.player_hand.busted:
            self.player.lose()
            return "Dealer wins! Player busts."
        elif self.dealer_hand.busted:
            self.player.win()
            return "Player wins! Dealer busts."
        elif self.player_hand.is_blackjack() and not self.dealer_hand.is_blackjack():
            self.player.win(multiplier=2.5)
            return "Blackjack! Player wins!"
        elif player_value > dealer_value:
            self.player.win()
            return "Player wins!"
        elif dealer_value > player_value:
            self.player.lose()
            return "Dealer wins!"
        else:
            self.player.push()
            return "It's a tie! Push."

    @property
    def needs_new_deck(self):
        """Check if deck is running low."""
        return self.deck.remaining < 10
