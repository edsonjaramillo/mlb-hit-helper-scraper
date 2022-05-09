from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser, Page, Playwright, BrowserContext


class Browser:
    """Generic browser class with core methods to drive the playwright browser."""
    playwright: Playwright
    browser: Browser
    context: BrowserContext
    page: Page

    def start_browser(self, is_headless: bool = True) -> None:
        """Boots up the browser with necessary settings.
        Parameters:
            `is_headless` (bool): Whether or not to start the browser in headless mode. Default is True."""
        # self._clear_terminal()
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=is_headless)
        self.context = self.browser.new_context(
            viewport={"width": 1920, "height": 1080})
        self.page = self.context.new_page()

    def open_url(self, url: str) -> None:
        """Opens the url in the browser.

        Parameters:
            `url` (str): URL to be opened."""
        self.page.goto(url, wait_until="load", timeout=120000)

    def close_browser(self) -> None:
        """Closes the browser."""
        self.browser.close()
        self.playwright.stop()

    def _clear_terminal(self):
        """Clears the terminal."""
        print("\033c", end="")

    def _scroll_down(self, number_of_scrolls: int = 1, seconds_between_scrolls: int = 0) -> None:
        """Scrolls down the page.
        Parameters:
            `number_of_scrolls` (int): Number of times to scroll down. Default is 1.
            `seconds_between_scrolls` (int): Number of seconds to wait between each scroll. Default is 0."""
        for _ in range(number_of_scrolls):
            self.page.keyboard.press("End")
            self._wait(seconds_between_scrolls)

    def _wait(self, seconds: int) -> None:
        """Waits for the specified amount of seconds.

        Parameters:
            `seconds` (int): Number of seconds to wait."""
        self.page.wait_for_timeout(seconds * 1000)
