# webscraper

## Contents:

[Main.py](#Mainpy)

[vinted Scraper](#vintedscraper)

[Instagram Scraper](#instagramscraper)

## Main.py

Main.py is a scraper for oceanhero, the weird browser that I choose to force myself to put up with *but think of the turtles!* -yeah sure. Anyway, it scrapes the page looking for images of a person holding up one finger - and then returns a csv file containing all of these images - this was for a machine learning project I was attempting before I realised that my laptop wouldn't be able to handle all of the compute power required. But here is the code anyway:

### Code:

We first import a bunch of modules, these are: pandas - for formatting the data that gets written to the csv, beautiful soup - for reading the html processed by selenium, selenium - for opening the webpage and waiting for all the html to load, dotenv - which is used to load the .env file and os - to actually get the .env variables.

We then use the dotenv module to `load_dotenv()` which sets up the .env file to be set as variables, this is how we get the service path using `os.getenv("servicePath")` and the os module.

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

## InstagramScraper