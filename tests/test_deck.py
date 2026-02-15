# testing for deck.py
import pytest
from src.core.deck import Deck

def test_deck_creation():
    deck = Deck()
    assert len(deck.cards) == 52