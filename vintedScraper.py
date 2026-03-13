from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.options import Options
from dotenv import load_dotenv
import pywhatkit
import datetime
import time
import csv
import os

load_dotenv()

servicePath = os.getenv("servicePath")
filePath = os.getenv("filePath")
phoneNumber = os.getenv("phoneNumber")

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(servicePath)
driver = webdriver.Edge(service=service, options=options)

driver.get ("https://www.vinted.co.uk/catalog?brand_ids[]=88&page=1&time=1772965691&size_ids[]=3&price_to=15.00&currency=GBP")
wait = WebDriverWait(driver, 20)
data = []
#send = []
seen_links = set()
include_keywords = ["jumper","hoodie","shirt","t-shirt","polo","tshirt","sweater","sweatshirt","long","knit","top"]
exclude_keywords = ["vest","button","blazer","skirt", "jean", "shorts"]
marker = "<!-- GENERATED CONTENT BELOW -->"
website = "index.html"
date = datetime.datetime.now()
#print(date)

with open(filePath, "r") as file:
    lines = file.readlines()

kept_lines = []
for line in lines:
    kept_lines.append(line)
    if marker in line:
        break

with open(filePath, "w") as file:
    file.writelines(kept_lines)

with open(filePath, "a", encoding="utf-8") as file:
    file.write(f"""
        <div>
        last updated: {date.strftime("%d/%m/%Y %H:%M:%S")}</div>
        <br></br>
    """)

try:
    with open("vintedItems.csv", "r") as seenItems:
        seen = csv.reader(seenItems, delimiter="@")
        for eachLine in seen:
            link = str(eachLine[2])
            seen_links.add(link)
except FileNotFoundError:
    print("no file seen, starting fresh")

try:
    cookies = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
        )
    cookies.click()
    time.sleep(2)
    print("1A")
except:
    print("no cookie pop up found")

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

try:
    items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".new-item-box__image-container"))
    )
    print("1B")
    #print(items)
    for item in items:
        link = item.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        img = item.find_element(By.CSS_SELECTOR, "img")
        image_url = img.get_attribute("src") or img.get_attribute("data-src")

        title = img.get_attribute("alt")
        if any(word in link for word in include_keywords):
            if not any(word in link for word in exclude_keywords):
                if link not in seen_links:
                    seen_links.add(link)
                    data.append([title, link, image_url])
                print("item found")
except:
    print("no items found")

for title, link ,image_url in data:
    with open("vintedItems.csv", "a") as saveFile:
        saveLine = f"\n{title}@{image_url}@{link}"
        saveFile.write(saveLine)
    #send.append(link)
    with open("index.html", "a", encoding="utf-8") as f:
        f.write(f"""
            <div>
            <tr>
            <td>{title}</td>
            <td><img src="{image_url}" width="150"></td>
            <td><a href="{link}">View</a></td>
            </tr>
            </div>
            <br></br>
        """)
#print(send)
pywhatkit.sendwhatmsg_instantly(
    phoneNumber,
    website
)

print("hello")
input("Press Enter to close the browser...")


