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


def get_main_index_data(ticker):
    st_date = datetime(datetime.now().year, 1, 1)
    end_date = datetime.now()

    # Obtener los datos
    data = yf.download(ticker, st_date, end_date, progress=False)
    
    # Agregar las tres líneas a los subplots
    fig = go.Figure(go.Scatter(x=data.index, y=data['Adj Close'], line=dict(color="#B00C0C")))
    
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly" 
    )

    
    return fig

    # fig.show()
