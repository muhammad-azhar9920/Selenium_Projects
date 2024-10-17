from selenium import webdriver
from selenium.webdriver.common.by import By
import booking.constants as const
import time
from booking.booking_filteration import BookingFilteration
from booking.booking_report import BookingReport
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable

class Booking(webdriver.Chrome):
    def __init__(self, teardown=False):
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        # for open chrome after working
        options.add_experimental_option("detach",True)
        # initialize the chrome webdriver
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()


    def land_first_page(self):
        self.get(const.BASE_URL)

    def check_adds(self):
        try:
            close_adds_elem = self.find_element(
                By.CSS_SELECTOR,
                value='button[aria-label="Dismiss sign-in info."]'
            )
            if(close_adds_elem):
                print("found adds")
                close_adds_elem.click()
        except:
            print("adds elem not found.")
    
    def change_currency(self, currency=None):
        self.check_adds()
        currency_element = self.find_element(
            By.CSS_SELECTOR,
            value='button[data-testid="header-currency-picker-trigger"]'
        )
        currency_element.click()
        self.check_adds()
        selected_currency_element = WebDriverWait(self,15).until(EC.element_to_be_clickable(
            (By.XPATH,
            f"//div[@data-testid='Suggested for you']//div[contains(@class,'CurrencyPicker_currency')][normalize-space()='{currency}']"
            )
        ))
        selected_currency_element.click()
    
    def select_place_to_go(self, place_to_go):
        self.check_adds()
        search_field = self.find_element(
            By.ID,
            value=":rh:"
        )
        search_field.clear()
        search_field.send_keys(place_to_go)
        self.check_adds()
        first_result = self.find_element(
            By.CSS_SELECTOR,
            value="li[id='autocomplete-result-0']"
        )
        if(first_result):
            first_result.click()
        else:
            print("first result not found")

    def select_dates(self, check_in_date, check_out_date):
        check_in_elem = self.find_element(
            By.CSS_SELECTOR,
            value=f'span[data-date="{check_in_date}"]'
        )
        check_in_elem.click()

        check_out_elem = self.find_element(
            By.CSS_SELECTOR,
            value=f'span[data-date="{check_out_date}"]'
        )
        check_out_elem.click()

    def select_adults(self, count=1):
        selection_elem = self.find_element(
            By.XPATH,
            value="//span[@class='a8887b152e c7ce171153']"
        )
        selection_elem.click()

        while True:
            decrease_adults_elem = self.find_element(
                By.XPATH,
                value="//button[@class='a83ed08757 c21c56c305 f38b6daa18 d691166b09 ab98298258 bb803d8689 e91c91fa93']"
            )
            decrease_adults_elem.click()
            # If the value of adults reaches 1, then we should get out of the while loop
            adults_value_elem = self.find_element(
                By.ID,
                value="group_adults"
            )
            adults_value = adults_value_elem.get_attribute("value")
            if int(adults_value) == 1:
                break
        increase_adults_elem = self.find_element(
            By.XPATH,
            value="//body[1]/div[3]/div[2]/div[1]/form[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/button[2]"
        )
        for i in range(count-1):
            increase_adults_elem.click()
        time.sleep(1)

    def click_search(self):
        search_button = self.find_element(
            By.CSS_SELECTOR,
            value='button[type="submit"]'
        )
        search_button.click()

    def apply_filterations(self):
        filteration = BookingFilteration(driver=self)
        filteration.apply_star_rating(3,4)

    def report_results(self):
        hotel_boxes = WebDriverWait(self,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'div[data-results-container="1"]')))
        print("After hotel_boxes")
        if(hotel_boxes):
            report = BookingReport(hotel_boxes)
            table = PrettyTable()
            table.field_names = ["Hotel Name", "Price"]
            table.add_rows(report.pull_deal_box_attributes())
            print(table)