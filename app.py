import streamlit as st
from utils import StockAPI

# Intiliaze a blank web app
st.set_page_config(page_title="Stock market project", layout="wide")


# Load the stock api and store it in cache (temporary memory)
@st.cache_resource
def get_stock_client():
    return StockAPI()


client = StockAPI()

@st.cache_data(ttl=3600)
def get_company_symbols(company: str):
    return client.get_symbols(company)

@st.cache_data(ttl=3600)
def get_stock_data(symbol: str):
    return client.get_daily_prices(symbol)

# Show the title for web app
st.title("Stock Market Project")
st.subheader("by Utkarsh Gaikwad")

# Take a company name as input from user
company = st.text_input("Enter the company name : ")

if company:
    # search_df = client.get_symbols(company)
    search_df = get_company_symbols(company)
    symbols = search_df["1. symbol"].tolist()
    # Dropdown of symbols
    sel_symbol = st.selectbox("Select the symbol", options=symbols)
    sel_df = search_df[search_df["1. symbol"] == sel_symbol]
    st.dataframe(sel_df)
    # Add a button to plot chart
    button = st.button("Plot Chart", type="primary")
    # If the button is pressed then load the dataframe from the api
    if button:
        # stock_df = client.get_daily_prices(sel_symbol)
        stock_df = get_stock_data(sel_symbol)
        st.dataframe(stock_df.head())
        fig = client.plot_candlestick(stock_df)
        st.plotly_chart(fig)
