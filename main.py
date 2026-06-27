import streamlit as st
from read import load_products
from operation import handle_dashboard_page, handle_sell_page, handle_restock_page, handle_view_page

st.set_page_config(page_title="WeCare Wholesale", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background-color: #fdf8f8 !important;
}
.block-container {
    padding: 2rem 3rem !important;
    max-width: 1200px !important;
}

/* ---- sidebar ---- */
section[data-testid="stSidebar"] {
    background-color: #fff5f5 !important;
    border-right: 1px solid #f2dfdf !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 2rem 1.5rem 1rem !important;
}
.sidebar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: #b84c55;
    letter-spacing: -0.5px;
}
.sidebar-sub {
    font-size: 0.76rem;
    color: #c9a0a5;
    line-height: 1.6;
    margin-top: 4px;
    margin-bottom: 1.5rem;
}
.sidebar-divider {
    border: none;
    border-top: 1px solid #eecfcf;
    margin: 0 0 1.2rem;
}
section[data-testid="stSidebar"] .stRadio > label { display: none !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    gap: 0.2rem !important;
    display: flex !important;
    flex-direction: column !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label {
    display: flex !important;
    align-items: center !important;
    padding: 0.65rem 1rem !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: #7a4a4a !important;
    background: transparent !important;
    border: none !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    margin: 0 !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label p,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label span {
    color: #7a4a4a !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    visibility: visible !important;
    opacity: 1 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover {
    background: #fde8e8 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover > div,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover p,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:hover span {
    color: #b84c55 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) {
    background: #f5c6c8 !important;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) > div,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) p,
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label:has(input:checked) span {
    color: #8b2e35 !important;
    font-weight: 600 !important;
}
section[data-testid="stSidebar"] .stRadio input[type="radio"] { display: none !important; }
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div:first-child { display: none !important; }

/* ---- page typography ---- */
.page-title {
    font-size: 2rem;
    font-weight: 700;
    color: #2a1515;
    letter-spacing: -0.5px;
    margin-bottom: 0.25rem;
}
.page-subtitle {
    font-size: 0.95rem;
    color: #b09095;
    margin-bottom: 1.8rem;
}
.section-label {
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #c4959b;
    margin-bottom: 0.5rem;
    margin-top: 1.2rem;
}

/* ---- fix st.container(border=True) styling ---- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff !important;
    border: 1.5px solid #f2dede !important;
    border-radius: 16px !important;
    box-shadow: 0 2px 10px rgba(184,76,85,0.05) !important;
    padding: 1.4rem 1.6rem !important;
    margin-bottom: 1.2rem !important;
}

/* ---- fix ALL input labels to be visible ---- */
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stCheckbox label,
.stToggle label,
label[data-testid="stWidgetLabel"],
label[data-testid="stWidgetLabel"] p {
    color: #5a3535 !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    visibility: visible !important;
    opacity: 1 !important;
}

/* ---- inputs ---- */
.stTextInput input, .stNumberInput input {
    border-radius: 10px !important;
    border: 1.5px solid #eedede !important;
    background: #ffffff !important;
    font-size: 0.92rem !important;
    color: #2a1515 !important;
    padding: 0.5rem 0.8rem !important;
}
.stTextInput input::placeholder {
    color: #c4959b !important;
    opacity: 1 !important;
}
.stTextInput input:focus, .stNumberInput input:focus {
    border-color: #b84c55 !important;
    box-shadow: 0 0 0 3px rgba(184,76,85,0.08) !important;
}
.stSelectbox > div > div {
    border-radius: 10px !important;
    border: 1.5px solid #eedede !important;
    background: #ffffff !important;
    font-size: 0.92rem !important;
    color: #2a1515 !important;
}

/* ---- stat boxes ---- */
.stat-box {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    border: 1px solid #f2dede;
    box-shadow: 0 2px 8px rgba(184,76,85,0.04);
}
.stat-value {
    font-size: 2.6rem;
    font-weight: 700;
    color: #2a1515;
    line-height: 1.1;
    margin-bottom: 6px;
}
.stat-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #c4959b;
}
.stat-box.alert-active { border-color: #f5c6c8; background: #fffafa; }
.stat-box.alert-active .stat-value { color: #b84c55; }

/* ---- pills ---- */
.free-badge {
    display: inline-block;
    background: #e6f7ed;
    color: #1e6b3e;
    border-radius: 20px;
    padding: 0.4rem 1.1rem;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.5rem 0 1rem 0;
    border: 1px solid #c8ebd5;
}
.low-pill {
    display: inline-block;
    background: #fde8e8;
    color: #b84c55;
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 500;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
    border: 1px solid #fcdada;
}

/* ---- totals grid ---- */
.totals-grid {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.total-item {
    flex: 1;
    min-width: 130px;
    background: #fff8f8;
    border: 1px solid #f5e2e2;
    border-radius: 14px;
    padding: 1.1rem;
    text-align: center;
}
.total-val { font-size: 1.3rem; font-weight: 700; color: #8b2e35; }
.total-lbl {
    font-size: 0.75rem;
    color: #b09095;
    margin-top: 5px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
}
.total-item.highlight { background: #b84c55; border-color: #b84c55; }
.total-item.highlight .total-val { color: #ffffff; }
.total-item.highlight .total-lbl { color: #f2dede; }

/* ---- bill box ---- */
.bill-box {
    background: #faf5f5;
    border: 1px solid #eedede;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'Courier New', monospace;
    font-size: 0.82rem;
    color: #443335;
    white-space: pre;
    overflow-x: auto;
    line-height: 1.7;
}

/* ---- buttons ---- */
.stButton > button {
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.15s ease !important;
    border: none !important;
}
.stButton > button[kind="primary"] {
    background: #b84c55 !important;
    color: #ffffff !important;
    box-shadow: 0 2px 8px rgba(184,76,85,0.2) !important;
}
.stButton > button[kind="primary"]:hover { background: #9e3d45 !important; }
.stButton > button[kind="secondary"] {
    background: #ffffff !important;
    border: 1.5px solid #f2dede !important;
    color: #b07070 !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #b84c55 !important;
    color: #b84c55 !important;
    background-color: #fffafa !important;
}
.stDownloadButton > button {
    border-radius: 10px !important;
    background: #ffffff !important;
    border: 1.5px solid #f2dede !important;
    color: #b07070 !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.6rem !important;
}
.stDownloadButton > button:hover {
    border-color: #b84c55 !important;
    color: #b84c55 !important;
}

/* ---- dataframe ---- */
.stDataFrame > div {
    border-radius: 12px !important;
    border: 1px solid #f2dede !important;
    overflow: hidden !important;
}

/* ---- misc ---- */
.stCheckbox label p, .stToggle label p {
    font-size: 0.92rem !important;
    color: #5a3535 !important;
}

/* ---- misc ---- */
.stCheckbox label p {
    font-size: 0.92rem !important;
    color: #5a3535 !important;
}
/* checkbox accent color */
.stCheckbox input[type="checkbox"]:checked {
    background-color: #b84c55 !important;
    border-color: #b84c55 !important;
}
.stCheckbox input[type="checkbox"] {
    border: 2px solid #c4959b !important;
    border-radius: 4px !important;
}
.stSuccess > div {
    background: #f0faf4 !important;
    border: 1px solid #ccebda !important;
    border-radius: 10px !important;
    color: #1a5332 !important;
    font-size: 0.92rem !important;
}
.stError > div {
    background: #fff5f5 !important;
    border: 1px solid #fcdada !important;
    border-radius: 10px !important;
    color: #b84c55 !important;
    font-size: 0.92rem !important;
}

.info-chip {
    background: #fff8f8;
    border: 1px solid #f2dede;
    border-radius: 10px;
    padding: 0.5rem 0.9rem;
    font-size: 0.88rem;
    color: #5a3535;
    margin-bottom: 0.8rem;
    display: inline-block;
    width: 100%;
}
.info-chip strong { color: #b84c55; }
.info-chip.promo {
    background: #e6f7ed;
    border-color: #c8ebd5;
    color: #1e6b3e;
}
.info-chip.promo strong { color: #1e6b3e; }

#MainMenu, footer, header { visibility: hidden !important; }
</style>
""", unsafe_allow_html=True)


def main():
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

    products = st.session_state.products

    st.sidebar.markdown('<div class="sidebar-brand">WeCare</div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div class="sidebar-sub">Sinamangal, Kathmandu<br>Managed by Praptiiii</div>',
        unsafe_allow_html=True
    )
    st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

    page = st.sidebar.radio(
        "",
        ["Dashboard", "Sell Products", "Restock Products", "View Products"],
        index=0
    )

    if page == "Dashboard":
        handle_dashboard_page(products)
    elif page == "Sell Products":
        handle_sell_page(products)
    elif page == "Restock Products":
        handle_restock_page(products)
    elif page == "View Products":
        handle_view_page(products)

main()