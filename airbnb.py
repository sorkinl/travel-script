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
    scroll_nav_out_of_way = 'window.scrollBy(0, -200);'
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
    expr = '\$?([0-9,]*\.?[0-9]*)'

    match = re.search(expr, input_str)
    print(match.group(0))              # give entire match
    print(match.group(1))              # give only text in brackets

    # replace comma because can't be converted to a number
    price_without_comma = match.group(1).replace(',', '')
    # convert string to float
    price_num = float(price_without_comma)
    return price_num
#


def scrape_airbnb_from_URL(url):
    
    driver.get(url)
    time.sleep(20)
    driver.find_element_by_tag_name("body").send_keys(Keys.END)
    time.sleep(3)
    listEl = driver.find_elements_by_class_name("_lb2964m")
    listEl[len(listEl) -1].click()
    time.sleep(2)
    #driver.find_element_by_class_name("_fk86kl8").send_keys(Keys.END)
    time.sleep(1)
    list_buttons = driver.find_elements_by_tag_name("li")
    list_buttons[len(list_buttons)-2].click()
    time.sleep(7)
    #driver.add_cookie({'name' : 'currency', 'value' : 'USD'})
    source_element = driver.find_element_by_class_name("_1bfat5l")
    if 'firefox' in driver.capabilities['browserName']:
        scroll_shim(driver, source_element)
    time.sleep(1)
    ActionChains(driver).move_to_element(source_element).perform()
    time.sleep(5)
    page = BeautifulSoup(driver.page_source)
    size = len(page.body.findAll("a", class_="_833p2h"))
    print(size)
    num = int(page.body.findAll("a", class_="_833p2h")[size-1].contents[0])
    print(num)

    for i in range(num):
        page = BeautifulSoup(driver.page_source)
        arr = page.body.find_all("div", class_="c1o3pz3i")

        for x in arr:
            row = add_row(x, 1)
            settings.df = settings.df.append(row, ignore_index=True)

        source_element = driver.find_element_by_class_name("_1bfat5l")
        if 'firefox' in driver.capabilities['browserName']:
            scroll_shim(driver, source_element)
        ActionChains(driver).move_to_element(source_element).perform()
        time.sleep(2)
        source_element.click()
        time.sleep(5)


def add_row(x, a_or_h):
    row = {"Name": "", "Link": "", "Price": "", "Max_Guest": "",
           "Bedroom": "", "Bed": "", "Bath": "", "Rating": "", "Airbnb": ""}

    link = "https://www.airbnb.com/{}".format(x.find("a")["href"])

    name_row = x.find_all("span", "t16jmdcf")
    data_row = x.find_all("div", "i4phm33")[0]
    row["Name"] = name_row[0].contents[0]
    print(row["Name"])
    row["Link"] = link
    row["Price"] = extract_price(x.find_all("div", "_tt122m")[
                                 0].contents[0].contents[0])
    print(row["Price"])
    row["Max_Guest"] = extract_number(data_row.contents[0].contents[0])
    print(row["Max_Guest"])
    try:
        row["Bedroom"] = extract_number(data_row.contents[2].contents[0])
    except:
        print("error")
    try:
        row["Bed"] = extract_number(data_row.contents[4].contents[0])
    except:
        print("error")
    try:
        row["Bath"] = extract_number(data_row.contents[6].contents[0])
    except:
        print("error")

    rating = x.find("span", {"class": "r1g2zmv6"})

    try:
        row["Rating"] = rating.contents[0]
    except:

        row["Rating"] = "NA"
    row["Airbnb"] = a_or_h

    return row
