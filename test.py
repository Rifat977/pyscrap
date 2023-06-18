import requests
from bs4 import BeautifulSoup

# Define the search query
search_query = 'laptop'

# Construct the Flipkart URL
url = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&sort=price_asc'

# Send an HTTP request to the URL
response = requests.get(url)

# Parse the response content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the product div elements
products = soup.find_all('div', {'class': '_2kHMtA'})

# Loop through the product div elements and print the details
for product in products:
    # Get the product title
    title = product.find('div', {'class': '_4rR01T'}).text
    
    # Get the product price
    price = product.find('div', {'class': '_30jeq3 _1_WHN1'}).text
    
    # Get the product rating
    rating = product.find('div', {'class': '_3LWZlK'}).text
    
    # Print the product details
    print('Title:', title)
    print('Price:', price)
    print('Rating:', rating)
    print('-------------------------------')
