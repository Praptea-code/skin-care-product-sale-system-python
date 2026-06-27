'''this file handles all writing operations
saving sell bills, restock invoices and updating products.txt'''

import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_FILE = os.path.join(BASE_DIR, "products.txt")
BILLS_DIR = os.path.join(BASE_DIR, "bills")
os.makedirs(BILLS_DIR, exist_ok=True)


def save_products(products):
    temp = PRODUCTS_FILE + ".tmp"
    file = open(temp, "w")
    for prod in products.values():
        original_price = int(int(prod[3]) / 2)
        line = prod[0] + "," + prod[1] + "," + prod[2] + "," + str(original_price) + "," + prod[4] + "\n"
        file.write(line)
    file.close()
    os.replace(temp, PRODUCTS_FILE)


def save_sell_bill(name, phone, items, shipping, vat, final_total, grand_total):
    now = datetime.datetime.now()
    bill_time = now.strftime("%d %B %Y, %I:%M %p")
    ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "bill_" + name + "_" + phone + "_" + ts + ".txt"
    path = os.path.join(BILLS_DIR, filename)

    W = 52  # receipt width

    def line(char="-"):
        return char * W + "\n"

    def center(text):
        return text.center(W) + "\n"

    def row(label, value, indent=2):
        space = W - indent - len(label) - len(value)
        return " " * indent + label + " " * max(1, space) + value + "\n"

    file = open(path, "w")
    file.write(line("="))
    file.write(center("W E C A R E   W H O L E S A L E"))
    file.write(center("Sinamangal, Kathmandu"))
    file.write(line("="))
    file.write("\n")
    file.write(row("Customer:", name))
    file.write(row("Phone:", phone))
    file.write(row("Date:", bill_time))
    file.write("\n")
    file.write(line("-"))
    file.write(f"  {'ITEM':<20} {'QTY':>4}  {'FREE':>4}  {'PRICE':>7}  {'TOTAL':>7}\n")
    file.write(line("-"))
    for item in items:
        name_col = item[0][:20]
        file.write(f"  {name_col:<20} {item[1]:>4}  {item[4]:>4}  {item[2]:>7}  {item[3]:>7}\n")
    file.write(line("-"))
    file.write("\n")
    file.write(row("Subtotal:", f"Rs {grand_total:,}"))
    file.write(row("VAT (13%):", f"Rs {vat:,}"))
    if shipping > 0:
        file.write(row("Shipping:", f"Rs {shipping:,}"))
    file.write(line())
    file.write(row("TOTAL PAYABLE:", f"Rs {final_total:,}"))
    file.write(line())
    file.write("\n")
    file.write(center("Thank you for shopping at WeCare!"))
    file.write(center("Please visit again :)"))
    file.write("\n")
    file.write(line("="))
    file.close()
    return path, filename


def save_restock_bill(items, subtotal, vat, grand_total):
    now = datetime.datetime.now()
    buy_time = now.strftime("%d %B %Y, %I:%M %p")
    ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = "restock_" + ts + ".txt"
    path = os.path.join(BILLS_DIR, filename)

    W = 52

    def line(char="-"):
        return char * W + "\n"

    def center(text):
        return text.center(W) + "\n"

    def row(label, value, indent=2):
        space = W - indent - len(label) - len(value)
        return " " * indent + label + " " * max(1, space) + value + "\n"

    file = open(path, "w")
    file.write(line("="))
    file.write(center("W E C A R E   R E S T O C K   I N V O I C E"))
    file.write(center("Sinamangal, Kathmandu"))
    file.write(line("="))
    file.write(row("Date:", buy_time))
    file.write("\n")
    file.write(line("-"))
    file.write(f"  {'PRODUCT':<20} {'QTY':>4}  {'PRICE':>7}  {'TOTAL':>7}\n")
    file.write(line("-"))
    for item in items:
        name_col = item[0][:20]
        file.write(f"  {name_col:<20} {item[1]:>4}  {item[2]:>7}  {item[3]:>7}\n")
    file.write(line("-"))
    file.write("\n")
    file.write(row("Subtotal:", f"Rs {subtotal:,}"))
    file.write(row("VAT (13%):", f"Rs {vat:,}"))
    file.write(line())
    file.write(row("TOTAL PAYABLE:", f"Rs {grand_total:,}"))
    file.write(line())
    file.write("\n")
    file.write(center("Restock complete. Ready for sales!"))
    file.write("\n")
    file.write(line("="))
    file.close()
    return path, filename