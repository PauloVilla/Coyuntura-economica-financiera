import random

import pandas as pd
import plotly.graph_objs as go
import requests
import streamlit as st
import yaml
import yfinance as yf
from yaml.loader import SafeLoader

import data_sources
from config import a_v_token

st.set_page_config(page_title="Dashboard de Coyuntura económica",layout="wide")

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

def generate_random_color():
    color = random.randrange(0, 2**24)
    hex_color = hex(color)
    return "#" + hex_color[2:]


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
        st.plotly_chart(data_sources.get_main_index_data("^GSPC", generate_random_color()), use_container_width=True)
    with inx_2:
        st.header("NASDAQ100 (^NDX)")
        st.plotly_chart(data_sources.get_main_index_data("^NDX", generate_random_color()), use_container_width=True)
    with inx_3:
        st.header("IPC (^MXX)")
        st.plotly_chart(data_sources.get_main_index_data("^MXX", generate_random_color()), use_container_width=True)

    # --- Segunda fila (Noticias, currencies y stock watchlist)
    main_news, secondary_news, global_currencies, stock_watchlist = st.columns(4)

    with main_news:
        st.header("Noticias Principales")

    with secondary_news:
        st.subheader("Noticia Secundaria 1")
        st.subheader("Noticia Secundaria 2")
        st.subheader("Noticia Secundaria 3")


    with global_currencies:
        st.header("Principales Monedas vs USD")

    with stock_watchlist:
        st.header("Lista Personalizada de Stocks")

    # ----- Tercer fila (Stocks, news, cetes)
    stocks_graphs, display_news_stock, cetes_plot = st.columns(3)

    with stocks_graphs:
        st.header("Stock Seleccionado")

    with display_news_stock:
        st.header("Noticias de Stock Seleccionado")

    with cetes_plot:
        st.header("Grafica Histórica de Cetes")

