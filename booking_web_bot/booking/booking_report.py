# This file is going to include method that will parse
# The specific data that we need from each one of the deal boxes.
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
import time

class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()
        print("deal_boxes ", len(self.deal_boxes))

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR,
            value='div[data-testid="property-card-container"]'
        )

    def pull_deal_box_attributes(self):
        collection = []
        # pulling the hotel name
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(
                By.CSS_SELECTOR,
                value='div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()
            # print(hotel_name)
            # pulling the hotel price
            hotel_price = deal_box.find_element(
                By.CSS_SELECTOR,
                value='span[data-testid="price-and-discounted-price"]'
            ).get_attribute('innerHTML').strip()

            collection.append(
                [hotel_name, hotel_price]
            )
        return collection