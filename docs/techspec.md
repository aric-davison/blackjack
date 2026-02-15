# Casino Playground - Technical Specification

## Overview

Refactor the existing Blackjack terminal game into a modular **Casino Playground** — a Textual TUI app that hosts multiple card/casino games from a single entry point. The core goal is to separate shared concerns (deck, cards, players, chips) from game-specific logic so new games can be added without duplicating infrastructure.

## Current State

```
blackjack/
├── black_jack.py      # Game logic + deck handling (coupled)
├── ui.py              # Textual app (welcome, game, result screens)
├── card_widget.py     # ASCII card rendering widget
├── ui.tcss            # Textual CSS
├── player.py          # Player/Hand classes (not integrated)
├── enviroment.yml     # Conda env
├── archive/
│   └── main.py        # Original CLI version
└── docs/
    └── Screenshot ...
```

### Problems to Solve

- Deck creation, shuffling, and dealing live in `black_jack.py` — these are generic and shouldn't be tied to one game.
- `player.py` has `Player` and `Hand` classes that aren't wired into the game yet.
- Cards are raw tuples `(rank, suit, value)` in the game logic but `card_widget.py` expects rank/suit strings — no shared card model.
- No single entry point; `ui.py` runs the app directly.
- Flat file structure won't scale to multiple games.

## Proposed Structure

```
blackjack/
├── main.py                  # Single entry point — runs the app
├── src/
│   ├── __init__.py
│   ├── core/                # Shared across all games
│   │   ├── __init__.py
│   │   ├── deck.py          # Card + Deck classes (create, shuffle, deal)
│   │   └── player.py        # Player class (name, chips, betting)
│   │
│   ├── ui/                  # Shared UI components
│   │   ├── __init__.py
│   │   ├── app.py           # Main CasinoApp, lobby/game selection
│   │   ├── card_widget.py   # ASCII card widget (from current)
│   │   ├── screens.py       # Shared screens (welcome, lobby)
│   │   └── styles.tcss      # Global styles
│   │
│   └── games/               # Each game is a self-contained module
│       ├── __init__.py
│       ├── blackjack/
│       │   ├── __init__.py
│       │   ├── game.py      # Blackjack rules, hand logic, win checks
│       │   ├── screen.py    # Blackjack game screen
│       │   └── styles.tcss  # Blackjack-specific styles (if needed)
│       └── ...              # Future games go here
│
├── tests/
│   ├── __init__.py
│   ├── test_deck.py
│   ├── test_player.py
│   └── test_blackjack.py
│
├── archive/                 # Previous versions, never deleted
│   ├── main.py              # Original CLI game
│   ├── black_jack.py        # Pre-refactor game logic
│   ├── ui.py                # Pre-refactor TUI
│   ├── card_widget.py       # Pre-refactor card widget
│   ├── player.py            # Pre-refactor player classes
│   └── ui.tcss              # Pre-refactor styles
│
├── docs/
│   ├── techspec.md          # This file
│   └── screenshots/
│
├── environment.yml
├── .gitignore
└── README.md
```

## Core Modules

### `src/core/deck.py` — Card + Deck

Card and Deck live in the same file since they're tightly coupled — a Deck is always a collection of Cards and you'd never import one without the other.

- `Card` class with `rank`, `suit`, `value` attributes
- Suit symbols mapping (Hearts -> ♥, etc.)
- `Deck` class wrapping a list of `Card` objects
- `create()` — build a standard 52-card deck
- `shuffle()` — randomize the deck in place
- `deal()` — pop and return a card
- `remaining` — cards left in the deck
- Support for multi-deck shoes (e.g., 6-deck for blackjack) via a `num_decks` parameter

### `src/core/player.py` — Player and Chips

Carried over from current `player.py` but updated to use `Card` objects.

- `Player` class: name, chips, current bet
- `Hand` class: list of `Card` objects, value calculation
- Betting methods: `place_bet()`, `win()`, `lose()`, `push()`
- Hand value calculation stays game-agnostic in the base class; games can override (e.g., blackjack ace logic)

## UI Modules

### `src/ui/app.py` — Main Application

- `CasinoApp(App)` — top-level Textual app
- Mounts the lobby screen on start
- Manages screen navigation between lobby and games

### `src/ui/screens.py` — Shared Screens

- `LobbyScreen` — game selection menu (Blackjack, and future games)
- `WelcomeScreen` — splash/intro

### `src/ui/card_widget.py` — Card Widget

Carried over from current `card_widget.py`, updated to accept `Card` objects.

## Game Modules

### `src/games/blackjack/`

- `game.py` — Blackjack-specific rules:
  - Hand value calculation with ace logic
  - Win/bust/push/blackjack detection
  - Dealer AI (hit on soft 17, etc.)
- `screen.py` — `BlackjackScreen(Screen)`:
  - Dealer and player card display
  - Hit/Stand buttons
  - Result modal
  - Betting UI

### Adding a New Game

1. Create `src/games/<game_name>/` with `game.py` and `screen.py`
2. Game logic imports `Card` and `Deck` from `src/core/deck`
3. Register the game in the lobby screen
4. Game-specific styles go in its own `styles.tcss`

## Migration Plan

This is the order of work for the refactor:

1. **Archive current code** — copy all current source files into `archive/`
2. **Create directory structure** — set up `src/`, `src/core/`, `src/ui/`, `src/games/blackjack/`, `tests/`
3. **Extract core modules** — pull deck/card logic out of `black_jack.py` into `src/core/deck.py`
4. **Integrate player module** — move and update `player.py` into `src/core/player.py`, wire `Hand` into the game
5. **Move UI components** — migrate `card_widget.py` and styles into `src/ui/`
6. **Build lobby** — create `CasinoApp` with a lobby screen and game selection
7. **Refactor blackjack** — move game logic into `src/games/blackjack/`, use core modules
8. **Create `main.py`** — single entry point at project root
9. **Add tests** — unit tests for core modules and blackjack logic
10. **Fix minor issues** — `.gitignore` typos, `environment.yml` filename

## Future Game Ideas

- Poker (Texas Hold'em or Five Card Draw)
- War
- Roulette
- Slots
- Baccarat

Each would follow the same pattern: game logic in `src/games/<name>/game.py`, screen in `screen.py`, shared card/deck/player infrastructure from `src/core/`.

## Tech Stack

- **Python 3.13**
- **Textual** — TUI framework
- **textual-dev** — development tools (console, devtools)
- **pytest** — testing
- **Conda** — environment management
