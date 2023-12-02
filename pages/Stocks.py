import data_sources
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
from functions import download_data, asset_allocation, backtesting


@st.cache_data
def apply_backtesting(tickers, cap, start_dt_back, end_dt_back, start_dt, end_dt):
    # Como benchmark utilizamos GSCP
    benchmark = "^GSPC"
    # Descargamos los datos.
    data_opt, data_benchmark_opt = download_data(benchmark=benchmark, tickers_USA=tickers,
                                                 start_date=start_dt_back, end_date=end_dt_back).download()
    # Generamos el asset allocation con una tasa de 0.05 libre de riesgo
    AA = asset_allocation(data_opt, data_benchmark_opt, .05)
    # Generamos los pesos, con un n_port de 10000
    weights_summary = AA.summary(1000)

    # Hacemos el backtesting
    # Descargamos los datos con nuevas fechas más actuales, los mismos tickers y benchmarks.
    data_backtesting, data_benchmark_backtesting = download_data(tickers_USA=tickers,
                                                                 benchmark=benchmark,
                                                                 start_date=start_dt,
                                                                 end_date=end_dt).download()
    # Hacemos el backtesting
    BT = backtesting(weights_summary=weights_summary, data_stocks=data_backtesting,
                     data_benchmark=data_benchmark_backtesting, cap_inicial=cap)
    # Generamos la historia de evolución
    evol = BT.history
    # Generamos las métricas del backtesting con una tasa de 0.05 libres de riesgo
    metrics = BT.metrics(rf=0.05)
    return metrics, evol


def plot_backtesting(history: pd.DataFrame):
    # Crear una figura de Plotly
    fig = go.Figure()
    # Agregar líneas para cada columna en el DataFrame 'history'
    for column in history.columns:
        fig.add_trace(go.Scatter(x=history.index, y=history[column], mode='lines', name=column))
    # Personalizar el diseño del gráfico
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Capital",
        showlegend=True
    )
    # Cambiar los colores de las líneas
    colors = ['#ff1493', '#ee1289', '#cd1076', '#fc8eac', '#68228b']  # Puedes ajustar los colores según tus preferencias
    for i, column in enumerate(history.columns):
        fig.update_traces(selector=dict(name=column), line=dict(color=colors[i]))

    st.plotly_chart(fig, use_container_width=True)


st.set_page_config(layout="wide")
# Definimos un contenedor primero
cont = st.empty()

with cont.container():
    st.markdown("<h1 style='text-align: center;'>Calculadora de acciones</h1>", unsafe_allow_html=True)
    st.write("---")
    # Definimos parámetros, al ser bastantes los dividimos en 2 filas de 3 columnas
    param_1, param_2, param_3 = st.columns(3)

    with param_1:
        acciones = st.multiselect(
            "Selecciona la(s) accion(es) de tu portafolio", data_sources.get_stocks_catalog())
        # Lo convertimos a string separado por comas para que funcione
        acciones = ", ".join(acciones)

    with param_2:
        estrategias = st.multiselect("Selecciona las(s) estrategia(s) para el backtesting",
                                     ["Min Var", "Max Sharpe", "Semivariance", "Omega"])

    with param_3:
        capital = st.number_input(
            "Selecciona el capital de tu portafolio", min_value=0)
    # Comenzamos con los siguientes parámetros
    param_4, param_5, param_6 = st.columns(3)
    # Obtener la fecha actual
    fecha_actual = datetime.now().date()
    with param_4:
        dt_inicio = st.date_input(
            "Fecha inicial", pd.to_datetime('2023-01-01'))

    with param_5:
        dt_final = st.date_input("Fecha final", max_value=fecha_actual)# pd.to_datetime('2023-12-31'))

    with param_6:
        exe = st.button("Ejecutar", use_container_width=True)
    st.write("---")
    nueva_fecha_inicial = dt_inicio - timedelta(days=365)
    nueva_fecha_final = dt_inicio - timedelta(days=1)   

    if exe:
        metricas, history = apply_backtesting(tickers=acciones, cap=capital, 
                                              start_dt_back= nueva_fecha_inicial,
                                              end_dt_back=nueva_fecha_final,
                                              start_dt=dt_inicio, end_dt=dt_final)

        estrategias.append("Benchmark")
        st.markdown("<h2 style='text-align: center;'>Resultado de las estrategias</h2>", unsafe_allow_html=True)
        metricas = metricas[metricas.index.isin(estrategias)]
        st.table(metricas)

        history = history[estrategias]
        plot_backtesting(history=history)
