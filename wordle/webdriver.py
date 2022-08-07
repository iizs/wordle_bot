import time
import json
import logging
import tkinter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from .game import WordleGameStatus
from .exception import ResignException, WordleHelperException

logger = logging.getLogger(__name__)


class LocalStorage:
    def __init__(self, driver):
        self.driver = driver

    def __len__(self):
        return self.driver.execute_script("return window.localStorage.length;")

    def items(self):
        return self.driver.execute_script(
            "var ls = window.localStorage, items = {}; "
            "for (var i = 0, k; i < ls.length; ++i) "
            "  items[k = ls.key(i)] = ls.getItem(k); "
            "return items; ")

    def keys(self):
        return self.driver.execute_script(
            "var ls = window.localStorage, keys = []; "
            "for (var i = 0; i < ls.length; ++i) "
            "  keys[i] = ls.key(i); "
            "return keys; ")

    def get(self, key):
        return self.driver.execute_script("return window.localStorage.getItem(arguments[0]);", key)

    def set(self, key, value):
        self.driver.execute_script("window.localStorage.setItem(arguments[0], arguments[1]);", key, value)

    def has(self, key):
        return key in self.keys()

    def remove(self, key):
        self.driver.execute_script("window.localStorage.removeItem(arguments[0]);", key)

    def clear(self):
        self.driver.execute_script("window.localStorage.clear();")

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.keys()

    def __iter__(self):
        return self.items().__iter__()

    def __repr__(self):
        return self.items().__str__()


class WordleWebDriver:
    SITE_URL = "https://www.nytimes.com/games/wordle/index.html"
    HOW_TO_PLAY_MODAL_CLOSE_BUTTON_CLASS_NAME = "Modal-module_closeIcon__b4z74"
    KEYBOARD_BUTTONS_CLASS_NAME = "Key-module_key__Rv-Vp"
    TOAST_CONTAINER_ID = "ToastContainer-module_gameToaster__yjzPn"
    SHARE_BUTTON_ID = "share-button"

    def __init__(self, player):
        self.player = player
        self.tkroot = tkinter.Tk()
        self.tkroot.withdraw()  # to hide the window
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        self.driver.get(WordleWebDriver.SITE_URL)
        self.driver.implicitly_wait(0.5)
        self.local_storage = LocalStorage(self.driver)

        how_to_play_modal_close_button = self.driver.find_element(
            by=By.CLASS_NAME,
            value=WordleWebDriver.HOW_TO_PLAY_MODAL_CLOSE_BUTTON_CLASS_NAME
        )
        how_to_play_modal_close_button.click()

        # '←': Backspace
        # '↵': Enter
        # 'a-z': A-Z
        self.keyboard_buttons = {}
        buttons = self.driver.find_elements(by=By.CLASS_NAME, value=WordleWebDriver.KEYBOARD_BUTTONS_CLASS_NAME)
        for button in buttons:
            self.keyboard_buttons[button.get_attribute("data-key")] = button

        self.state = json.loads(self.local_storage.get("nyt-wordle-state"))
        self.prev_state = json.loads(self.local_storage.get("nyt-wordle-state"))

    def make_guess(self, guess):
        assert len(guess) == 5

        for i in range(5):
            self.keyboard_buttons['←'].click()
        for c in guess:
            self.keyboard_buttons[str(c).lower()].click()
        self.keyboard_buttons['↵'].click()

        time.sleep(2)

    def __update_state__(self):
        self.prev_state = dict(self.state)
        self.state = json.loads(self.local_storage.get("nyt-wordle-state"))

    def start_game(self):
        self.player.restart()
        status = WordleGameStatus()
        try:
            for i in range(6):
                valid_guess = False
                guess = None
                while not valid_guess:
                    guess = self.player.make_guess(status)
                    if guess == '/resign':
                        raise ResignException()

                    self.make_guess(guess)
                    self.__update_state__()
                    if self.prev_state['rowIndex'] != self.state['rowIndex']:
                        valid_guess = True
                    else:
                        status.set_as_invalid_guess(guess)
                m = ''
                for evaluation in self.state['evaluations'][self.state['rowIndex'] - 1]:
                    if evaluation == 'correct':
                        m += '🟩'
                    elif evaluation == 'present':
                        m += '🟨'
                    elif evaluation == 'absent':
                        m += '⬛'
                    else:
                        raise WordleHelperException(f'Unexpected evaluation value: {evaluation}')
                status.add(guess, m)
                if status.win:
                    break
        except ResignException:
            return False

        if status.win:
            self.player.win(status)
        else:
            self.player.lose(status, self.state["solution"])

        self.player.game_over()

        return status.win

    def get_share_texts(self):
        while True:
            try:
                share_button = self.driver.find_element(By.ID, WordleWebDriver.SHARE_BUTTON_ID)
                break
            except NoSuchElementException as e:
                logger.info('Share Button is not ready yet. Waiting 1 second.')
                time.sleep(1)
        logger.info(share_button.is_displayed())
        share_button.click()
        return self.tkroot.clipboard_get()
