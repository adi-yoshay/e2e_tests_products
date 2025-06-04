from playwright.sync_api import Page, Locator
import logging


class BasePage:

    def __init__(self, page: Page):
        self.current_page = page
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    def screen_title(self) -> Locator:
        title_selector = self.current_page.locator(Selectors.ScreenTitle)
        return title_selector



class Selectors:
    ScreenTitle = ".title"




