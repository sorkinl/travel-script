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
from airbnb import scrape_airbnb_from_URL
from trivago import scrape_trivago_from_URL
import settings
from selenium.webdriver.common.action_chains import ActionChains


# settings.init()

scrape_airbnb_from_URL("https://www.airbnb.com/s/Miami-Beach--FL--United-States/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_dates%5B%5D=february&flexible_trip_dates%5B%5D=january&flexible_trip_lengths%5B%5D=weekend_trip&date_picker_type=calendar&checkin=2022-03-13&checkout=2022-03-18&adults=9&query=Miami%20Beach%2C%20FL%2C%20United%20States&place_id=ChIJud3-Kxem2YgR62OUJUEXvjc&source=structured_search_input_header&search_type=autocomplete_click")
# scrape_trivago_from_URL("https://www.trivago.com/?aDateRange%5Barr%5D=2022-03-13&aDateRange%5Bdep%5D=2022-03-18&aPriceRange%5Bfrom%5D=0&aPriceRange%5Bto%5D=0&iRoomType=9&aRooms%5B0%5D%5Badults%5D=2&aRooms%5B1%5D%5Badults%5D=2&aRooms%5B2%5D%5Badults%5D=2&aRooms%5B3%5D%5Badults%5D=2&aRooms%5B4%5D%5Badults%5D=1&cpt2=14337%2F200%2C2%2F101&hasList=1&hasMap=0&bIsSeoPage=0&sortingId=1&slideoutsPageItemId=&iGeoDistanceLimit=16093&address=&addressGeoCode=&offset=0&ra=&overlayMode=")


ddf = settings.df

settings.df

ddf = settings.df
print("Gets here")
settings.df.to_excel("table.xlsx")
