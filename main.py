import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from dotenv import load_dotenv
import csv
import os

load_dotenv()

servicePath = os.getenv("servicePath")

options = Options()
options.add_argument("--start-maximized")
service = Service(servicePath)
driver = webdriver.Edge(service=service, options=options)

driver.get ("https://oceanhero.today/images?q=person+holding+one+finger+up")

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,".object-cover"))
)

results = []
content = driver.page_source
print(len(content))
soup = BeautifulSoup(content, "html.parser")
driver.quit()

def parse_image_urls(soup, classes, source):
    for img in soup.find_all("img", class_=classes):
        if img.get(source):
            results.append(img.get(source))

parse_image_urls(soup, "object-cover", "src")

df = pd.DataFrame(results, columns=["Image URL"])
df.to_csv("oceanhero_images.csv", index=False)
print("Saved image URLs to oceanhero_images.csv")

