# WeCare Wholesale Inventory System

## Overview
WeCare Wholesale is a console-based inventory management system for a fictional wholesale store in Sinamangal, Kathmandu, managed by Prapti. The system enables efficient management of product sales, restocking, and inventory display, featuring a "Buy 3 Get 1 Free" offer, VAT calculations, and bill generation. Built with Python, it uses text files for data persistence, offering a simple and effective solution for inventory operations.

## Features

- **Menu-Driven Interface**: Provides options to sell products, restock inventory, display products, or exit the system.

- **Product Sales**:
  - Supports sales with a "Buy 3 Get 1 Free" offer.
  - Calculates 13% VAT and optional shipping costs (Rs. 250).
  - Generates detailed bills saved as text files and displayed in the console.

- **Restocking**:
  - Enables purchasing products from manufacturers at original prices (half of selling price).
  - Updates stock levels and generates restock invoices.

- **Product Display**:
  - Displays a table of products with ID, name, brand, stock, price, and origin.
  - Shows doubled prices for sales and original prices for restocking.
- **Data Persistence**:
  - Reads product data from products.txt.
  - Updates products.txt after transactions to reflect current stock.
- **Input Validation**:
  - Ensures valid numeric inputs for menu choices, product IDs, and quantities.
  - Prevents overselling by checking stock availability.

## Technologies Used
- **Python 3**: Core language for application logic.
- **File I/O**: Manages product data and bill/invoice generation via text files.
- **Standard Libraries**:
- **datetime**: For timestamping bills and invoices.
- **Modular Design**: Separates functionality into operation.py, read.py, and write.py for better organization.

## File Structure
```plaintext
├── products.txt          # Text file storing product data (e.g., Vitamin C Serum, Garnier, 121, 3000, France)
├── operation.py          # Main script with menu, validation, and core sale/restock functions
├── read.py               # Contains load_products() to read product data from products.txt
├── write.py              # Contains sell_bill() and buy_bill() for generating bills and invoices
└── README.md             # Project documentation
```
## Usage
- **Navigation**: Interact with the system via the console menu, selecting options 1–4.
- **Sell Product**: Enter customer name, phone, product IDs, and quantities; choose shipping to generate a bill with the "Buy 3 Get 1 Free" offer.
- **Restock Product**: Select product IDs and quantities to restock, generating an invoice with costs at original prices.
- **Display Product**: View a table of all products, showing selling prices (doubled) or original prices (for restocking).

## Output Files:
- Sales generate bill files (e.g., bill_John_1234567890_2025-07-09_12-52-45.txt).
- Restocking generates invoice files (e.g., restock_bill_2025-07-09_12-52-45.txt).
- products.txt is updated after each transaction.
