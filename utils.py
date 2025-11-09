import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go


class StockAPI:

    def __init__(self):
        self.url = "https://alpha-vantage.p.rapidapi.com/query"
        self.headers = {
            "x-rapidapi-key": st.secrets["API_KEY"],
            "x-rapidapi-host": "alpha-vantage.p.rapidapi.com",
        }

    def get_symbols(self, company: str) -> pd.DataFrame:
        querystring = {
            "datatype": "json",
            "keywords": company,
            "function": "SYMBOL_SEARCH",
        }
        response = requests.get(self.url, headers=self.headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        search_df = pd.DataFrame(data["bestMatches"])
        return search_df

    def get_daily_prices(self, symbol: str) -> pd.DataFrame:
        querystring = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": "compact",
            "datatype": "json",
        }
        response = requests.get(url=self.url, headers=self.headers, params=querystring)
        response.raise_for_status()
        data = response.json()
        price_df = pd.DataFrame(data["Time Series (Daily)"]).T
        price_df = price_df.astype(float)
        price_df.index = pd.to_datetime(price_df.index)
        return price_df

    def plot_candlestick(self, stock_df: pd.DataFrame) -> go.Figure:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=stock_df.index,
                    open=stock_df["1. open"],
                    high=stock_df["2. high"],
                    low=stock_df["3. low"],
                    close=stock_df["4. close"],
                )
            ]
        )

        fig.update_layout(height=800, width=1200)
        return fig
