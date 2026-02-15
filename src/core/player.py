from .deck import Card


class Hand:
    def __init__(self):
        self.cards = []
        self.stood = False
        self.busted = False

    def add_card(self, card):
        self.cards.append(card)
        if self.get_value() > 21:
            self.busted = True

    def get_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                value += 11
            else:
                value += card.value
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21

    def is_soft(self):
        # has an ace counting as 11
        ...


class Player:
    def __init__(self, name, starting_chips=1000):
        self.name = name
        self.chips = starting_chips
        self.current_bet = 0
        self.hands = [Hand()]  # list for future split support
        self.is_sitting = True

    def place_bet(self, amount):
        self.chips -= amount
        self.current_bet = amount

    def win(self, multiplier=2):
        self.chips += self.current_bet * multiplier
        self.current_bet = 0

    def lose(self):
        self.current_bet = 0

    def push(self):
        self.chips += self.current_bet
        self.current_bet = 0

    def reset_hands(self):
        self.hands = [Hand()]
        self.current_bet = 0