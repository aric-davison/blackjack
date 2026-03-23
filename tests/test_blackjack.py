import pytest
from src.core.player import Player
from src.games.blackjack.game import BlackjackGame


def test_start_round_deals_four_cards():
    game = BlackjackGame()
    player = Player("Test")
    game.start_round(player)
    assert len(game.player_hand.cards) == 2
    assert len(game.dealer_hand.cards) == 2


def test_player_hit_adds_card():
    game = BlackjackGame()
    player = Player("Test")
    game.start_round(player)
    game.player_hit()
    assert len(game.player_hand.cards) == 3


def test_player_stand_triggers_dealer():
    game = BlackjackGame()
    player = Player("Test")
    game.start_round(player)
    game.player_stand()
    assert game.game_over
    assert game.dealer_hand.get_value() >= 17 or game.dealer_hand.busted


def test_game_result_not_empty_after_stand():
    game = BlackjackGame()
    player = Player("Test")
    game.start_round(player)
    game.player_stand()
    assert game.result != ""


def test_chips_change_after_round():
    game = BlackjackGame()
    player = Player("Test", starting_chips=1000)
    game.start_round(player, bet=100)
    assert player.chips == 900  # bet deducted
    game.player_stand()
    # Chips should have changed (win, lose, or push)
    assert player.current_bet == 0


def test_needs_new_deck():
    game = BlackjackGame(num_decks=1)
    # Deal down to exactly 10 remaining (52 - 42 = 10)
    for _ in range(42):
        game.deck.deal()
    assert not game.needs_new_deck  # 10 remaining
    game.deck.deal()
    assert game.needs_new_deck  # 9 remaining (< 10)
