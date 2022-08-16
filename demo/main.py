import requests
from bs4 import BeautifulSoup

html = requests.get("http://www.chemicalbook.com/Search_EN.aspx?keyword=CB5273333")

# soup = BeautifulSoup(html)

# print(soup.title)