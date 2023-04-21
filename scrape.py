import json
import os
import psycopg2
import urllib.request
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from pyshadow.main import Shadow
from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from pathlib import Path
PROJECT_PATH  = Path(__file__).parent

# # Create a new instance of the Firefox driver
driver = webdriver.Chrome()
driver.implicitly_wait(20)


# Navigate to the page that contains the iframe
driver.get("https://www.sreality.cz/hledani/prodej/domy")


# Below line creates instance of ActionChains class 
action = ActionChains(driver)
# Below line locates and stores an element which is outside the shadow-root
element_outside_shadow = driver.find_element(By.XPATH, "//div[@class='szn-cmp-dialog-container']")
# Below 2 lines clicks on the browser at an offset of co-ordinates x=5 and y=5
action.move_to_element_with_offset(element_outside_shadow, 5, 5)
action.click()
# Below 2 lines presses TAB key 9 times so that pointer moves to "Souhlasím" button and presses ENTER key once
action.send_keys(Keys.TAB * 9).perform()
action.send_keys(Keys.ENTER).perform()



count = 0
images = []
data = []

h2 = []
links = []

# Create the folder if it doesn't exist
foldername = "50_img"
if not os.path.exists(foldername):
    os.makedirs(foldername)


while count < 500:
    # Get all the text-wrap elements on the page
    elements = driver.find_elements(By.CLASS_NAME, "text-wrap")
    houses_elements = driver.find_elements(By.CSS_SELECTOR, "div[class='_2xzMRvpz7TDA2twKCXTS4R']")

    # Print the text of each element
    for element in elements:
        # Wait 20 seconds for each element
        WebDriverWait(driver, 20).until(EC.visibility_of(element))
        title_element = element.find_element(By.TAG_NAME, "h2")
        # print(title_element.text)
        h2.append(title_element.text)

        # Create a new dictionary for each title element
        data_dict = {"title": title_element.text, "images": []}
        data.append(data_dict)

    for house in houses_elements:
        if count >= 500:
            break
        # Get the link element that contains "detail/prodej/"
        link_element = house.find_element(By.CSS_SELECTOR, "div._15Md1MuBeW62jbm5iL0XqR a[href*='detail/prodej/']")
        # Get the image source from the first image element within the link element
        img_element = link_element.find_element(By.CSS_SELECTOR, "img")
        img_src = img_element.get_attribute("src")
        # Add the image source to the "images" list in the last dictionary in the "data" list
        data[-1]["images"].append(img_src)
        links.append(img_src)
        print(img_src)
        count += 1

combined_dict = dict(zip(h2, links))
print(combined_dict)

table_name = "sreality"
name_column = "Names"
image_column = "Images"

conn = psycopg2.connect(
    host="localhost",
    database="sreality_db",
    user="postgres",
    password="password",
    port="5555"
)

cursor = conn.cursor()
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

create_table_query = f"""
    CREATE TABLE {table_name} (
        id SERIAL PRIMARY KEY,
        {name_column} TEXT NOT NULL,
        {image_column} JSONB NOT NULL
    );
"""
cursor.execute(create_table_query)
conn.commit()

json_data = json.dumps(combined_dict)


insert_query = f"INSERT INTO {table_name} ({name_column}, {image_column}) VALUES (%s, %s)"

for key, value in combined_dict.items():
    cursor.execute(insert_query, (key, json.dumps(value)))
conn.commit()

cursor.close()
conn.close()



conn = psycopg2.connect(
    host="localhost",
    database="sreality_db",
    user="postgres",
    password="password",
    port="5555"
)

cursor = conn.cursor()

select_query = "SELECT * FROM sreality"
cursor.execute(select_query)

rows = cursor.fetchall()

for row in rows:
    print(row)

cursor.close()
conn.close()
