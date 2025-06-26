from write import sell_bill, buy_bill
#function to display the menu for further functionality
def menu_display():
    '''Display the main menu for all possible options'''
    #printing every options
    print("-"*80)
    print("\t \t \t \t WeCare System Menu \t\t\t")
    print("-"*80)
    print("1. Sell Product")
    print("2. Restock Product")
    print("3. Display Product")
    print("4. Exit")
    print("-"*80)

#function to validate number input
def validate_choice(choice):
    """
    Validates users inputs
    Arguments: choice which is like prompt message for user input here
    Returns: int ( a valid menu option from  1 to 4 )
    """
    #looping until valid input is taken
    success=True
    while success:
        try:
            #converting the input taken into int
            number= int(input(choice))
            if 0< number <5:
                success=False
                return number
            else:
                print("Please enter a number ranging from 1-4")
        except:
            print("This is not even a number! Try Again. ")
    
#function to display products
def display_products(products, use_original_price):
    """
    displays list of all products
    Args: products( dict) the product dictionary with product ids as keys
    
    """
    print("-"*80)
    #this will be the header for our table
    print("ID \t Product \t Brand \t\t Stock \t Price \t Origin")
    print("-"*80)

    #looping each product in dictionary
    for key, value in products.items():
        print(key, end="\t")
        print(value[0], end="\t")  # Product
        print(value[1], end="\t\t")  # Brand
        print(value[2], end="\t")  # Stock
        if use_original_price:
            print(int(int(value[3]) / 2), end="\t")  # Original price
        else:
            print(value[3], end="\t")  # Doubled price
        print(value[4], end="\t")  # Origin
        print()
    print("-"*80)


#function to validate quantity while selling
def selling_quantity(quantity, stock):
    '''Validating selling quantity for buy 3 get 1 free offer
    Args: quantity(str) it takes prompt message
          stock(int) tells current available stock
    Returns: int valid quantity to be sold
    '''
    #looping until valid input
    while True:
        try:
            #quantity input converting into int
            amount= int(input(quantity))
            #lets check if the amound is greater than 0 or not
            if amount>0:
                #calculating free items for buy 3 get 1 free
                free_product = amount //3
                #total amount to deduct
                total = amount + free_product
                if total <= stock:
                    return amount
                else:
                    #printing if we dont have enough amount
                    print("Sorry we dont have enough stock")
            else:
                print("Please enter more than 0 ")
        except:
            print("This is not even a number! Try Again.")
            
#function to validate quantity for restocking/ buying from manufacturer
def buying_quantity(quantity):
    """
    Validates quantity for restocking products
    Arguments: quantity (str) prompt message for quantity input
    Returns: int (valid quantity to be restocked)
    """
    #simply checking if the input gareko number is more than 0 or not
    while True:
        try:
            amount= int(input(quantity))
            if amount >= 1:
                return amount
            else:
                print("Please enter more than 0 ")
        except:
            print("This is not even a number! Try Again.")

#function to sell products
''' handling product sales with by 3 get 1 free ofeer, shipping cost and vat'''
def sell_products(products):
    """
    Validates selling quantity for buy 3 get 1 free offer
    Arguments: quantity (str) prompt message for quantity input, stock (int) current available stock
    Returns: int (valid quantity to be sold)
    """
    print(" \n \t \t \t -Sell to Customers- ")

    #asking fro the customers name and phone number
    name= input ( "Enter customer name : ")
    phone= input ( "Enter customer phone : ")

    #creating a list to store purchased items
    items=[]

    #initializing the total bill first
    total= 0
    #initializing sell too
    sell=True

    #starting a loop for selling multiple products
    while sell == True:
        # Show available product list once per purchase attempt
        display_products(products,use_original_price=False)
        # Keep asking for a valid product ID
        valid_id = False
        while valid_id == False:
            try:
                product_id = int(input("Enter the Product ID to purchase : "))
                if product_id in products:
                    valid_id = True
                else:
                    print("Product not found, please enter a valid Product ID.")
            except ValueError:
                print("Please enter a valid Product ID number.")

                # Checking if product ID is available
        if product_id in products:
            product = products[product_id]
            product_name = product[0]
            # Check stock of that item
            stock = int(product[2])

            # Ask for the quantity from the customer and call the selling quantity function
            amount = selling_quantity("Amount : ", stock) 

            # Calculate the free items
            free = amount // 3

            # Calculate total for the item
            price = int(product[3])  # as the price is in 3rd index
            item_total = price * amount
            total += item_total

            # Letting customer know about free product
            if free > 0:
                print("OMG, " + name + "! Got " + str(free) + " free items ! (Buy 3 Get 1 Free)!")

            # Adding item details to the item list
            items.append([product[0], amount, price, item_total, free])

            # Update stocks now
            products[product_id][2] = str(stock - (amount + free))

        else:
            print("Product not found, Sorry! ")

        #asking the cutomer is they want to purchase more stuff
        more = input("Buy more? :) (y/n)").lower()
        if more !="y" and more != "yes":
            sell=False #exit the loop

    shipping_cost=0
    # Asking if the customer wants shipping
    ship = input("Do you want your products to be shipped? (Y/N): ")
    if ship.upper() == "Y":
        shipping_cost = 250 

    # Final bill amount including shipping
    grand_total = total + shipping_cost

    # calculating VAT (13%)
    vat_rate = 0.13
    vat_amount = int(total * vat_rate)

    # calculating final total including VAT
    final_total = grand_total + vat_amount

    #calling the billing function
    sell_bill(name, phone,items,shipping_cost, vat_amount, final_total,grand_total,products)


           
#Lets restock now gng lesgo buy from manufacturer
def buy_products(products):
    """
    Handles restocking by purchasing products from manufacturer
    Arguments: products (dict) dictionary with product ids as keys and product details as values
    """
    print(" \n \t \t \t Buy From Manufacturer ")
    #letem see the available prods first
    items = []  # List to store purchased items
    total = 0    # Initialize total bill amount
    
    #check if valid or not
    buy=True
    while buy==True:
        display_products(products,use_original_price=True)
        valid_id = False
        while valid_id==False:
            #getting the ids
            prod_id = buying_quantity("Enter product ID to restock: ")
            if prod_id in products:
                valid_id = True
                amount = buying_quantity("Enter quantity to add: ")
                product_name = products[prod_id][0]
                #the price
                price = int(int(products[prod_id][3])/2)
                #total price
                total_price = price * amount
                total += total_price
                #lesgo update the stock now
                products[prod_id][2] = str(int(products[prod_id][2]) + amount)
                # Save to item list
                items.append([product_name, amount, price, total_price])
                
                #if we want to buy
                more = input("Buy more? :) (y/n)").lower()
                if more != "y" and more != "yes":
                    buy = False #exit the loop
            else:
                print("Invalid id, try Again!")
        
    vat=0.13
    vat_amount= int(total * vat)
    #nowgrandtotal
    grand_total=total + vat_amount
    
    #file ma ni save garnu parne raicha tesaile invoice wala method call gardiiney
    buy_bill(items,total, vat_amount, grand_total, products) 
   
