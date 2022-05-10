from components.browser import Browser
from scrapers.teams_scraper import TeamsScraper
from scrapers.stats_scraper import StatsScraper
from scrapers.games_today_scraper import GamesTodayScraper
from components.cms import CMS
from components.logger import Logger


def main() -> None:
    NUM_BATTERS = 3
    logger = Logger()

    browser = Browser()
    browser.start_browser(is_headless=True)
    logger.report_start()
    try:
        has_teams, teams_playing = GamesTodayScraper(browser).get_games()
        has_teams = True
        if has_teams == True:
            batters = TeamsScraper(browser).get_batters(NUM_BATTERS, teams_playing)
            final_batters = StatsScraper(browser).get_stats(batters)
            CMS().update_cms(final_batters)
    except Exception:
        logger.report_exception()
    finally:
        logger.report_end()
        browser.close_browser()


if __name__ == "__main__":
    main()
