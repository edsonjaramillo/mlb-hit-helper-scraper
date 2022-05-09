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
        self._browser.open_url(
            f"https://www.baseball-reference.com/players/gl.fcgi?id={id}&t=b&year=2022")
        print(f"Scraping {name} from {team_name}")
        self._browser._wait(0.25)

    def _get_table(self, table_id: str) -> ElementHandle:
        table = self._browser.page.query_selector(table_id)
        date_column = table.query_selector(f"[data-stat='date_game']")
        for _ in range(2):
            date_column.click()
            self._browser._wait(0.25)
        return table

    def _get_game_rows(self, table: ElementHandle, games_amount: int) -> List:
        rows = table.query_selector_all("tbody tr")[0:games_amount]
        return rows

    def _get_date(self, row: ElementHandle) -> str:
        date_element = row.query_selector("[data-stat='date_game']")
        date = date_element.get_attribute("csk").split(".")[0]
        return date

    def _get_data_value(self, row: ElementHandle, data_type: str) -> str:
        data_element = row.query_selector(f"[data-stat='{data_type}']")
        return int(data_element.inner_text())

    def _get_opponent(self, row: ElementHandle) -> str:
        opponent = row.query_selector(f"[data-stat='opp_ID']").inner_text()
        home_away = row.query_selector(
            "[data-stat='team_homeORaway']").inner_text()

        return f"{home_away}{opponent}"

    def _export_to_json(self) -> None:
        with open("data/batters.json", "w+", encoding='UTF-8') as file:
            json.dump([bat.to_dict()for bat in self._batters], file, indent=2)
