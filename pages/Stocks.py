import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from functions import download_data, asset_allocation, backtesting


@st.cache_data
def tickers_class():
    # Descargar la lista de componentes del S&P 500
    sp500_components = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    # Seleccionar los primeros 200 tickers
    top_200_tickers = sp500_components['Symbol'].tolist()
    return sorted(top_200_tickers)


@st.cache_data
def apply_backtesting(tickers, start_dt, end_dt, cap):
    # Como benchmark utilizamos GSCP
    benchmark = "^GSPC"
    # Descargamos los datos.
    data_opt, data_benchmark_opt = download_data(benchmark=benchmark, tickers_USA=tickers,
                                                 start_date=start_dt, end_date=end_dt).download()
    # Generamos el asset allocation con una tasa de 0.05 libre de riesgo
    AA = asset_allocation(data_opt, data_benchmark_opt, .05)
    # Generamos los pesos, con un n_port de 10000
    weights_summary = AA.summary(10000)

    # Hacemos el backtesting
    # Descargamos los datos con nuevas fechas más actuales, los mismos tickers y benchmarks.
    data_backtesting, data_benchmark_backtesting = download_data(tickers_USA=tickers,
                                                                 benchmark=benchmark,
                                                                 start_date="2022-01-01",
                                                                 end_date="2023-01-01").download()
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
        title="Backtesting de las estrategias",
        xaxis_title="Fecha",
        yaxis_title="Capital",
        showlegend=True
    )
    st.plotly_chart(fig)


# Definimos un contenedor primero
cont = st.empty()

with cont.container():
    st.title("Calculadora de acciones")
    # Definimos parámetros
    param_1, param_2, param_3 = st.columns(3)

    with param_1:
        acciones = st.multiselect("Selecciona la(s) accion(es) de tu portafolio", tickers_class())
        # Lo dejamos como string separado por comas para que funcione
        acciones = ", ".join(acciones)

    with param_2:
        estrategias = st.multiselect("Selecciona las(s) estrategia(s) para el backtesting",
                                     ["Min Var", "Max Sharpe", "Semivariance", "Omega"])

    with param_3:
        capital = st.number_input("Selecciona el capital de tu portafolio", min_value=0)

    param_4, param_5, param_6 = st.columns(3)

    with param_4:
        dt_inicio = st.date_input("Fecha de Inicio", pd.to_datetime('2023-01-01'))

    with param_5:
        dt_final = st.date_input("Fecha de Fin", pd.to_datetime('2023-12-31'))

    with param_6:
        exe = st.button("Ejecutar")

    if exe:
        metricas, history = apply_backtesting(tickers=acciones, start_dt=dt_inicio,
                                              end_dt=dt_final, cap=capital)
        tabla, grafica = st.columns(2)

        with tabla:
            st.write("Resultado de las estrategias")
            metricas = metricas[metricas.index.isin(estrategias)]
            st.table(metricas)

        with grafica:
            history = history[estrategias]
            plot_backtesting(history=history)