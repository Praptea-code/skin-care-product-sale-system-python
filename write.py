import datetime
#function for bill now
def sell_bill(name, phone,items,shipping_cost, vat_amount, final_total,grand_total,products):
    """
    Generates a bill file and prints the billing summary for customer purchases.

    Args:
        name (str) customer's name.
        phone (str) customer's phone number
        items (list) list of purchased items.
        shipping_cost (int) shipping charge
        vat_amount (int) VAT added
        final_total (int) final amount after VAT and shipping.
        grand_total (int) total before VAT.
    """
    try:
        bill_time=str(datetime.datetime.now())
        #creating billfilename
        # Create bill file name
        bill_file = "bill_" + name + "_" + phone + bill_time.replace(" ", "_").replace(":", "-")+".txt"
        # Open file in write mode, yayy!
        file = open(bill_file, "w")
        file.write("=" * 75 + "\n")
        file.write("\n")
        file.write("\tWeCare Wholesale Bill - Sinamangal, Kathmandu\n")
        file.write("\n")
        file.write("=" * 75 + "\n")
        file.write("\n")
        file.write("\tCustomer: " + name + "\t\tPhone: " + phone + "\n")
        file.write("\tDate and Time: " + bill_time + "\n")
        file.write("\n")
        file.write("-" * 75 + "\n")
        file.write("\tItem\t\tQty\tFree\tPrice\tTotal\n")
        file.write("-" * 75 + "\n")
        # Write purchased items
        for item in items:
            file.write("\t" + item[0] + "\t\t" + str(item[1]) + "\t" + str(item[4]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\n")
        file.write("-" * 75 + "\n")
        file.write("\n")
        # Write totals
        file.write("\tGrand Total:\t\t\t\tRs " + str(grand_total) + "\n")
        file.write("\tVAT (13%):\t\t\t\tRs " + str(vat_amount) + "\n")
        if shipping_cost > 0:
            file.write("\tShipping Cost:\t\t\t\tRs " + str(shipping_cost) + "\n")
        file.write("\tFinal Total:\t\t\t\tRs " + str(final_total) + "\n")
        file.write("\n")
        file.write("=" * 75 + "\n")
        file.write("\n")
        file.write("\tTHANK YOU FOR VISITING,Do visit again! :)\n")
        file.write("\n")
        file.write("=" * 75 + "\n")
        # Close file
        file.close()
        
        file = open("products.txt", "w")
        for prod in products.values():
            original_price = int(int(prod[3]) / 2)
            line = prod[0] + "," + prod[1] + "," + prod[2] + "," + str(original_price) + "," + prod[4] + "\n"
            file.write(line)
        file.close()
        
        #now printing the bill
        print("\n" + "="*60 + "\t")
        print("\tWeCare Wholesale Bill – Sinamangal, Kathmandu\t")
        print("="*60 + "\t")
        print("\tCustomer: " + name + "\tPhone: " + phone + "\t")
        print("\tDate and Time: " + bill_time + "\t")
        print("-"*60 + "\t")
        print("\tItem\t\tQty\tFree\tPrice\tTotal\t")
        print("-"*60 + "\t")
        for item in items:
            print("\t" + item[0] + "\t" + str(item[1]) + "\t" + str(item[4]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\t")
        print("-"*60 + "\t")
        print("\tGrand total:\t\t\t\t" + str(grand_total) + "\t")
        print("\tVAT (13%):\t\t\t\t" + str(vat_amount) + "\t")
        if shipping_cost > 0:
            print("\tShipping:\t\t\t\t250\t")
        print("-"*60 + "\t")
        print("\tFinal Total:\t\t\t\t" + str(final_total) + "\t")
        print("="*60 + "\t")
        print("\tBill saved as " + bill_file + "\n \n")
        
    except Exception as e:
        # Printing error if bill generation fails
        print("Error making bill, Sorry :( \t" + str(e))
                        
#function to generate buying bill from manufacturers
def buy_bill(items,total, vat_amount, grand_total,products):
    """
    Generates a restock invoice file and prints the invoice summary
    Arguments: items (list) list of restocked items, total (int) subtotal before VAT, vat_amount (int) VAT added, grand_total (int) total after VAT, products (dict) product dictionary
    Returns: none
    """
    try:
        buy_time=str(datetime.datetime.now())
        buy_bill_file="restock_bill_" + buy_time.replace(" ", "_").replace(":", "-")+".txt"
        file=open(buy_bill_file,"w")
        file.write("="*59 + "\t\n")
        file.write("\tWeCare Wholesale Restock Invoice – Kathmandu\t\n")
        file.write("="*59 + "\t\n")
        # Writing date and time
        file.write("\tDate and Time: " + buy_time + "\t\n")
        file.write("-"*59 + "\t\n")
        # Writing table header
        file.write("\tProduct\t\tQty\tPrice\tTotal\t\n")
        file.write("-"*59 + "\t\n")
        # Writing restocked product details
        for item in items:
            file.write("\t" + item[0] + "\t" + str(item[1]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\t\n")
        file.write("-"*59 + "\t\n")
        # Writing subtotal
        file.write("\tSubtotal:\t\t\t" + str(total) + "\t\n")
        # Writing VAT
        file.write("\tVAT (13%):\t\t\t" + str(vat_amount) + "\t\n")
        file.write("-"*59 + "\t\n")
        # Writing grand total
        file.write("\tGrand Total:\t\t\t" + str(grand_total) + "\t\n")
        file.write("="*59 + "\t\n")
        # Writing thank you message
        file.write("\tRestock complete, Ready for sales!\t\n")
        file.write("="*59 + "\t\n")
        # Closing invoice file
        file.close()

        #Update products.txt manually
        file = open("products.txt", "w")
        for prod in products.values():
            original_price = int(int(prod[3]) / 2)  # reverse the markup to store original price
            line = prod[0] + "," + prod[1] + "," + prod[2] + "," + str(original_price) + "," + prod[4] + "\n"
            file.write(line)
        file.close()

        
        # Printing invoice to console
        print("\n" + "="*66 + "\t")
        print("\tWeCare Wholesale Restock Invoice – Kathmandu\t")
        print("="*66 + "\t")
        print("\tDate and Time: " + buy_time + "\t")
        print("-"*66 + "\t")
        print("\tProduct\t\tQty\tPrice\tTotal\t")
        print("-"*66 + "\t")
        for item in items:
            print("\t" + item[0] + "\t" + str(item[1]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\t")
        print("-"*66 + "\t")
        print("\tSubtotal:\t\t\t" + str(total) + "\n")
        print("\tVAT (13%):\t\t\t" + str(vat_amount) + "\n")
        print("-"*66 + "\t")
        print("\tGrand Total:\t\t\t" + str(grand_total) + "\n")
        print("="*66 + "\t")
        print("\tInvoice saved as " + buy_bill_file + "\n")
    except:
        # Printing error if invoice generation fails
        print("Error making restock invoice :(")

    
