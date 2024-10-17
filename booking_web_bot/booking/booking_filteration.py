# This file will include a class with instance method.
# that will be responsible to interact with our website
# After we have some results, to apply filteration

# to get autocompletion
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BookingFilteration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):

        self.driver.execute_script("window.scrollTo(0,1700)")
        time.sleep(1)
        star_filteration_box = WebDriverWait(self.driver,15).until(EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                'div[data-filters-group="class"]'
            )
        ))

        star_child_elements = star_filteration_box.find_elements(
            By.CSS_SELECTOR,
            value="*"
        )
        print(len(star_child_elements))

        try:
            for star_value in star_values:
                print('star_value',star_value)
                for star_element in star_child_elements:
                    if (str(star_element.get_attribute("innerHTML")).strip() == f"{star_value} stars"):
                        print(star_element.get_attribute("innerHTML"))
                        star_element.click()
                        break
        except:
            pass