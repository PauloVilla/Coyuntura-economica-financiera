import datetime as dt
import warnings
from datetime import datetime, timedelta

import nltk
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
import yfinance as yf
from googletrans import Translator
from ipywidgets import interact
from newspaper import Article
from transformers import pipeline

from cetes import Cetes
from config import a_v_token  # archivo de python con el api key de alpha vantage

sentiment_pipeline = pipeline("sentiment-analysis")
st_date = datetime(datetime.now().year, 1, 1)
end_date = datetime.now()


@st.cache_data
def get_main_index_data(ticker, color):
    # Obtener los datos
    data = yf.download(ticker, st_date, end_date, progress=False)

    # Agregar las tres líneas a los subplots
    fig = go.Figure(go.Scatter(
        x=data.index, y=data['Adj Close'], line=dict(color=color)))

    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Valor",
        template="plotly"
    )
    return fig


@st.cache_data
def get_main_news(topics, number_of_articles):
    topic = ','.join(topics)

    url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics={topic}&sort=RELEVANCE&apikey={a_v_token}'
    r = requests.get(url)
    data = r.json()
    return parse_news(data, number_of_articles)


def parse_news(data, number_of_articles):
    # Obtener las ligas
    links = [[data['feed'][i]['url'], data['feed'][i]['title']]
             for i in range(int(data['items']))]

    news_summaries = {}
    pending_articles = number_of_articles
    while len(news_summaries.keys()) < number_of_articles:
        try:
            link = []
            link = links.pop()
            title = _translate(link[1])
            body = _translate(_get_article_summary(link[0]))
            sentiment_analysis = sentiment_pipeline(link[1])
            print(sentiment_analysis)
            sentiment_analysis = sentiment_analysis.pop()
            print(f"Sentiment Analysis for {link[0]}: \n{sentiment_analysis}")
            news_summaries[link[0]] = {
                "title": title,
                "body": body,
                "sentiment": sentiment_analysis["label"]
            }
        except:
            print(f"Error parsing article {link[0]}")
        pending_articles = number_of_articles - len(news_summaries.keys())
        print(f"Pending articles: {pending_articles}")

    return news_summaries


def _translate(text):
    translator = Translator()
    return translator.translate(text, dest='es').text


def _get_article_summary(link):
    # Web Scrapping
    article = Article(link)
    article.download()
    article.parse()
    article.nlp()
    return article.summary


@st.cache_data
def get_global_currencies():
    vs_currency = 'MXN'
    currencies = ['USD', 'AUD', 'JPY', 'GBP']

    currency_names = []
    exchange_rate = {}
    bid_price = {}
    ask_price = {}

    for c in currencies:
        url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={c}&to_currency={vs_currency}&apikey={a_v_token}"
        r = requests.get(url)
        data = r.json()
        data = data['Realtime Currency Exchange Rate']
        currency_names.append(f"{c}/{vs_currency}")
        exchange_rate[c] = data['5. Exchange Rate']
        bid_price[c] = data['8. Bid Price']
        ask_price[c] = data['9. Ask Price']

    df = pd.DataFrame({
        'Moneda': currency_names,
        'Tipo de Cambio': exchange_rate.values(),
        'Compra': bid_price.values(),
        'Venta': ask_price.values()
    })
    return df


@st.cache_data
def get_personalized_stock_list(stocks):
    open = {}
    high = {}
    low = {}
    price = {}
    volume = {}
    previous_close = {}
    change = {}
    change_percent = {}

    for t in stocks:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={t}&apikey={a_v_token}'
        r = requests.get(url)
        data = r.json()
        data = data['Global Quote']
        open[t] = data['02. open']
        high[t] = data['03. high']
        low[t] = data['04. low']
        price[t] = data['05. price']
        volume[t] = data['06. volume']
        previous_close[t] = data['08. previous close']
        change[t] = data['09. change']
        change_percent[t] = data['10. change percent']

    df = pd.DataFrame({
        'Ticker': stocks,
        'Apertura': open.values(),
        'Alta': high.values(),
        'Baja': low.values(),
        'Precio': price.values(),
        'Volumen': volume.values(),
        'Precio al Ultimo Cierre': previous_close.values(),
        'Cambio': change.values(),
        'Porcentaje de Cambio': change_percent.values()
    })
    possible_choices = [col for col in df.columns if col !=
                        'Ticker' and col != 'Porcentaje de Cambio']
    df[possible_choices] = df[possible_choices].astype(float)
    df['Porcentaje de Cambio'] = df['Porcentaje de Cambio'].str[:-
                                                                1].astype(float)
    return df


@st.cache_data
def get_selected_stock(stock, graph_color):
    # Obtener los datos
    data = yf.download(stock, st_date, end_date, progress=False)

    # Crear una figura de Plotly
    fig = go.Figure()

    # Agregar una línea de gráfica para el precio de cierre ajustado
    fig.add_trace(go.Scatter(
        x=data.index, y=data['Adj Close'], mode='lines', line=dict(color=graph_color)))

    # Configurar el título y etiquetas de los ejes
    fig.update_layout(
        title=stock,
        xaxis_title='Fecha',
        yaxis_title='Precio Cierre',
        xaxis=dict(tickangle=-45)
    )

    return fig


@st.cache_data
def get_cetes_graph(term, graph_color):
    cetes = Cetes(term)
    start_date = '2010-01-01'
    end_date = str(dt.date.today())
    data = cetes.get_data(date_end=end_date, date_start=start_date)

    # Convierte la columna "date" a tipo datetime si no está en ese formato
    data['date'] = pd.to_datetime(data['date'])

    # Crea la figura de la gráfica de barras
    fig = go.Figure()

    # Agrega las barras a la figura
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['value'],
        marker_color=graph_color))

    # Configuración del estilo de la gráfica
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Valor',
        title=f'Gráfica de barras para Cetes {term}')
    return fig


@st.cache_data
def get_selected_stock_news(stock, number_of_articles):
    d = datetime.today() - timedelta(days=180)
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={stock}&time_from={d.strftime('%Y%m%dT%H%M')}&limit=3&sort=RELEVANCE&apikey={a_v_token}"
    r = requests.get(url)
    data = r.json()
    return parse_news(data, number_of_articles)
