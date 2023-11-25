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

st.set_page_config(layout="wide")
show_pages(
    [
        Page("app.py", "Coyuntura", "🏠"),
        Page("pages/Calculadora_de_Cetes.py",
             "Calculadora Cetes", ":computer:"),
        Page("pages/Stocks.py", "Acciones", ":chart_with_upwards_trend:"),
    ]
)

NewsTopics = {
    "Blockchain": "blockchain",
    "Earnings": "earnings",
    "IPO": "ipo",
    "Mergers and Acquisitions": "mergers_and_acquisitions",
    "Financial Markets": "financial_markets",
    "Economy Fiscal Policy": "economy_fiscal",
    "Economy Monetary Policy": "economy_monetary",
    "Economy Macro Overall": "economy_macro",
    "Energy and Transportation": "energy_transportation",
    "Finance": "finance",
    "Life Sciences": "life_sciences",
    "Manufacturing": "manufacturing",
    "Real Estate and Construction": "real_estate",
    "Retail and Wholesale": "retail_wholesale",
    "Technology": "technology"
}

st.markdown("<h1 style='text-align: center;'>Dashboard de Coyuntura Económica</h1>",
            unsafe_allow_html=True)

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)


def generate_random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    hex_color = hex_color[2:]

    return "#" + hex_color.zfill(6)


selected_stocks = ['IBM', 'TSLA', 'AAPL', 'PLTR']
# --- Titulo

# Creamos un contenedor que tendrá todo el dashboard
contenedor = st.empty()

# Almacenamos adentro del contenedor.
with contenedor.container():

    # --- Primer fila dashboard (Indexes)
    inx_1, inx_2, inx_3 = st.columns(3)

    with inx_1:
        st.markdown("<h2 style='text-align: center;'>S&P 500</h2>",
                    unsafe_allow_html=True)

        st.plotly_chart(data_sources.get_main_index_data(
            "^GSPC", generate_random_color()), use_container_width=True)
    with inx_2:
        st.markdown("<h2 style='text-align: center;'>NASDAQ100</h2>",
                    unsafe_allow_html=True)
        st.plotly_chart(data_sources.get_main_index_data(
            "^NDX", generate_random_color()), use_container_width=True)
    with inx_3:
        st.markdown("<h2 style='text-align: center;'>IPC</h2>",
                    unsafe_allow_html=True)
        st.plotly_chart(data_sources.get_main_index_data(
            "^MXX", generate_random_color()), use_container_width=True)

    # --- Segunda fila (Noticias, currencies y stock watchlist)
    st.markdown("<h2 style='text-align: center;'>Principales Noticias</h2>",
                unsafe_allow_html=True)
    st.multiselect("", options=NewsTopics, default=[
                   "IPO", "Technology"], key="selected_topics")
    cols = st.columns(4)

    news = data_sources.get_main_news(st.session_state.selected_topics, 4)

    for url, article in news.items():
        column = cols.pop()
        with column:
            st.markdown(f"#### [{article['title'][:70]}...]({url})  " + (
                ":grinning:" if article['sentiment'] == 'POSITIVE' else ":disappointed:"))
            text = article['body'][:140]
            st.markdown(f"{text}... ")
    global_currencies, stock_watchlist = st.columns(2)

    with global_currencies:
        st.markdown("<h2 style='text-align: center;'>Monedas</h2>",
                    unsafe_allow_html=True)

        if 'selected_currency_1' not in st.session_state:
            st.session_state.selected_currency_1 = 'USD'
            st.session_state.selected_currency_2 = 'AUD'
            st.session_state.selected_currency_3 = 'JPY'
            st.session_state.selected_currency_4 = 'GBP'
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.selectbox(label="",
                         options=data_sources.get_currency_catalog(), key="selected_currency_1")
        with col2:
            st.selectbox(label="",
                         options=data_sources.get_currency_catalog(), key="selected_currency_2")
        with col3:
            st.selectbox(label="",
                         options=data_sources.get_currency_catalog(), key="selected_currency_3")
        with col4:
            st.selectbox(label="",
                         options=data_sources.get_currency_catalog(), key="selected_currency_4")
        selected_currencies = [st.session_state.selected_currency_1, st.session_state.selected_currency_2,
                               st.session_state.selected_currency_3, st.session_state.selected_currency_4]
        st.dataframe(data_sources.get_global_currencies(selected_currencies),
                     hide_index=True, use_container_width=True)

    with stock_watchlist:
        st.markdown("<h2 style='text-align: center;'>Acciones</h2>",
                    unsafe_allow_html=True)
        if 'selected_stocks_1' not in st.session_state:
            st.session_state.selected_stocks_1 = 'AMZN'
            st.session_state.selected_stocks_2 = 'GOOGL'
            st.session_state.selected_stocks_3 = 'TSLA'
            st.session_state.selected_stocks_4 = 'AAPL'
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.selectbox(label="",
                         options=data_sources.get_stocks_catalog(), key="selected_stocks_1")
        with col2:
            st.selectbox(label="",
                         options=data_sources.get_stocks_catalog(), key="selected_stocks_2")
        with col3:
            st.selectbox(label="",
                         options=data_sources.get_stocks_catalog(), key="selected_stocks_3")
        with col4:
            st.selectbox(label="",
                         options=data_sources.get_stocks_catalog(), key="selected_stocks_4")
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
        st.markdown(
            "<h2 style='text-align: center;'>Seleccionar Acción</h2>", unsafe_allow_html=True)
        st.selectbox(label="",
                     options=data_sources.get_stocks_catalog(), key="selected_stock")
        selected_stock_graph = st.empty()
        with selected_stock_graph:
            st.plotly_chart(data_sources.get_selected_stock(
                st.session_state.selected_stock, generate_random_color()), use_container_width=True)

    with display_news_stock:
        st.markdown(
            "<h2 style='text-align: center;'>Noticias de Acción Seleccionada</h2>", unsafe_allow_html=True)
        selected_stock_news = st.container()
        selected_stock_news.empty()
        try:
            news = data_sources.get_selected_stock_news(
                st.session_state.selected_stock, 2)
            for url, article in news.items():
                st.markdown(f"##### [{article['title'][:70]}...]({url}) " + (
                    ":grinning:" if article['sentiment'] == 'POSITIVE' else ":disappointed:"))
                st.markdown(f"{article['body'][:140]}...")
        except:
            st.write(
                f"No se encontraron noticias relacionadas con la Acción {st.session_state.selected_stock}")

    with cetes_plot:
        st.markdown(
            "<h2 style='text-align: center;'>Grafica Histórica de CETES</h2>", unsafe_allow_html=True)
        st.plotly_chart(data_sources.get_cetes_graph(
            "28", generate_random_color()), use_container_width=True)
