# deck class
import random

class Deck:
    def __init__(self, num_of_decks=1):
        self.cards = self.create_deck(num_of_decks)

    def create_deck(self, num_of_decks=1):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11
        }
        single = [(rank, suit, value) for suit in suits for rank, value in ranks.items()]
        decks = single * num_of_decks
        random.shuffle(decks)
        return decks

    def deal_card(self):
        return self.cards.pop()
