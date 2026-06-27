'''this file handles all the business logic for the streamlit app
displaying product tables, building cart data, calculating totals'''

import streamlit as st
from write import save_sell_bill, save_restock_bill, save_products
from read import load_products


def get_product_table(products, use_original_price=False):
    """
    Builds a list of dictionaries for displaying products as a table
    Args:
        products (dict) the product dictionary with product ids as keys
        use_original_price (bool) if True shows original buy price, else shows sell price
    Returns: list of dicts ready for st.dataframe
    """
    rows = []
    #looping through each product in the dictionary
    for pid, p in products.items():
        #showing original price or doubled sell price depending on the flag
        if use_original_price:
            price = int(int(p[3]) / 2)
        else:
            price = int(p[3])
        rows.append({
            "ID": pid,
            "Product": p[0],
            "Brand": p[1],
            "Stock": int(p[2]),
            "Price (Rs)": price,
            "Origin": p[4],
        })
    return rows


def handle_sell_page(products):
    """
    Handles the entire sell products page including cart, billing and stock update
    Args: products (dict) the product dictionary with product ids as keys
    """
    st.subheader("Sell to Customer")

    #getting customer details
    col1, col2 = st.columns(2)
    name  = col1.text_input("Customer Name")
    phone = col2.text_input("Customer Phone")

    st.divider()
    st.markdown("#### Add Items to Cart")

    #showing the product table so user can see available products
    st.dataframe(get_product_table(products), use_container_width=True, hide_index=True)

    #building dropdown options from product dictionary
    product_options = {str(pid) + " - " + p[0] + " (" + p[1] + ")": pid for pid, p in products.items()}

    col_a, col_b, col_c = st.columns([3, 1, 1])
    selected_label = col_a.selectbox("Select Product", list(product_options.keys()))
    selected_id    = product_options[selected_label]
    selected_prod  = products[selected_id]
    stock          = int(selected_prod[2])

    #quantity input capped at current stock
    qty           = col_b.number_input("Quantity", min_value=1, max_value=max(1, stock), value=1, step=1)
    shipping_want = col_c.checkbox("Add Shipping? (+Rs 250)")

    #calculating free items for buy 3 get 1 free offer
    free         = qty // 3
    total_deduct = qty + free
    price        = int(selected_prod[3])
    item_total   = price * qty

    #letting user know about their free items
    if free > 0:
        st.info("Buy 3 Get 1 Free! You get " + str(free) + " free item(s). Total deducted from stock: " + str(total_deduct))

    #checking if we have enough stock including the free items
    if total_deduct > stock:
        st.error("Not enough stock! Available: " + str(stock) + ", Required (including free): " + str(total_deduct))
        can_add = False
    else:
        can_add = True

    #adding item to cart if button is clicked
    if st.button("Add to Cart", disabled=not can_add):
        st.session_state.cart.append({
            "Product": selected_prod[0],
            "Qty": qty,
            "Free": free,
            "Price": price,
            "Total": item_total,
        })
        #deducting from stock in session state immediately
        products[selected_id][2] = str(stock - total_deduct)
        st.success("Added " + selected_prod[0] + " to cart!")
        st.rerun()

    #showing cart if it has items
    if st.session_state.cart:
        st.divider()
        st.markdown("#### Cart")
        st.dataframe(st.session_state.cart, use_container_width=True, hide_index=True)

        #calculating all totals
        subtotal    = sum(i["Total"] for i in st.session_state.cart)
        shipping    = 250 if shipping_want else 0
        grand_total = subtotal + shipping
        vat_amount  = int(subtotal * 0.13)
        final_total = grand_total + vat_amount

        #displaying totals in columns
        col_x, col_y, col_z = st.columns(3)
        col_x.metric("Subtotal", "Rs " + str(subtotal))
        col_y.metric("VAT (13%)", "Rs " + str(vat_amount))
        col_z.metric("Final Total", "Rs " + str(final_total))

        col_bill, col_clear = st.columns(2)

        #generating bill when button is clicked
        if col_bill.button("Generate Bill", type="primary"):
            if not name or not phone:
                st.error("Please enter customer name and phone number.")
            else:
                #building items list in format expected by save_sell_bill
                items = [[i["Product"], i["Qty"], i["Price"], i["Total"], i["Free"]]
                         for i in st.session_state.cart]
                path, fname = save_sell_bill(name, phone, items, shipping, vat_amount, final_total, grand_total)
                #saving updated stock to products.txt
                save_products(products)
                #storing bill text in session so it can be shown and downloaded
                file = open(path, "r")
                st.session_state.bill_text  = file.read()
                st.session_state.bill_fname = fname
                file.close()
                #clearing the cart after bill is generated
                st.session_state.cart = []
                st.success("Bill generated and stock updated!")
                st.rerun()

        #clearing cart and restoring stock if user wants to start over
        if col_clear.button("Clear Cart"):
            st.session_state.products = load_products()
            st.session_state.cart = []
            st.rerun()

    #showing the last generated bill with a download button
    if st.session_state.bill_text:
        st.divider()
        st.markdown("#### Last Generated Bill")
        st.code(st.session_state.bill_text, language=None)
        st.download_button(
            "Download Bill",
            data=st.session_state.bill_text,
            file_name=st.session_state.bill_fname,
            mime="text/plain"
        )


def handle_restock_page(products):
    """
    Handles the entire restock page including restock list, invoice and stock update
    Args: products (dict) the product dictionary with product ids as keys
    """
    st.subheader("Restock from Manufacturer")
    st.caption("Prices shown below are the buy price (original, before markup).")

    #showing product table with original buy prices
    st.dataframe(get_product_table(products, use_original_price=True), use_container_width=True, hide_index=True)

    #building dropdown options from product dictionary
    product_options = {str(pid) + " - " + p[0] + " (" + p[1] + ")": pid for pid, p in products.items()}

    col_a, col_b = st.columns([3, 1])
    selected_label = col_a.selectbox("Select Product to Restock", list(product_options.keys()))
    selected_id    = product_options[selected_label]
    qty            = col_b.number_input("Quantity to Add", min_value=1, value=10, step=1)

    #calculating buy price and total for selected product
    buy_price  = int(int(products[selected_id][3]) / 2)
    item_total = buy_price * qty
    st.info("Buy price: Rs " + str(buy_price) + " x " + str(qty) + " = Rs " + str(item_total))

    #adding item to restock list if button is clicked
    if st.button("Add to Restock List"):
        st.session_state.restock_cart.append({
            "Product": products[selected_id][0],
            "Qty": qty,
            "Price": buy_price,
            "Total": item_total,
            "id": selected_id,
        })
        st.success("Added to restock list!")
        st.rerun()

    #showing restock list if it has items
    if st.session_state.restock_cart:
        st.divider()
        st.markdown("#### Restock List")
        #hiding the internal id field from the display table
        display = [{k: v for k, v in i.items() if k != "id"} for i in st.session_state.restock_cart]
        st.dataframe(display, use_container_width=True, hide_index=True)

        #calculating totals
        subtotal    = sum(i["Total"] for i in st.session_state.restock_cart)
        vat_amount  = int(subtotal * 0.13)
        grand_total = subtotal + vat_amount

        col_x, col_y, col_z = st.columns(3)
        col_x.metric("Subtotal", "Rs " + str(subtotal))
        col_y.metric("VAT (13%)", "Rs " + str(vat_amount))
        col_z.metric("Grand Total", "Rs " + str(grand_total))

        col_bill, col_clear = st.columns(2)

        #confirming restock, updating stock and generating invoice
        if col_bill.button("Confirm Restock", type="primary"):
            items = []
            for i in st.session_state.restock_cart:
                pid = i["id"]
                #adding restocked quantity to existing stock
                products[pid][2] = str(int(products[pid][2]) + i["Qty"])
                items.append([i["Product"], i["Qty"], i["Price"], i["Total"]])
            #saving updated stock to products.txt
            save_products(products)
            path, fname = save_restock_bill(items, subtotal, vat_amount, grand_total)
            #storing invoice text in session so it can be shown and downloaded
            file = open(path, "r")
            st.session_state.restock_bill_text  = file.read()
            st.session_state.restock_bill_fname = fname
            file.close()
            #clearing the restock list after invoice is generated
            st.session_state.restock_cart = []
            st.success("Restock complete and stock updated!")
            st.rerun()

        if col_clear.button("Clear List"):
            st.session_state.restock_cart = []
            st.rerun()

    #showing the last generated invoice with a download button
    if st.session_state.restock_bill_text:
        st.divider()
        st.markdown("#### Last Restock Invoice")
        st.code(st.session_state.restock_bill_text, language=None)
        st.download_button(
            "Download Invoice",
            data=st.session_state.restock_bill_text,
            file_name=st.session_state.restock_bill_fname,
            mime="text/plain"
        )


def handle_dashboard_page(products):
    """
    Handles the dashboard page showing inventory overview and all products
    Args: products (dict) the product dictionary with product ids as keys
    """
    st.subheader("Inventory Overview")

    #calculating summary stats for the dashboard
    total_products = len(products)
    total_stock    = sum(int(p[2]) for p in products.values())
    #finding products with less than 20 units in stock
    low_stock      = [p[0] for p in products.values() if int(p[2]) < 20]

    #displaying stats in three columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Products", total_products)
    col2.metric("Total Units in Stock", total_stock)
    col3.metric("Low Stock Items (less than 20)", len(low_stock))

    #warning if any products are running low
    if low_stock:
        st.warning("Low stock: " + ", ".join(low_stock))

    st.divider()
    st.subheader("All Products")
    st.dataframe(get_product_table(products), use_container_width=True, hide_index=True)


def handle_view_page(products):
    """
    Handles the view products page with a toggle between buy and sell prices
    Args: products (dict) the product dictionary with product ids as keys
    """
    st.subheader("Product Catalogue")
    #toggle to switch between buy price and sell price view
    price_view = st.toggle("Show buy price (from manufacturer)", value=False)
    st.dataframe(get_product_table(products, use_original_price=price_view), use_container_width=True, hide_index=True)
