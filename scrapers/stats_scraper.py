import json
from typing import List
from components.browser import Browser
from playwright.sync_api import ElementHandle
from components.batters_game import BattersGame
from components.batter import Batter


class StatsScraper:
    _browser: Browser
    _batters: List[Batter] = []

    def __init__(self, browser: Browser):
        self._browser = browser

    def get_stats(self, batters: List[Batter]) -> List[Batter]:
        """Adds the stats to the batters previously scraped.

        Parameters:
            `batters` (List[Batter]): The batters to add the stats to.

        Returns:
            `batters` (List[Batter]): The batters with the stats added."""
        batters_list = batters
        for batter in batters_list:
            id, name, team_name = batter.get_url_info()
            self._open_batters_page(id, name, team_name)
            batting_table = self._get_table("#div_batting_gamelogs")
            rows = self._get_game_rows(batting_table, 10)
            batting_games: List[BattersGame] = []
            for row in rows:
                date = self._get_date(row)
                team_played = self._get_opponent(row)
                hits = self._get_data_value(row, "H")
                at_bats = self._get_data_value(row, "AB")
                batter_game = BattersGame(date, team_played, hits, at_bats)
                batting_games.append(batter_game)

            batter.add_games(batting_games)
        self._batters = batters
        self._batters.sort(key=lambda x: x.moving_average, reverse=True)
        self._export_to_json()
        return batters_list

    def _open_batters_page(self, id: str, name: str, team_name: str) -> None:
        """Opens the batters page for the given player.
        Ex: https://www.baseball-reference.com/players/gl.fcgi?id=`id`&t=b&year=2022

        Parameters:
            `id` (str): The player's id.
            `name` (str): The player's name.
            `team_name` (str): The player's team name."""
        self._browser.open_url(
            f"https://www.baseball-reference.com/players/gl.fcgi?id={id}&t=b&year=2022")
        print(f"Scraping {name} from {team_name}")
        self._browser._wait(6, 3)

    def _get_table(self, table_id: str) -> ElementHandle:
        """Gets the table with the given id.

        Parameters:
            `table_id` (str): The id of the table to get.

        Returns:
            `table` (ElementHandle): The table with the given id."""
        table = self._browser.page.wait_for_selector(table_id, timeout=0, state="visible")
        date_column = table.query_selector(f"[data-stat='date_game']")
        for _ in range(2):
            date_column.click()
            self._browser._wait(1, 0.5)
        return table

    def _get_game_rows(self, table: ElementHandle, games_amount: int) -> List[ElementHandle]:
        """Gets the rows of the games table.

        Parameters:
            `table` (ElementHandle): The table to get the rows from.
            `games_amount` (int): The amount of games to get.

        Returns:
            `rows` (List[ElementHandle]): The rows of the games table."""
        rows = table.query_selector_all("tbody tr")[0:games_amount]
        return rows

    def _get_date(self, row: ElementHandle) -> str:
        """Gets the date of the game.

        Parameters:
            `row` (ElementHandle): The row to get the date from.

        Returns:
            `date` (str): The date of the game."""
        date_element = row.query_selector("[data-stat='date_game']")
        date = date_element.get_attribute("csk").split(".")[0]
        return date

    def _get_data_value(self, row: ElementHandle, data_type: str) -> str:
        """Gets the data value of the given type.

        Parameters:
            `row` (ElementHandle): The row to get the data from.
            `data_type` (str): The type of data to get.

        Returns:
            `data_value` (str): The data value of the given type."""
        data_element = row.query_selector(f"[data-stat='{data_type}']")
        return int(data_element.inner_text())

    def _get_opponent(self, row: ElementHandle) -> str:
        """Gets the opponent of the game.

        Parameters:
            `row` (ElementHandle): The row to get the opponent from.

        Returns:
            `opponent` (str): The opponent of the game."""
        opponent = row.query_selector(f"[data-stat='opp_ID']").inner_text()
        home_away = row.query_selector(
            "[data-stat='team_homeORaway']").inner_text()

        return f"{home_away}{opponent}"

    def _export_to_json(self) -> None:
        """Exports the batters to a json file."""
        with open("data/batters.json", "w+", encoding='UTF-8') as file:
            json.dump([bat.to_dict()for bat in self._batters], file, indent=2)
