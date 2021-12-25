from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from webdriver_manager.firefox import GeckoDriverManager
import requests
import re
import settings
from selenium.webdriver.common.action_chains import ActionChains

driver = settings.driver


def scroll_shim(passed_in_driver, object):
    x = object.location['x']
    y = object.location['y']
    scroll_by_coord = 'window.scrollTo(%s,%s);' % (
        x,
        y
    )
    scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
    passed_in_driver.execute_script(scroll_by_coord)
    passed_in_driver.execute_script(scroll_nav_out_of_way)


def extract_number(input_str):
    if not input_str and not isinstance(input_str, str):
        return 0
    out_number = ''
    for ele in input_str:
        if (ele == '.' and '.' not in out_number) or ele.isdigit():
            out_number += ele
        elif out_number:
            break
    return float(out_number)


def extract_price(input_str):
    expr = '\$([0-9,]*\.?[0-9]*)'

    match = re.search(expr, input_str)
    print(match.group(0))              # give entire match
    print(match.group(1))              # give only text in brackets

    # replace comma because can't be converted to a number
    price_without_comma = match.group(1).replace(',', '')
    # convert string to float
    price_num = float(price_without_comma)
    return price_num


def scrape_trivago_from_URL(url):

    driver.get(url)
    time.sleep(10)
    source_element = driver.find_element_by_class_name('btn--next')
    if 'firefox' in driver.capabilities['browserName']:
        scroll_shim(driver, source_element)
    ActionChains(driver).move_to_element(source_element).perform()
    time.sleep(5)
    page = BeautifulSoup(driver.page_source)
    size = len(page.body.findAll(
        "button", class_="btn btn--pagination btn--small pagination__page"))
    print(size)
    num = int(page.body.findAll(
        "button", class_="btn btn--pagination btn--small pagination__page")[size-1].contents[0])
    print(num)

    for i in range(num):
        page = BeautifulSoup(driver.page_source)
        arr = page.body.find_all(
            "li", class_="hotel-item item-order__list-item js_co_item")

        for x in arr:
            row = add_row(x, 0)
            settings.df = settings.df.append(row, ignore_index=True)

        if(i < num-1):
            source_element = driver.find_element_by_class_name('btn--next')
            if 'firefox' in driver.capabilities['browserName']:
                scroll_shim(driver, source_element)
            ActionChains(driver).move_to_element(source_element).perform()
            driver.find_element_by_class_name("btn--next").click()
            time.sleep(2)


def add_row(x, a_or_h):
    row = {"Name": "", "Link": "", "Price": "", "Max_Guest": "",
           "Bedroom": "", "Bed": "", "Bath": "", "Rating": "", "Airbnb": ""}

    #link = "https://www.airbnb.com/{}".format(x.find("a")["href"])

    name_row = x.find_all("span", "item-link name__copytext")
    #data_row = x.find_all("div", "i4phm33")[0]
    row["Name"] = name_row[0].contents[0]
    print(row["Name"])
    #row["Link"] = link
    row["Price"] = extract_price(x.find_all(
        "strong", "accommodation-list__pricePerStay--22fbe")[0].contents[0])
    print(row["Price"])
    row["Max_Guest"] = "NA"
    print(row["Max_Guest"])
    try:
        row["Bedroom"] = "NA"
    except:
        print("error")
    try:
        row["Bed"] = "NA"
    except:
        print("error")
    try:
        row["Bath"] = "NA"
    except:
        print("error")

    rating = x.find("span", {
                    "class": "item-components__pillValue--d848f item-components__value-sm--64f76 item-components__pillValue--d848f"})

    try:
        row["Rating"] = rating.contents[0]
    except:

        row["Rating"] = "NA"
    row["Airbnb"] = a_or_h

    return row


#driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

# scrape_trivago_from_URL("https://www.trivago.com/?aDateRange%5Barr%5D=2022-03-13&aDateRange%5Bdep%5D=2022-03-18&aPriceRange%5Bfrom%5D=0&aPriceRange%5Bto%5D=0&iRoomType=9&aRooms%5B0%5D%5Badults%5D=2&aRooms%5B1%5D%5Badults%5D=2&aRooms%5B2%5D%5Badults%5D=2&aRooms%5B3%5D%5Badults%5D=2&aRooms%5B4%5D%5Badults%5D=1&cpt2=14337%2F200%2C2%2F101&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=16093&address=&addressGeoCode=&offset=0&ra=&overlayMode=")


#ddf = df

# df

#ddf = df
#print("Gets here")
# df.to_excel("trivago.xlsx")
