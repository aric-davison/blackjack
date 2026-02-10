from fastapi import FastAPI

from pydantic import BaseModel

class GameState(BaseModel):
    game_id: str
    player_hand: list[tuple[str, str, int]]
    dealer_visible: tuple[str, str, int]
    player_value: int
    is_over: bool
    result: str | None = None





app = FastAPI()

games = {}  # store active games by ID

@app.post("/game/new")
def new_game():
    # create deck, shuffle, deal, return game_id + player hand

@app.get("/game/{game_id}")
def get_game(game_id: str):
    # return current hand and visible dealer card

@app.post("/game/{game_id}/hit")
def hit(game_id: str):
    # deal card, return updated hand

@app.post("/game/{game_id}/stand")
def stand(game_id: str):
    # dealer plays, return result