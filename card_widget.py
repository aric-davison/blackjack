from textual.widgets import Static


class CardWidget(Static):
    """Full-size 9-line ASCII playing card with pip layouts."""

    # Each card has 5 rows of 3 slots (left, mid, right) = 15 slots max
    # "X" = show suit symbol, " " = blank
    PIPS = {
        "A":  [[" ", " ", " "],
               [" ", " ", " "],
               [" ", "X", " "],
               [" ", " ", " "],
               [" ", " ", " "]],
        "2":  [[" ", "X", " "],
               [" ", " ", " "],
               [" ", " ", " "],
               [" ", " ", " "],
               [" ", "X", " "]],
        "3":  [[" ", "X", " "],
               [" ", " ", " "],
               [" ", "X", " "],
               [" ", " ", " "],
               [" ", "X", " "]],
        "4":  [["X", " ", "X"],
               [" ", " ", " "],
               [" ", " ", " "],
               [" ", " ", " "],
               ["X", " ", "X"]],
        "5":  [["X", " ", "X"],
               [" ", " ", " "],
               [" ", "X", " "],
               [" ", " ", " "],
               ["X", " ", "X"]],
        "6":  [["X", " ", "X"],
               [" ", " ", " "],
               ["X", " ", "X"],
               [" ", " ", " "],
               ["X", " ", "X"]],
        "7":  [["X", " ", "X"],
               [" ", "X", " "],
               ["X", " ", "X"],
               [" ", " ", " "],
               ["X", " ", "X"]],
        "8":  [["X", " ", "X"],
               [" ", "X", " "],
               ["X", " ", "X"],
               [" ", "X", " "],
               ["X", " ", "X"]],
        "9":  [["X", " ", "X"],
               ["X", "X", "X"],
               [" ", " ", " "],
               ["X", "X", "X"],
               [" ", "X", " "]],
        "10": [["X", " ", "X"],
               ["X", "X", "X"],
               [" ", "X", " "],
               ["X", "X", "X"],
               ["X", " ", "X"]],
        "J":  [[" ", " ", " "],
               [" ", " ", " "],
               [" ", "♛", " "],
               [" ", " ", " "],
               [" ", " ", " "]],
        "Q":  [[" ", " ", " "],
               [" ", " ", " "],
               [" ", "♛", " "],
               [" ", " ", " "],
               [" ", " ", " "]],
        "K":  [[" ", " ", " "],
               [" ", " ", " "],
               [" ", "♔", " "],
               [" ", " ", " "],
               [" ", " ", " "]],
    }

    def __init__(self, rank: str, suit: str, face_up: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.rank = rank
        self.suit = suit
        self.face_up = face_up

    def render(self) -> str:
        if not self.face_up:
            return (
                "┌───────────┐\n"
                "│░░░░░░░░░░░│\n"
                "│░░░░░░░░░░░│\n"
                "│░░░░░░░░░░░│\n"
                "│░░░░░░░░░░░│\n"
                "│░░░░░░░░░░░│\n"
                "│░░░░░░░░░░░│\n"
                "│░░░░░░░░░░░│\n"
                "└───────────┘"
            )

        tl = f"{self.rank}{self.suit}".ljust(5)
        br = f"{self.suit}{self.rank}".rjust(5)
        pips = self.PIPS.get(self.rank, [[" "]*3]*5)

        rows = [
            "┌───────────┐",
            f"│{tl}      │",
        ]
        for pip_row in pips:
            rows.append(self._make_row(pip_row[0], pip_row[1], pip_row[2]))
        rows.append(f"│      {br}│")
        rows.append("└───────────┘")
        return "\n".join(rows)

    def _make_row(self, left: str, mid: str, right: str) -> str:
        s = self.suit
        l = s if left == "X" else left if left not in ("X", " ") else " "
        m = s if mid == "X" else mid if mid not in ("X", " ") else " "
        r = s if right == "X" else right if right not in ("X", " ") else " "
        return f"│ {l}   {m}   {r} │"  # was "│  {l}   {m}   {r}  │"

    def on_mount(self) -> None:
        if self.face_up and self.suit in ("♥", "♦"):
            self.add_class("red-card")
        elif not self.face_up:
            self.add_class("face-down")
