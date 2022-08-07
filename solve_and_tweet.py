from wordle.webdriver import WordleWebDriver
from wordle.entropy_bot import EntropyBotPlayer

player = EntropyBotPlayer()
wordle_web_driver = WordleWebDriver(player)
wordle_web_driver.start_game()
# wordle_web_driver.make_guess("xxxxx")
# wordle_web_driver.make_guess("yyyyy")
# wordle_web_driver.make_guess("zzzzz")
# wordle_web_driver.make_guess("arose")
# wordle_web_driver.make_guess("buddy")


"""


search_box = driver.find_element(by=By.NAME, value="q")
search_button = driver.find_element(by=By.NAME, value="btnK")

search_box.send_keys("Selenium")
search_button.click()

search_box = driver.find_element(by=By.NAME, value="q")
value = search_box.get_attribute("value")
assert value == "Selenium"
"""
input("type anything to continue")

#driver.quit()


