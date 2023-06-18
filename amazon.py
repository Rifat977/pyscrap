import requests
from bs4 import BeautifulSoup

URL = "https://www.amazon.in/s?k=earphone"

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}

r = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(r.content, 'html.parser')

products = soup.find_all("div", attrs={'class':"sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16"})

for product in products:
    title = product.find("span", attrs={'class':"a-size-medium a-color-base a-text-normal"})
    price = product.find("span", attrs={'class': "a-price-whole"})
    print(title.text)
    print(price.text)




# with open("amazon.html", "wb") as f:
#     f.write(soup.encode("utf-8"))
