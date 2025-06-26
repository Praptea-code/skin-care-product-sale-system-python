''' we use dictionary named product to store products inside function
product id is taken as key and
product details is taken as value'''

def load_products():
    """
    Loads product data from "product.txt" file
    Returns a dictionary where key is product id  value are product details
    """
    products={}
    #open file product.txt file in read mode
    file=open("products.txt","r")
    #read all the lines from the file
    data=file.readlines()
    #looping through each line in file
    prod_id=1
    for line in data:
        #replacing the new line character and spliting the line by commas
        line = line.replace("\n","").split(",")
        #convert the price which is in index 3 from string to integer
        original_price = int(line[3])
        #replacing the original price with 200%markup
        line[3] = str(original_price * 2)
        #adding the updated product list to the dictionary products using prod_id as the key
        products[prod_id]=line
        #increment id for next item
        prod_id=prod_id+1
    #closing the file
    file.close()
    return products
