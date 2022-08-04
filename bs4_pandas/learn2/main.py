from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests

res = requests.get("http://www.beatstars.com/explore-tracks")
# b_data = BeautifulSoup(html_data, "html.parser")

# x = b_data.find_all('div')
print(res.text)

# products = b_data.find_all(['article'], class_="product_pod")
# price = b_data.find_all(['p'], class_="price_color")
# images = b_data.find_all(['div'], class_="image_container")

# filename = "output.csv"
# f = open(filename, "w")
# headers = "Name, Price, Image\n"
# f.write(headers)

# product_name = []
# product_price = []
# product_images = []

# for p_name in products:
#     product_name.append(p_name.h3.a.text)

# for p_price in price:
#     product_price.append(p_price.string)

# for p_image in images:
#     product_images.append("https://books.toscrape.com/"+p_image.img['src'])

# for i,j,k in zip(product_name, product_price, product_images):
#     f.write(i + "," + j + "," + k + "\n")
# f.close()
