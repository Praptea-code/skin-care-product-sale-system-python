"""
This file handles all the business logic for the streamlit app
displaying product tables, building cart data, calculating totals
"""

import streamlit as st
import pandas as pd
from write import save_sell_bill, save_restock_bill, save_products
from read import load_products


def get_product_table(products, use_original_price=False, show_status=False):
    rows = []
    for pid, p in products.items():
        price = int(int(p[3]) / 2) if use_original_price else int(p[3])
        stock = int(p[2])
        row = {
            "ID": pid,
            "Product": p[0],
            "Brand": p[1],
            "Stock": stock,
            "Price (Rs)": price,
            "Origin": p[4],
        }
        if show_status:
            row["Status"] = "Low Stock" if stock < 20 else "In Stock"
        rows.append(row)
    return pd.DataFrame(rows)


def show_table(df, show_status=False):
    def style_status(val):
        if val == "Low Stock":
            return "background-color:#fde8e8; color:#b84c55; font-weight:600;"
        elif val == "In Stock":
            return "background-color:#e6f7ed; color:#1e6b3e; font-weight:600;"
        return ""

    styled = df.style.set_properties(**{
        'background-color': '#ffffff',
        'color': '#2a1515',
        'font-size': '0.88rem',
    }).set_table_styles([
        {'selector': 'thead th', 'props': [
            ('background-color', '#4a1a1a'),
            ('color', '#ffffff'),
            ('font-size', '0.75rem'),
            ('font-weight', '700'),
            ('text-transform', 'uppercase'),
            ('letter-spacing', '0.08em'),
            ('padding', '0.75rem 1rem'),
        ]},
        {'selector': 'tbody tr:hover td', 'props': [
            ('background-color', '#fffaf8'),
        ]},
        {'selector': 'tbody td', 'props': [
            ('padding', '0.75rem 1rem'),
            ('border-bottom', '1px solid #fdf5f5'),
        ]},
    ])

    if show_status and "Status" in df.columns:
        styled = styled.map(style_status, subset=["Status"])

    st.dataframe(styled, use_container_width=True, hide_index=True)


def show_totals(subtotal, vat_amount, final_total, shipping=0):
    """Renders the totals summary using st.columns instead of raw HTML."""
    st.write("")
    cols = [1, 1, 1]
    if shipping:
        cols = [1, 1, 1, 1]

    if shipping:
        c1, c2, c3, c4 = st.columns(cols)
    else:
        c1, c2, c3 = st.columns(cols)

    c1.markdown(f"""
        <div class="total-item">
            <div class="total-val">Rs {subtotal:,}</div>
            <div class="total-lbl">Subtotal</div>
        </div>
    """, unsafe_allow_html=True)

    c2.markdown(f"""
        <div class="total-item">
            <div class="total-val">Rs {vat_amount:,}</div>
            <div class="total-lbl">VAT (13%)</div>
        </div>
    """, unsafe_allow_html=True)

    if shipping:
        c3.markdown(f"""
            <div class="total-item">
                <div class="total-val">Rs {shipping:,}</div>
                <div class="total-lbl">Shipping</div>
            </div>
        """, unsafe_allow_html=True)
        c4.markdown(f"""
            <div class="total-item highlight">
                <div class="total-val">Rs {final_total:,}</div>
                <div class="total-lbl">Grand Total</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        c3.markdown(f"""
            <div class="total-item highlight">
                <div class="total-val">Rs {final_total:,}</div>
                <div class="total-lbl">Grand Total</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("")


def handle_dashboard_page(products):
    total_products = len(products)
    total_stock = sum(int(p[2]) for p in products.values())
    low_stock = [p[0] for p in products.values() if int(p[2]) < 20]

    st.markdown('<div class="page-title">Good day, Praptiiii!</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Here\'s what\'s happening at WeCare today.</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="stat-box"><div class="stat-value">{total_products}</div><div class="stat-label">Products Listed</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-box"><div class="stat-value">{total_stock}</div><div class="stat-label">Units in Stock</div></div>', unsafe_allow_html=True)
    alert_class = " alert-active" if low_stock else ""
    c3.markdown(f'<div class="stat-box{alert_class}"><div class="stat-value">{len(low_stock)}</div><div class="stat-label">Low Stock Items</div></div>', unsafe_allow_html=True)

    if low_stock:
        st.write("")
        pills = "".join([f'<span class="low-pill">{item}</span>' for item in low_stock])
        st.markdown(f'<div style="margin-top:0.5rem;">{pills}</div>', unsafe_allow_html=True)

    st.write("")
    st.markdown('<div class="section-label">Live Inventory Catalog</div>', unsafe_allow_html=True)
    with st.container(border=True):
        show_table(get_product_table(products, show_status=True), show_status=True)


def handle_sell_page(products):
    st.markdown('<div class="page-title">Sell Products</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Add items to the cart and generate a customer bill.</div>', unsafe_allow_html=True)

    # customer info
    st.markdown('<div class="section-label">Customer Information</div>', unsafe_allow_html=True)
    with st.container(border=True):
        col1, col2 = st.columns(2)
        name = col1.text_input("Full Name", placeholder="e.g. Sita Rai")
        phone = col2.text_input("Mobile Number", placeholder="e.g. 9841000000")

    # product selection
    st.markdown('<div class="section-label">Product Selection</div>', unsafe_allow_html=True)
    with st.container(border=True):
        show_table(get_product_table(products, show_status=True), show_status=True)
        st.write("")
        product_options = {f"{p[0]} ({p[1]})": pid for pid, p in products.items()}
        col_a, col_b = st.columns([3, 1])
        selected_label = col_a.selectbox("Choose Product", list(product_options.keys()))
        selected_id = product_options[selected_label]
        selected_prod = products[selected_id]
        stock = int(selected_prod[2])
        qty = col_b.number_input("Quantity", min_value=1, max_value=max(1, stock), value=1, step=1)

        free = qty // 3
        total_deduct = qty + free
        price = int(selected_prod[3])
        item_total = price * qty

        # info row
        ia, ib, ic = st.columns(3)
        ia.markdown(f'<div class="info-chip">Unit Price: <strong>Rs {price:,}</strong></div>', unsafe_allow_html=True)
        ib.markdown(f'<div class="info-chip">Stock Available: <strong>{stock}</strong></div>', unsafe_allow_html=True)
        if free > 0:
            ic.markdown(f'<div class="info-chip promo">Buy 3 Get 1 Free — {free} bonus item(s)</div>', unsafe_allow_html=True)

        shipping_want = st.checkbox("Apply home delivery service charges (+Rs 250)")

        can_add = total_deduct <= stock
        if not can_add:
            st.error(f"Insufficient stock. Requested: {total_deduct} (including {free} free), Available: {stock}")

        if st.button("Add to cart", type="primary", disabled=not can_add):
            st.session_state.cart.append({
                "Product": selected_prod[0],
                "Qty": qty,
                "Free Items": free,
                "Unit Price": price,
                "Total": item_total,
            })
            products[selected_id][2] = str(stock - total_deduct)
            st.success(f"{selected_prod[0]} added to cart.")
            st.rerun()

    # active cart
    if st.session_state.cart:
        st.markdown('<div class="section-label">Active Cart</div>', unsafe_allow_html=True)
        with st.container(border=True):
            show_table(pd.DataFrame(st.session_state.cart))

            subtotal = sum(i["Total"] for i in st.session_state.cart)
            shipping = 250 if shipping_want else 0
            grand_total = subtotal + shipping
            vat_amount = int(subtotal * 0.13)
            final_total = grand_total + vat_amount

            show_totals(subtotal, vat_amount, final_total, shipping)

            col_bill, col_clear, _ = st.columns([1.2, 1, 3])
            if col_bill.button("Save Bill", type="primary"):
                if not name or not phone:
                    st.error("Please enter customer name and phone number.")
                else:
                    items = [[i["Product"], i["Qty"], i["Unit Price"], i["Total"], i["Free Items"]] for i in st.session_state.cart]
                    path, fname = save_sell_bill(name, phone, items, shipping, vat_amount, final_total, grand_total)
                    save_products(products)
                    with open(path, "r") as file:
                        st.session_state.bill_text = file.read()
                    st.session_state.bill_fname = fname
                    st.session_state.cart = []
                    st.success("Bill saved successfully.")
                    st.rerun()
            if col_clear.button("Clear cart"):
                st.session_state.products = load_products()
                st.session_state.cart = []
                st.rerun()

    # receipt
    if st.session_state.bill_text:
        st.markdown('<div class="section-label">Customer Receipt</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.code(st.session_state.bill_text, language=None)
            st.download_button("Download Receipt", data=st.session_state.bill_text, file_name=st.session_state.bill_fname, mime="text/plain")


def handle_restock_page(products):
    st.markdown('<div class="page-title">Restock Products</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Order from the manufacturer and update stock levels.</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">Manufacturer Base Rates</div>', unsafe_allow_html=True)
    with st.container(border=True):
        show_table(get_product_table(products, use_original_price=True))
        st.write("")
        product_options = {f"{p[0]} ({p[1]})": pid for pid, p in products.items()}
        col_a, col_b = st.columns([3, 1])
        selected_label = col_a.selectbox("Select Product", list(product_options.keys()))
        selected_id = product_options[selected_label]
        qty = col_b.number_input("Units to Restock", min_value=1, value=10, step=1)
        buy_price = int(int(products[selected_id][3]) / 2)
        item_total = buy_price * qty

        ra, rb = st.columns(2)
        ra.markdown(f'<div class="info-chip">Manufacturer Price: <strong>Rs {buy_price:,}</strong></div>', unsafe_allow_html=True)
        rb.markdown(f'<div class="info-chip">Order Total: <strong>Rs {item_total:,}</strong></div>', unsafe_allow_html=True)

        if st.button("Add to procurement list", type="primary"):
            st.session_state.restock_cart.append({
                "Product": products[selected_id][0],
                "Qty": qty,
                "Manufacturer Price": buy_price,
                "Total Cost": item_total,
                "id": selected_id,
            })
            st.success(f"{products[selected_id][0]} added to procurement list.")
            st.rerun()

    if st.session_state.restock_cart:
        st.markdown('<div class="section-label">Procurement Queue</div>', unsafe_allow_html=True)
        with st.container(border=True):
            display_rows = [{k: v for k, v in i.items() if k != "id"} for i in st.session_state.restock_cart]
            show_table(pd.DataFrame(display_rows))

            subtotal = sum(i["Total Cost"] for i in st.session_state.restock_cart)
            vat_amount = int(subtotal * 0.13)
            grand_total = subtotal + vat_amount

            show_totals(subtotal, vat_amount, grand_total)

            col_bill, col_clear, _ = st.columns([1.5, 1, 3])
            if col_bill.button("Confirm Restock", type="primary"):
                items = []
                for i in st.session_state.restock_cart:
                    pid = i["id"]
                    products[pid][2] = str(int(products[pid][2]) + i["Qty"])
                    items.append([i["Product"], i["Qty"], i["Manufacturer Price"], i["Total Cost"]])
                save_products(products)
                path, fname = save_restock_bill(items, subtotal, vat_amount, grand_total)
                with open(path, "r") as file:
                    st.session_state.restock_bill_text = file.read()
                st.session_state.restock_bill_fname = fname
                st.session_state.restock_cart = []
                st.success("Restock completed and stock updated.")
                st.rerun()
            if col_clear.button("Clear list"):
                st.session_state.restock_cart = []
                st.rerun()

    if st.session_state.restock_bill_text:
        st.markdown('<div class="section-label">Procurement Invoice</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.code(st.session_state.restock_bill_text, language=None)
            st.download_button("Download Invoice", data=st.session_state.restock_bill_text, file_name=st.session_state.restock_bill_fname, mime="text/plain")


def handle_view_page(products):
    st.markdown('<div class="page-title">Product Catalogue</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">All skin care products available at WeCare.</div>', unsafe_allow_html=True)
    price_view = st.checkbox("Show manufacturer base prices", value=False)
    st.write("")
    st.markdown('<div class="section-label">All Products</div>', unsafe_allow_html=True)
    with st.container(border=True):
        show_table(get_product_table(products, use_original_price=price_view, show_status=True), show_status=True)