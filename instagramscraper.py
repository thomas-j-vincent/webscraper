from bs4 import BeautifulSoup   
import requests

page = requests.get("https://www.instagram.com/explore/search/keyword/?q=recipes")
soup = BeautifulSoup(page.text, "html.parser")
links = soup.find_all("a",attrs={"class":"x1i10hfl"} )

for link in links:
    href = link.get("href")
    print(href)

print("hello")