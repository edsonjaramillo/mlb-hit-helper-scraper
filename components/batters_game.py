class BattersGame:
    date: str
    team_played: str
    hits: int
    at_bats: int

    def __init__(self, date: str, team_played: str, hits: int, at_bats: int):
        self.date = date
        self.team_played = team_played
        self.hits = hits
        self.at_bats = at_bats

    def get_date(self) -> str:
        return self.date

    def get_team_played(self) -> str:
        return self.team_played

    def get_hits(self) -> int:
        return self.hits

    def get_at_bats(self) -> int:
        return self.at_bats

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "team_played": self.team_played,
            "hits": self.hits,
            "at_bats": self.at_bats
        }
