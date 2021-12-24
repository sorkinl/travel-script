import pandas as pd
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver

column = ["Name", "Link", "Price", "Max_Guest",
          "Bedroom", "Bed", "Bath", "Rating"]
global df
global driver
df = pd.DataFrame(columns=column)
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())