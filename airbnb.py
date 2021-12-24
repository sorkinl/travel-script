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

column = ["Name", "Link", "Price", "Max_Guest",
          "Bedroom", "Bed", "Bath", "Rating"]

df = pd.DataFrame(columns=column)
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

    price_without_comma = match.group(1).replace(',', '')     # replace comma because can't be converted to a number
    price_num = float(price_without_comma)                    # convert string to float 
    return price_num
#
def scrape_airbnb_from_URL(url):
    global df
    driver.get(url)
    driver.find_element_by_tag_name("body").send_keys(Keys.END)
    time.sleep(10)
    driver.find_element_by_tag_name("body").send_keys(Keys.END)
    time.sleep(5)
    page = BeautifulSoup(driver.page_source)
    size = len(page.body.findAll("a", class_="_833p2h"))
    print(size)
    num = int(page.body.findAll("a", class_="_833p2h")[size-1].contents[0])
    print(num)

    # for i in range(num):
    page = BeautifulSoup(driver.page_source)
    arr = page.body.find_all("div", class_="c1o3pz3i")

    for x in arr:
        row = add_row(x, 1)
        df = df.append(row, ignore_index=True)
        
    # driver.find_element_by_class_name("_1bfat5l").click()
    # time.sleep(5)

def add_row(x, a_or_h):
    row = {"Name": "", "Link": "", "Price": "", "Max_Guest": "",
           "Bedroom": "", "Bed": "", "Bath": "", "Rating": "", "Airbnb": ""}

    link = "https://www.airbnb.com/{}".format(x.find("a")["href"])


    name_row = x.find_all("span", "t16jmdcf")
    data_row = x.find_all("div", "i4phm33")[0]
    row["Name"] = name_row[0].contents[0]
    print(row["Name"])
    row["Link"] = link
    row["Price"] = extract_price(x.find_all("div", "_tt122m")[0].contents[0].contents[0])
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



driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

scrape_airbnb_from_URL("https://www.airbnb.com/s/Miami-Beach--FL--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&checkin=2022-03-13&checkout=2022-03-18&adults=9&query=Miami%20Beach%2C%20FL%2C%20United%20States&place_id=ChIJud3-Kxem2YgR62OUJUEXvjc&source=structured_search_input_header&search_type=autocomplete_click")








ddf = df

df

ddf = df
print("Gets here")
df.to_excel("airbnb.xlsx")
