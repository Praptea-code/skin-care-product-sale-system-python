'''we use dictionary named products to store products inside function
product id is taken as key and
product details is taken as value'''

import os

#getting the base directory so file paths always work no matter where the app is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.txt")

def load_products():
    """
    Loads product data from products.txt file
    Returns a dictionary where key is product id and value is product details
    """
    products = {}
    #opening the products.txt file in read mode
    file = open(PRODUCTS_FILE, "r")
    #reading all lines from the file
    data = file.readlines()
    #looping through each line in the file
    prod_id = 1
    for line in data:
        #stripping newline and splitting by comma, also stripping spaces from each part
        line = [part.strip() for part in line.replace("\n", "").split(",")]
        #converting the price at index 3 from string to int and applying 200% markup for sell price
        original_price = int(line[3])
        line[3] = str(original_price * 2)
        #adding updated product list to dictionary using prod_id as key
        products[prod_id] = line
        #incrementing id for next product
        prod_id = prod_id + 1
    #closing the file
    file.close()
    return products
