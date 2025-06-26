#importing date and time module to get current date and time and all other modules
from operation import menu_display, validate_choice, sell_products,buy_products,display_products
from read import load_products
import datetime

'''creating a banner like structure for our system'''
#printing everything
print("\n")
print("="*80)
print("\t \t \t WeCare Wholesale,Sinamangal,Kathamandu \t")
print("\t \t \t \t Managed by Praptiiii")
print("-"*80)
print("\t \t Everyone's First Choice – Where Love Meets Quality!")
print("="*80)


#the main program
def main():
    """
    Main function to run the WeCare Wholesale system
    Loads products
    Displays menu
    handles user choices for selling, buying, or exiting
    """
    products= load_products()   
    run=True
    while run==True:
        menu_display()
        #getting users choice
        choice= validate_choice("Enter your choice (1-4) :")
        if choice ==1:
            sell_products(products)
        elif choice==2:
            buy_products(products)
        elif choice == 3:
            display_products(products,use_original_price=False)
        elif choice ==4:
            print("Thank you for using WeCare, Byebye We actually Care!")
            run=False
            
#calling the main function
main()



           
        
        
            
        
