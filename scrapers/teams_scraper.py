import json
from typing import List, Tuple
from components.browser import Browser
from playwright.sync_api import ElementHandle
from components.batter import Batter


class TeamsScraper:
    _browser: Browser
    _batters: List[Batter] = []

    def __init__(self, browser: Browser) -> None:
        """Initialize the scraper.

        Parameters:
            `browser` (Browser): The browser instance."""
        self._browser = browser

    def get_batters(self, num_batters: int, teams_playing: List[str]) -> List[Batter]:
        """Get the batters for the teams playing.

        Parameters:
            `num_batters` (int): The number of batters to get from each team.
            `teams_playing` (List[str]): The teams playing.

        Returns:
            `List[Batter]`: The batters."""

        team_directory = self._get_teams_json(teams_playing)

        for team in team_directory:
            team_code = team["team_code"]
            self._open_team_page(team_code)
            batting_table = self._get_table("#team_batting", "H")
            batting_rows = self._get_player_rows(batting_table, num_batters)
            self._add_batters(batting_rows, team)

        self._export_to_json()
        return self._batters

    def _add_batters(self, batter_rows: List[ElementHandle], team: dict) -> List[Batter]:
        """Add the batter to the list of batters.

        Parameters:
            `batter_rows` (List[ElementHandle]): The rows to cycle through.
            `team` (dict): The team dictionary.

        Returns:
            `List[Batter]`: The batters."""
        for row in batter_rows:
            id, name = self._get_player_name(row)
            player = Batter(id, name, team)
            self._batters.append(player)

        return self._batters

    def _open_team_page(self, team_code: str):
        """Open the team page.

        Parameters:
            `team_code` (str): The team code."""
        self._browser.open_url(
            f"https://www.baseball-reference.com/teams/{team_code}/2022.shtml")
        print(f"Scraping {team_code}")
        self._browser._wait(3)

    def _get_table(self, table_id: str, data_stat: str) -> ElementHandle:
        """Get the table on webpage, and gets sorted by the data-stat.
        The data-stat column is clicked to sort the table.

        Parameters:
            `table_id` (str): The table id.
            `data_stat` (str): The data stat attribute.

        Returns:
            `ElementHandle`: The table."""
        table = self._browser._query_selector(f"{table_id}")
        table.query_selector(f"[data-stat={data_stat}]").click()
        self._browser._wait(3)
        return table

    def _get_player_rows(self, table: ElementHandle, players_amount) -> List[ElementHandle]:
        """Get the player rows and get the amound of players.

        Parameters:
            `table` (ElementHandle): The table to get the rows from.
            `players_amount` (int): The amount of players to get.

        Returns:
            `List[ElementHandle]`: The player rows from the table."""
        rows = table.query_selector_all("tbody tr")[0:players_amount]
        return rows

    def _get_player_name(self, player_row: ElementHandle) -> Tuple[str, str]:
        """Get the player name and id from ElementHandle and cleans the id with
        the _clean_id function.

        Parameters:
            `player_row` (ElementHandle): The row to get the name from.

        Returns:
            `Tuple[str, str]`: The player id and name."""
        player = player_row.query_selector("[data-stat='player']")
        id = player.get_attribute("data-append-csv")
        name = player.query_selector("a").inner_text()

        return self._clean_id(id), name

    def _clean_id(self, id: str) -> str:
        """Clean the id to get the player id by removing the unnecessary characters.

        Parameters:
            `id` (str): The id to clean.

        Returns:
            `id` (str): The cleaned id."""

        return id.split("/")[-1]

    def _export_to_json(self) -> None:
        """Export the batters to a json file."""
        with open("data/batters.json", "w+", encoding='UTF-8') as file:
            json.dump([bat.to_dict()for bat in self._batters], file, indent=2)

    def _get_teams_json(self, teams_playing: List[str]) -> List[dict]:
        """Get the teams json file and filter the teams that are playing..

        Parameters:
            `teams_playing` (List[str]): The teams playing.

        Returns:
            `List[dict]`: The teams playing."""
        with open("data/teams_directory.json", "r") as file:
            all_teams: List[dict] = json.load(file)

        final_teams: List[dict] = []
        for team in all_teams:
            name = team["team_name"]
            team_code = team["team_code"]
            primary_color = team["primary_color"]
            secondary_color = team["secondary_color"]
            is_playing = self._check_if_team_is_playing(name, teams_playing)
            if is_playing:
                final_teams.append({
                    "team_code": team_code,
                    "team_name": name,
                    "primary_color": primary_color,
                    "secondary_color": secondary_color,
                })
        print(f"Found {len(final_teams)} teams")
        return final_teams

    def _check_if_team_is_playing(self, team_name: str, teams_playing: List[str]) -> bool:
        """Check if the team is playing.

        Parameters:
            `team_name` (str): The team name.
            `teams_playing` (List[str]): The teams playing.

        Returns:
            `True` if the team is playing, `False` if not."""
        for team in teams_playing:
            if team_name.find(team) != -1:
                return True
