from typing import List, Tuple
from components.batters_game import BattersGame


class Batter:
    id: str
    name: str
    team_code: str
    team_name: str
    primary_color: str
    secondary_color: str
    moving_average: float = 0.00
    games: List[BattersGame] = []

    def __init__(self, id: str, name: str, team: dict):
        self.id = id
        self.name = name
        self.team_code = team["team_code"]
        self.team_name = team["team_name"]
        self.primary_color = team["primary_color"]
        self.secondary_color = team["secondary_color"]

    def get_id(self) -> str:
        return self.id

    def get_name(self) -> str:
        return self.name

    def get_team_code(self) -> str:
        return self.team_code

    def get_url_info(self) -> Tuple[str, str, str]:
        return self.id, self.name, self.team_name

    def add_games(self, batters_games: List[BattersGame]) -> None:
        self.games = batters_games
        self.calculate_moving_average()

    def get_batting_games(self) -> List[BattersGame]:
        return self.games

    def calculate_moving_average(self) -> None:
        total_hits = 0
        number_of_games = len(self.games)

        for game in self.games:
            total_hits += game.get_hits()

        if number_of_games > 0:
            self.moving_average = round(total_hits / number_of_games, 3)
        else:
            self.moving_average = round(0, 2)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "team_code": self.team_code,
            "team_name": self.team_name,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "moving_average": self.moving_average,
            "games": [game.to_dict() for game in self.games]
        }
