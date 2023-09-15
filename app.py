import yaml
import requests
import yfinance as yf
import streamlit as st
from config import api_key
import plotly.graph_objs as go
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is None:
    st.warning('Please enter your username and password')
    st.session_state["Auth"] = 0
elif not authentication_status:
    st.error('Username/password is incorrect')
    st.session_state["Auth"] = 0
elif authentication_status:
    st.session_state["Auth"] = 1
    with st.sidebar:
        authenticator.logout('Logout', 'main')

if st.session_state["Auth"] == 1:
    st.title("Analysis of economic situation by stock")

    ticker = st.text_input("Select your Ticker: ")
    start_date = st.date_input("Select starting date to analyze")
    end_date = st.date_input("Select ending date to analyze")
    if len(ticker) == 0 or start_date == end_date:
        st.error("Stock not available")
        st.stop()
    data = yf.download(ticker, start=start_date, end=end_date)

    # Crear una figura de Plotly
    fig = go.Figure()

    # Agregar una línea de gráfica para el precio de cierre ajustado
    fig.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], mode='lines', line=dict(color='maroon')))

    # Configurar el título y etiquetas de los ejes
    fig.update_layout(
        title=ticker,
        xaxis_title='Date',
        yaxis_title='Adj. Close Price',
        xaxis=dict(tickangle=-45)
    )
    st.plotly_chart(fig)
    st_date = str(start_date)
    n_news = st.number_input("Select the number of news", 0, 5, 3)
    # NEWS
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={ticker}&" \
          f"time_from={st_date.replace('-', '') + 'T0000'}&limit=3&sort=RELEVANCE&apikey={api_key}"
    r = requests.get(url)
    data = r.json()
    st.subheader("News")
    news_list = [data['feed'][i]['summary'] for i in range(n_news)]
    for i in range(n_news):
        st.write(news_list[i])
        st.write("---")

