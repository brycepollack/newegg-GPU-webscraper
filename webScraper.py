from urllib.request import urlopen as request
from bs4 import BeautifulSoup as soup
import csv
import re

#Building URL and parsing
url = 'https://www.newegg.com/Desktop-Graphics-Cards/SubCategory/ID-48'
client = request(url)
page_html = client.read()
client.close()
page_soup = soup(page_html, 'html.parser')
containers = page_soup.findAll("div", {"class":"item-container"})

#Creates CSV
filename = "graphicscards.csv"
f = open(filename, "w")
headers = "Brand, Product, Price, Shipping\n"
f.write(headers)

#For loop for data retrieval
for container in containers:
    #Grabs brand name
    brand = container.div.div.a.img['title']
    
    #Grabs product name
    productContainer = container.findAll("a", {"class":"item-title"})
    product = productContainer[0].text.strip()
    
    #Grabs shipping cost
    shippingContainer = container.findAll("li", {"class":"price-ship"})
    shipping = shippingContainer[0].text.strip()
    
    #Grabs product price by finding container, grabbing text, cleaning text
    priceContainer = container.findAll("li", {"class":"price-current"})
    price = priceContainer[0].text.strip()
    cleanObject = re.search(r"\$[\d,.]*", price)
    cleanPrice = cleanObject.group()
    
    #Prints to console
    print("Brand:  " + brand)
    print("Product:  " + product)
    print("Price:  " + cleanPrice)
    print("Shipping Cost:  " + shipping)
    
    #Writes to csv, replaces commas with content
    f.write(brand + "," + product.replace(",", "|") + "," + cleanPrice.replace(",", "") + "," + shipping + "\n")
f.close()
