#importing streamlit and all modules
import streamlit as st
from read import load_products
from operation import handle_dashboard_page, handle_sell_page, handle_restock_page, handle_view_page

#setting up the page with title and wide layout
st.set_page_config(page_title="WeCare Wholesale", layout="wide")

#creating a banner like structure for our system using html and css
st.markdown("""
<style>
    .banner {
        background: linear-gradient(135deg, #f8b4d9, #fde8f0, #c9e8f5);
        border-radius: 12px;
        padding: 20px 30px;
        text-align: center;
        margin-bottom: 20px;
    }
    .banner h1 { color: #7b2d5e; margin: 0; font-size: 2rem; }
    .banner p  { color: #555; margin: 4px 0 0; font-size: 1rem; }
    div[data-testid="stMetric"] { background: #fdf4f9; border-radius: 8px; padding: 10px; }
</style>
<div class="banner">
    <h1>WeCare Wholesale</h1>
    <p>Sinamangal, Kathmandu &nbsp;|&nbsp; Managed by Praptiiii</p>
    <p><i>Everyone's First Choice - Where Love Meets Quality!</i></p>
</div>
""", unsafe_allow_html=True)


#the main function to run the WeCare Wholesale streamlit app
def main():
    """
    Main function to run the WeCare Wholesale system
    Initialises session state
    Displays sidebar menu
    Handles page routing based on user choice
    """
    #initialising session state variables on first run
    if "products" not in st.session_state:
        st.session_state.products = load_products()
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "restock_cart" not in st.session_state:
        st.session_state.restock_cart = []
    if "bill_text" not in st.session_state:
        st.session_state.bill_text = None
    if "bill_fname" not in st.session_state:
        st.session_state.bill_fname = None
    if "restock_bill_text" not in st.session_state:
        st.session_state.restock_bill_text = None
    if "restock_bill_fname" not in st.session_state:
        st.session_state.restock_bill_fname = None

    #getting products from session state
    products = st.session_state.products

    #displaying the sidebar menu for navigation
    page = st.sidebar.radio(
        "Menu",
        ["Dashboard", "Sell Products", "Restock Products", "View Products"],
        index=0
    )

    #routing to the correct page based on user choice
    if page == "Dashboard":
        handle_dashboard_page(products)
    elif page == "Sell Products":
        handle_sell_page(products)
    elif page == "Restock Products":
        handle_restock_page(products)
    elif page == "View Products":
        handle_view_page(products)


#calling the main function
main()
