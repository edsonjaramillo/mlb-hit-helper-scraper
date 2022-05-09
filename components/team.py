from typing import List, Tuple
from components.batter import Batter

class Team:
    team_code: str
    name: str
    primary_color: str
    secondary_color: str
    batters: List[Batter] = []

    def __init__(self, team_code: str, name: str, primary_color: str, secondary_color: str) -> None:
        self.team_code = team_code
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color

    def get_team_code(self) -> str:
        return self.team_code

    def add_players(self, batters: List[Batter]) -> None:
        self.batters = batters

    def get_batters(self) -> List[Batter]:
        return self.batters

    def get_name(self) -> str:
        return self.name

    def get_attributes(self) -> Tuple[str, str, str, str]:
        return (self.team_code, self.name, self.primary_color, self.secondary_color)

    def to_dict(self) -> dict:
        return {
            "team_code": self.team_code,
            "name": self.name,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "batters": [batter.to_dict() for batter in self.batters],
        }
