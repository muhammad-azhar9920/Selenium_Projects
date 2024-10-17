from booking.booking import Booking

try:
    # using "with" keyword, It executes automatically __exit__() method like, close file automatically
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency="USD")
        bot.select_place_to_go(input("Where You want to go ? "))
        bot.select_dates(input("What is check in date ? "),input("What is check out date ? "))
        bot.select_adults(int(input("How many people ?")))
        bot.click_search()
        bot.refresh() # A workaround to let our bot to grab the data properly
        bot.apply_filterations()
        bot.report_results()

except Exception as e:
    print("there is error in this program")
    print(str(e))