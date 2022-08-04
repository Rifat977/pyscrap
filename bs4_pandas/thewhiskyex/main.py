from bs4 import BeautifulSoup
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.thewhiskyexchange.com"

headers = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}

productLinks = []

for i in range(1,2):
    res = requests.get("https://www.thewhiskyexchange.com/specialoffers?pg="+str(i)+"#productlist-filter", headers=headers)
    soup = BeautifulSoup(res.content, "html.parser")
    
    productList = soup.find_all('div', class_="item")    
    for item in productList:
        for link in item.find_all('a', href=True):
            productLinks.append(url+link['href'])

allProduct = []

for link in productLinks:
    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')

    try:
        name = soup.find('h1', class_="product-main__name").text.strip()
    except:
        name = 'no name'
    try:
        rating = soup.find('div', class_="review-overview__rating").text.strip()
    except:
        rating = 'no rating'
    try:
        reviews = soup.find('span', class_="review-overview__count").text.strip()
    except:
        reviews = 'no reviews'
    try:
        price = soup.find('p', class_="product-action__price").text.strip()
    except:
        price = 'no price'
    product = {
        'name':name,
        'rating':rating,
        'reviews': reviews,
        'price':price
    }
    allProduct.append(product)
    print('Saving:', product['name'])

data = pd.DataFrame(allProduct)
# print(data.head(15))
data.to_csv('products.csv', index=False)