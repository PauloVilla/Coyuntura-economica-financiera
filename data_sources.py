import warnings
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import yfinance as yf
from ipywidgets import interact

from cetes import Cetes
from config import a_v_token  # archivo de python con el api key de alpha vantage


def get_main_index_data(ticker, color):
    st_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()

    # Obtener los datos
    data = yf.download(ticker, st_date, end_date, progress=False)
    
    # Agregar las tres líneas a los subplots
    fig = go.Figure(go.Scatter(x=data.index, y=data['Adj Close'], line=dict(color=color)))
    
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly" 
    )
    return fig


# moving this from the main app.py

# def show_main_currencies():
#     vs_currency = 'USD'
#     currencies = ['MXN','AUD','JPY', 'GBP']

#     st.subheader("Principales Monedas Globales")
#     exchange_rate = {}
#     bid_price = {}
#     ask_price ={}
#     st.text(f"Moneda de referencia: {vs_currency}")
#     for c in currencies:
#         url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={c}&to_currency={vs_currency}&apikey={a_v_token}"
#         r = requests.get(url)
#         data = r.json()
#         data = data['Realtime Currency Exchange Rate']
#         exchange_rate[c] = data['5. Exchange Rate']
#         bid_price[c] = data['8. Bid Price']
#         ask_price[c] = data['9. Ask Price']
#     with st.container():
#         df = pd.DataFrame({
#             'Moneda': currencies,
#             'Tipo de Cambio': exchange_rate.values(),
#             'Compra': bid_price.values(),
#             'Venta': ask_price.values()
#             })
#         st.table(df)


# # -------- DEJÉ LA INFO QUE TENÍAMOS DENTRO DE ESTA FUNCIÓN PARA NO BORRARLA (Momentáneamente)
# def data():
#     ticker = st.text_input("Select your Ticker: ")
#     start_date = st.date_input("Select starting date to analyze")
#     end_date = st.date_input("Select ending date to analyze")
#     if len(ticker) == 0 or start_date == end_date:
#         st.error("Stock not available or date not selected")
#         st.stop()
#     data = yf.download(ticker, start=start_date, end=end_date)

#     # Crear una figura de Plotly
#     fig = go.Figure()

#     # Agregar una línea de gráfica para el precio de cierre ajustado
#     fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', line=dict(color='maroon')))

#     # Configurar el título y etiquetas de los ejes
#     fig.update_layout(
#         title=ticker,
#         xaxis_title='Date',
#         yaxis_title='Adj. Close Price',
#         xaxis=dict(tickangle=-45)
#     )
#     st.plotly_chart(fig)
#     st_date = str(start_date)
#     n_news = st.number_input("Select the number of news", 0, 5, 3)
#     # NEWS
#     url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&" \
#           f"time_from={st_date.replace('-', '') + 'T0000'}&limit=3&sort=RELEVANCE&apikey={a_v_token}"
#     r = requests.get(url)
#     data = r.json()
#     st.subheader("News")
#     news_list = [data['feed'][i]['summary'] for i in range(n_news)]
#     for i in range(n_news):
#         st.write(news_list[i])
#         st.write("---")

#     show_main_currencies()

