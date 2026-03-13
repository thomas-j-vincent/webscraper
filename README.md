# webscraper

## Contents:

[Main.py](#Mainpy)

[vinted Scraper](#vintedscraper)

[Instagram Scraper](#instagramscraper)

## Main.py

Main.py is a scraper for oceanhero, the weird browser that I choose to force myself to put up with *but think of the turtles!* -yeah sure. Anyway, it scrapes the page looking for images of a person holding up one finger - and then returns a csv file containing all of these images - this was for a machine learning project I was attempting before I realised that my laptop wouldn't be able to handle all of the compute power required. But here is the code anyway:

### Code:

We first import a bunch of modules, these are: pandas - for formatting the data that gets written to the csv, beautiful soup - for reading the html processed by selenium, selenium - for opening the webpage and waiting for all the html to load, dotenv - which is used to load the .env file and os - to actually get the .env variables.

We then use the dotenv module to `load_dotenv()` which sets up the .env file to be set as variables, this is how we get the service path (where the msedgedriver is stored on your computer) using `os.getenv("servicePath")` and the os module.

In the next few lines we set up the selenium module adding arguments such as `options.add_argument("--start-maximized")` (the webpage opens up full screen) although these are for user preference.

`driver.get` tells selenium the webpage that the module should open.

``` python
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,".object-cover"))
)
``` 
tells the module to wait until the CSS selector object-cover before continuing with the code - this ensures that the data we want to read is available when we come to access it.

results is a list containing the results we want to save.
`content = driver.page_source` creates a string of the entire html of the website and
`soup = BeautifulSoup(content, "html.parser")` allows beautiful soup to analyse it
`driver.quit()` we then close the webpage.

The function parse_image_urls takes the analysed html, the class to look for, and where to begin. It then appends those results to the results list.

df puts the results in a column titled: Image URL, it then sets it as a csv - without an index and prints "Saved image URLs to oceanhero_images.csv"

## VintedScraper

The Vinted scraper was a commision by my sister to take all the Ralph Lauren items on vinted (the ones that she wants at least) and format them in an easy way for her to look over and decide whether or not to buy. This will then be updated whenever the code is run - showing only the new "unseen" items. I decided to do this from a webpage as sending individual links was unfeasible incase large amounts of items were uploaded in one day, and it could be formatted nicely.

### Code: 

We first import the main modules from the last program:
- selenium; for controlling the webpage
- dotenv; for reading the .env file
- os; for converting the .env variables to useable variables
We then add in some new modules relating to how to format the data
- pywhatkit; sends a message via whatsapp - to send my sister the new link to all the products
- datetime; to show when the webpage was updated last
- time; to allow us to sleep the program for a short period of time
- csv; so we can read and write to csv files.

We then `load_dotenv()` as we did in the last program.

from the .env we use the os module to import the same variable as last time, service path, with the addition of filePath and phoneNumber. filePath is where the html file is on the computer - required so it can be modified, and phoneNumber is the number you are sending the whatsapp messages to.

We then set up the selenium webdriver like last time but add in some other arguments:
``` python
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
service = Service(servicePath)
driver = webdriver.Edge(service=service, options=options)
```
- start maximized opens up the webpage so we can see it, useful for debugging and because it's cool to watch
- --disable features=AutomationControlled disables the blink feature (blink is the browser engine used by lots of search engines) that tells the webpage that the visitor is a bot, reducing the chance the browser knows we're a bot.
- excludeSwitches enable-automation removes certain start-up flags that tell the webpage that we're not a an actual human - this can be seen on the webpage as the "Edge is being controlled by an automation software" banner at the top of the page disappears.
- useAutomationExtension, False prevents selenium from installing its own browser extension, reducing the work that selenium can do but prevents the browser from seeing that we are using selenium.
and the rest is as normal.

`driver.get` is the webpage we want to access, here I have included as many of the native search tools as possible to make the coding easier (because why add filters when the website does that for you)
Wait tells selenium to stop all actions for up to 20 seconds, before carrying on - in this program it is used to wait until the accept cookies button can be clickable.
Data is the list that stores the found information.
SeenLinks is a set that stores all the information we have previously found, so we get no duplicates - we use a set as it is quicker to check for duplicates than other data structures such as lists.
`include_keywords` and `exclude_keywords` are words that we either want in the products or do not want in the products, this allows us to filter out trousers or buttoned shirts, more than is just possible in the native filtering.
marker is the point we use to tell where the generated content in the html file begins, this allows us to add style sheets and titles that wouldn't be feasable (or efficient) if we had to re-generate the content each time.
website is the name of the html file, this is used to send the link in the whatsapp message - as the filePath isn't available to access the file on the internet.
date is the current date

We then open the html file to read and then reads the lines in the file, adding them to kept lines list. For each line if the marker is in the line we break so that any line before the marker is in kept lines.

Then we open the html file to write and write the lines to the file, effectivley replacing the old lines with the same ones.

The html file is opened in "append mode" so that the file has new information added to the end without rewriting the old file. We use the date module to add a div into the file stating when the last update was.

We then try to open the vintedItems csv file, going through each line and, splitting the information at the "@" symbol, define link as the second variable and add these links to the seen_links. If there is no file found then one is created.

We wait until the accept cookies button is available to be pressed, and then clicks it using `cookies.click()` after this has happened we sleep the program for 2 seconds - to make the bot appear more human-like. we print("1A") to show where the program has got to. 

we use the line: `driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")` to scroll to the bottom of the webpage, this ensures that all the html content has been loaded.

If there are items on the page we wait until the CSS selector ".new-item-box__image-container" appears on the page, and for these items we get the link as the CSS selector "a" with the attribute href, the image as the element with the CSS selector "img" image_url is the img element with the attribute src or data_scr, this will be used to display the image on the website. Title is then defined as the alternative words for the image (for when the image cannot be displayed). we then loop through all the words in all the links, making sure they contain the `include_keywords` and if it does, then ensures the words do not contain the `exclude_keywords` we use the links as they already take the words and format them to lowercase so I don't have to do it. Finally if the link is not in `seen_links` the link gets added to `seen_links` and appended to `data`. If no items are found we print that, so we can use this information for debugging later.

Then, for each variable in data (they have to be in order as python doesn't actually know anything about the file, it treats these variables as new ones where title links to title in data, otherwise we as humans forget title doesn't actually mean title and uses it incorrectly) we open the csv, write the title, link and image into the file - using "@" as a delimiter as its the only character I could see not already used - and then save it. We then open the html file and write a div using the title, image_url and link so it actually shows all the products.

we then send the website link to the phone number given in the .env.

Hello is then printed to show we've reached the end and `input("Press Enter to close the browser...")` ensures the browser can stay open long enough to figure out what went wrong when it inevitably does (for me as the developer at least) - you can remove it. 

## InstagramScraper