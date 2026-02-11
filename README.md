# Casino Playground

A terminal-based casino game suite built with Python and [Textual](https://textual.textualize.io/). Play Blackjack (and eventually more games) right in your terminal with full ASCII card rendering.

## Current Status

**Early development** — Blackjack is playable with a TUI. The project is being restructured from a single-game app into a modular casino platform. See [techspec.md](techspec.md) for the full architecture plan.

### What Works

- Blackjack game with hit/stand
- ASCII card rendering with suit pip layouts
- Face-down card display for dealer's hole card
- Red/black card coloring
- Welcome screen, game screen, result modal

### What's Next

- Separate shared card/deck logic from game-specific code
- Integrate player chips and betting
- Lobby screen for game selection
- Additional games (Poker, War, etc.)
- Tests

## Setup

### Prerequisites

- Python 3.13
- Conda (recommended) or pip

### Install

```bash
# Clone the repo
git clone <repo-url>
cd blackjack

# Create conda environment
conda env create -f environment.yml
conda activate jackenv
```

### Run

```bash
python main.py
```

> **Note:** During the refactor, the entry point is moving to `main.py` at the project root. Currently the app runs via `python ui.py`.

## Project Structure

```
├── main.py              # Entry point (planned)
├── src/
│   ├── core/            # Shared: cards, deck, player/chips
│   ├── ui/              # Shared: app shell, card widget, lobby
│   └── games/
│       └── blackjack/   # Blackjack game logic + screen
├── tests/
├── archive/             # Previous versions of code
├── docs/
├── techspec.md
└── environment.yml
```

See [techspec.md](techspec.md) for detailed architecture documentation.

## Tech Stack

- **Python 3.13**
- **Textual** — terminal UI framework
- **pytest** — testing

## Controls

| Key / Button | Action     |
|-------------|------------|
| Hit         | Draw a card |
| Stand       | End your turn |
| Play Again  | Start a new hand |
| Exit / Esc  | Quit the game |
