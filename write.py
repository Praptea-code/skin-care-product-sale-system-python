'''this file handles all writing operations
saving sell bills, restock invoices and updating products.txt'''

import datetime
import os

#getting the base directory so file paths always work no matter where the app is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.txt")

#creating a bills folder to store all bill files
BILLS_DIR = os.path.join(BASE_DIR, "bills")
os.makedirs(BILLS_DIR, exist_ok=True)


def save_products(products):
    """
    Saves the updated product data back to products.txt
    Uses a temp file first to avoid corrupting the original if something goes wrong
    Args: products (dict) the updated product dictionary
    """
    #writing to a temp file first then renaming it to avoid data corruption
    temp = PRODUCTS_FILE + ".tmp"
    file = open(temp, "w")
    for prod in products.values():
        #converting back to original price before saving (removing the 200% markup)
        original_price = int(int(prod[3]) / 2)
        line = prod[0] + "," + prod[1] + "," + prod[2] + "," + str(original_price) + "," + prod[4] + "\n"
        file.write(line)
    file.close()
    #atomically replacing the old file with the new one
    os.replace(temp, PRODUCTS_FILE)


def save_sell_bill(name, phone, items, shipping, vat, final_total, grand_total):
    """
    Generates and saves a customer bill as a .txt file
    Args:
        name (str) customer name
        phone (str) customer phone number
        items (list) list of purchased items
        shipping (int) shipping cost
        vat (int) vat amount
        final_total (int) final total after vat and shipping
        grand_total (int) total before vat
    Returns: path (str) full path to bill file, filename (str) just the file name
    """
    #getting current date and time for the bill
    now = datetime.datetime.now()
    bill_time = str(now)
    #creating a unique bill filename using customer name, phone and timestamp
    ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "bill_" + name + "_" + phone + "_" + ts + ".txt"
    path = os.path.join(BILLS_DIR, filename)

    #opening the bill file in write mode
    file = open(path, "w")
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
    #writing each purchased item
    for item in items:
        file.write("\t" + item[0] + "\t\t" + str(item[1]) + "\t" + str(item[4]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\n")
    file.write("-" * 75 + "\n")
    file.write("\n")
    file.write("\tGrand Total:\t\t\t\tRs " + str(grand_total) + "\n")
    file.write("\tVAT (13%):\t\t\t\tRs " + str(vat) + "\n")
    #only writing shipping cost if shipping was requested
    if shipping > 0:
        file.write("\tShipping Cost:\t\t\t\tRs " + str(shipping) + "\n")
    file.write("\tFinal Total:\t\t\t\tRs " + str(final_total) + "\n")
    file.write("\n")
    file.write("=" * 75 + "\n")
    file.write("\n")
    file.write("\tTHANK YOU FOR VISITING, Do visit again! :)\n")
    file.write("\n")
    file.write("=" * 75 + "\n")
    file.close()
    return path, filename


def save_restock_bill(items, subtotal, vat, grand_total):
    """
    Generates and saves a restock invoice as a .txt file
    Args:
        items (list) list of restocked items
        subtotal (int) total before vat
        vat (int) vat amount
        grand_total (int) total after vat
    Returns: path (str) full path to invoice file, filename (str) just the file name
    """
    #getting current date and time for the invoice
    now = datetime.datetime.now()
    buy_time = str(now)
    #creating a unique invoice filename using timestamp
    ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "restock_" + ts + ".txt"
    path = os.path.join(BILLS_DIR, filename)

    #opening the invoice file in write mode
    file = open(path, "w")
    file.write("=" * 60 + "\n")
    file.write("\tWeCare Wholesale Restock Invoice - Kathmandu\n")
    file.write("=" * 60 + "\n")
    file.write("\tDate and Time: " + buy_time + "\n")
    file.write("-" * 60 + "\n")
    file.write("\tProduct\t\tQty\tPrice\tTotal\n")
    file.write("-" * 60 + "\n")
    #writing each restocked item
    for item in items:
        file.write("\t" + item[0] + "\t" + str(item[1]) + "\t" + str(item[2]) + "\t" + str(item[3]) + "\n")
    file.write("-" * 60 + "\n")
    file.write("\tSubtotal:\t\t\t" + str(subtotal) + "\n")
    file.write("\tVAT (13%):\t\t\t" + str(vat) + "\n")
    file.write("\tGrand Total:\t\t\t" + str(grand_total) + "\n")
    file.write("=" * 60 + "\n")
    file.write("\tRestock complete, Ready for sales!\n")
    file.write("=" * 60 + "\n")
    file.close()
    return path, filename
