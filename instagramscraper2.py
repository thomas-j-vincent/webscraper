from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.edge.options import Options
from dotenv import load_dotenv
import time
import random
import csv
import os

load_dotenv()

servicePath = os.getenv("servicePath")
usernameValue = os.getenv("usernameValue")
passwordValue = os.getenv("passwordValue")

print("commencing...")
try:
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    service = Service(servicePath)
    driver = webdriver.Edge(service=service, options=options)
    driver.execute_script("""
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    """)

    driver.get ("https://www.instagram.com")
    #iframes = driver.find_elements(By.TAG_NAME, "iframe")
    #print("Number of iframes:", len(iframes))
    print(driver.execute_script("return navigator.webdriver"))
    wait = WebDriverWait(driver, 20)

    try:
        cookies = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Allow')]"))
            )
        cookies.click()
        time.sleep(2)
        print("1A")
    except:
        print("no cookie pop up found")

    print("2")
    wait.until(
        EC.visibility_of_element_located((By.NAME, "email"))
    )
    print("3")
    #wait.until(EC.presence_of_element_located((By.NAME, "username")))

    username = driver.find_element(By.NAME, "email")
    print("4")
    password = driver.find_element(By.NAME, "pass")
    print("5")

    username.clear()
    username.click()
    time.sleep(1)
    #print(driver.execute_script("return document.activeElement.name"))

    print(username.is_displayed())
    print(username.is_enabled())

    #driver.execute_script("arguments[0].click();", username)

    #username.send_keys("usernameValue")
    #print(driver.page_source)
    for letter in usernameValue:
        username.send_keys(letter)
        time.sleep(random.uniform(0.1, 0.5))

    time.sleep(1)
    
    password.clear()
    #password.send_keys("Aa")
    for letter in passwordValue:
        password.send_keys(letter)
        time.sleep(random.uniform(0.1, 0.5))

    time.sleep(3)
    #login = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    with open("driverpagesource.csv", "a", newline='', encoding="utf-8") as saveFile:
        writer = csv.writer(saveFile)
        writer.writerow([driver.page_source])
    try:
        #login = wait.until(
        #    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        #)
        login = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        print("new message")
        print("Button enabled:", login.is_enabled())
        print("Button displayed:", login.is_displayed())
        driver.execute_script("arguments[0].click();", login)
        #login.click()
        time.sleep(2)
        print("1B")
    except Exception as e:
        print("no login pop up found:", e)

    #print(login.is_displayed())
    #print(login.is_enabled())
    
    print("hello")
    input("Press Enter to close the browser...")
    time.sleep(555)


    # your selenium code
except Exception as e:
    print("ERROR:", e)
    input("Press Enter to close...")