from typing import List, Tuple
from components.browser import Browser
from playwright.sync_api import ElementHandle
from datetime import date, datetime
from os import name


class GamesTodayScraper:
    _browser: Browser
    _teams: List[str] = []

    def __init__(self, browser: Browser):
        self._browser = browser

    def get_games(self) -> Tuple[bool, List[str]]:
        """
        Opens the MLB.com schedule page and returns a list of teams that have games today.

        Returns:
            Tuple[bool, List[str]]:
        - True if there are games today
        - A list of the teams that have games today

        or 

        - False if there are no games today
        - An empty list if there are no games today
        """
        today = datetime.today().strftime('%Y-%m-%d')
        self._browser.open_url(f"https://www.mlb.com/schedule/{today}")
        self._browser._wait(5)
        has_games = self._has_games_today()
        if has_games:
            schedule = self._get_schedule()
            games = self._get_baseball_games(schedule)
            for game in games:
                away, home = self._get_baseball_teams(game)
                self._add_to_teams(away)
                self._add_to_teams(home)

            self._teams.sort()
            return (has_games, self._teams)

        print("No games today")
        return (has_games, [])

    def _add_to_teams(self, team: str):
        """Adds a team to the list of teams that have games today if it is not already in the list."""
        if team not in self._teams:
            self._teams.append(team)

    def today_date(self):
        """Returns the current date as a string. Ex: TUESDAY JANUARY 1"""
        if name == "nt":
            return datetime.today().strftime('%A %B %#d').upper()
        else:
            return datetime.today().strftime('%A %B %-d').upper()

    def _has_games_today(self) -> bool:
        """Returns True if there are games today."""
        day = self._browser.page.locator(
            ".ScheduleCollectionGridstyle__SectionLabelContainer-sc-c0iua4-3").all_inner_texts()[0].replace("\n", " ").strip()

        if day == self.today_date():
            return True

        return False

    def _get_schedule(self) -> ElementHandle:
        """Returns the schedule element."""
        schedule = self._browser._query_selector(
            ".ScheduleCollectionGridstyle__SectionWrapper-sc-c0iua4-0")
        return schedule

    def _get_baseball_games(self, schedule: ElementHandle) -> ElementHandle:
        """Returns the games element."""
        games = schedule.query_selector_all(
            ".ScheduleGamestyle__DesktopScheduleGameWrapper-sc-b76vp3-0")
        return games

    def _get_baseball_teams(self, game: ElementHandle) -> List[str]:
        """Returns the home/away teams that play in the game."""

        away_element = game.query_selector(
            ".TeamMatchupLayerstyle__AwayWrapper-sc-ouprud-1")
        home_element = game.query_selector(
            ".TeamMatchupLayerstyle__HomeWrapper-sc-ouprud-2")

        away = away_element.query_selector(
            ".TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0").inner_text()
        home = home_element.query_selector(
            ".TeamWrappersstyle__DesktopTeamWrapper-sc-uqs6qh-0").inner_text()

        if away == "D-backs":
            away = "Diamondbacks"
        if home == "D-backs":
            home = "Diamondbacks"

        return (away, home)
