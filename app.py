import random

import pandas as pd
import plotly.graph_objs as go
import requests
import streamlit as st
import yaml
import yfinance as yf
from st_pages import Page, show_pages
from yaml.loader import SafeLoader

import data_sources
from config import a_v_token

st.set_page_config(layout="wide")
show_pages(
    [
        Page("app.py", "Coyuntura", "wide", "🏠"),
        Page("pages/Calculadora_de_Cetes.py",
             "Calculadora Cetes", ":computer:"),
    ]
)

NewsTopics = {
    "Blockchain": "blockchain",
    "Earnings": "earnings",
    "IPO": "ipo",
    "Mergers_and_Acquisitions": "mergers_and_acquisitions",
    "Financial_Markets": "financial_markets",
    "Economy_Fiscal_Policy": "economy_fiscal",
    "Economy_Monetary_Policy": "economy_monetary",
    "Economy_Macro_Overall": "economy_macro",
    "Energy_and_Transportation": "energy_transportation",
    "Finance": "finance",
    "Life_Sciences": "life_sciences",
    "Manufacturing": "manufacturing",
    "Real_Estate_and_Construction": "real_estate",
    "Retail_and_Wholesale": "retail_wholesale",
    "Technology": "technology"
}

st.title("Dashboard de Coyuntura Económica")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


def generate_random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    hex_color = hex_color[2:]

    return "#" + hex_color.zfill(6)


selected_stocks = ['IBM', 'TSLA', 'AAPL', 'PLTR']
# --- Titulo

st.title("Análisis de Situación Económica")

# Creamos un contenedor que tendrá todo el dashboard
contenedor = st.empty()

# Almacenamos adentro del contenedor.
with contenedor.container():

    # --- Primer fila dashboard (Indexes)
    inx_1, inx_2, inx_3 = st.columns(3)

    with inx_1:
        st.header("S&P 500 (^GSPC)")
        st.plotly_chart(data_sources.get_main_index_data(
            "^GSPC", generate_random_color()), use_container_width=True)
    with inx_2:
        st.header("NASDAQ100 (^NDX)")
        st.plotly_chart(data_sources.get_main_index_data(
            "^NDX", generate_random_color()), use_container_width=True)
    with inx_3:
        st.header("IPC (^MXX)")
        st.plotly_chart(data_sources.get_main_index_data(
            "^MXX", generate_random_color()), use_container_width=True)

    # --- Segunda fila (Noticias, currencies y stock watchlist)
    st.write("## Principales Noticias")
    cols = st.columns(4)

    news = data_sources.get_main_news(
        [NewsTopics["IPO"], NewsTopics["Technology"]], 4)

    for url, article in news.items():
        column = cols.pop()
        with column:
            st.markdown(f"#### [{article['title'][:70]}...]({url})  " + (
                ":grinning:" if article['sentiment'] == 'POSITIVE' else ":disappointed:"))
            text = article['body'][:140]
            st.markdown(f"{text}... ")
    global_currencies, stock_watchlist = st.columns(2)

    with global_currencies:
        st.header("Monedas")

        if 'selected_currency_1' not in st.session_state:
            st.session_state.selected_currency_1 = 'USD'
            st.session_state.selected_currency_2 = 'AUD'
            st.session_state.selected_currency_3 = 'JPY'
            st.session_state.selected_currency_4 = 'GBP'
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text_input(label="Moneda:", key="selected_currency_1")
        with col2:
            st.text_input(label="Moneda:", key="selected_currency_2")
        with col3:
            st.text_input(label="Moneda:", key="selected_currency_3")
        with col4:
            st.text_input(label="Stock:", key="selected_currency_4")
        selected_currencies = [st.session_state.selected_currency_1, st.session_state.selected_currency_2,
                               st.session_state.selected_currency_3, st.session_state.selected_currency_4]
        st.dataframe(data_sources.get_global_currencies(selected_currencies),
                     hide_index=True, use_container_width=True)

    with stock_watchlist:
        st.header("Stocks")
        if 'selected_stocks_1' not in st.session_state:
            st.session_state.selected_stocks_1 = 'AMZN'
            st.session_state.selected_stocks_2 = 'GOOGL'
            st.session_state.selected_stocks_3 = 'TSLA'
            st.session_state.selected_stocks_4 = 'AAPL'
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text_input(label="Stock:", key="selected_stocks_1")
        with col2:
            st.text_input(label="Stock:", key="selected_stocks_2")
        with col3:
            st.text_input(label="Stock:", key="selected_stocks_3")
        with col4:
            st.text_input(label="Stock:", key="selected_stocks_4")
        selected_stocks = [st.session_state.selected_stocks_1, st.session_state.selected_stocks_2,
                           st.session_state.selected_stocks_3, st.session_state.selected_stocks_4]
        with stock_watchlist:
            st.data_editor(data_sources.get_personalized_stock_list(selected_stocks),
                           hide_index=True, use_container_width=True)

    # ----- Tercer fila (Stocks, news, cetes)
    stocks_graphs, display_news_stock, cetes_plot = st.columns(3)

    with stocks_graphs:
        if 'selected_stock' not in st.session_state:
            initialization = True
            st.session_state.selected_stock = 'AAPL'
        st.header(
            f"Stock Seleccionado: {st.session_state.selected_stock.upper()}")
        st.text_input("Stock a Mostrar", key="selected_stock")
        selected_stock_graph = st.empty()
        with selected_stock_graph:
            st.plotly_chart(data_sources.get_selected_stock(
                st.session_state.selected_stock, generate_random_color()), use_container_width=True)

    with display_news_stock:
        st.header("Noticias de Stock Seleccionado")
        selected_stock_news = st.container()
        selected_stock_news.empty()
        try:
            news = data_sources.get_selected_stock_news(
                st.session_state.selected_stock, 2)
        except:
            st.write("No se encontraron noticias")
        for url, article in news.items():
            st.markdown(f"##### [{article['title'][:70]}...]({url}) " + (
                ":grinning:" if article['sentiment'] == 'POSITIVE' else ":disappointed:"))
            st.markdown(f"{article['body'][:140]}...")

    with cetes_plot:
        st.header("Grafica Histórica de CETES")
        st.plotly_chart(data_sources.get_cetes_graph(
            "28", generate_random_color()), use_container_width=True)
