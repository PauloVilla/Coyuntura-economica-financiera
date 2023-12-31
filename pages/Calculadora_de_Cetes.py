import streamlit as st
from pandas import DataFrame

from cetes_calculator import calculo_cetes

number_input = None
st.set_page_config(layout="wide")

with st.container():
    st.markdown("<h1 style='text-align: center;'>Calculadora de CETES</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Esta calculadora de CETES te permite calcular el valor de tu inversión a un cierto plazo de años.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Módifica el capital inicial, periodo de inversión y años a invertir a tu gusto. La calculadora te dirá el monto en capital final que tendrás después del periodo de inversión.</p>", unsafe_allow_html=True)

    st.divider()
col1, col2, col3, col4 = st.columns(4)
st.divider()
df = DataFrame()
container = st.container()
container.empty()

graph_container = st.container()
graph_container.empty()


def cambio_parametros():
    try:
        capital = float(st.session_state["capital_cetes"])
        periodo = float(st.session_state["periodo"])
        anios_invertir = int(st.session_state["anios_invertir"])
    except Exception as e:
        print(e)
        return

    resumen, historico = calculo_cetes(
        capital, periodo, anios_invertir)
    with container:
        st.data_editor(resumen, hide_index=True, use_container_width=True)
    with graph_container:
        st.markdown("<h2 style='text-align: center;'>Progresión de Capital</h2>", unsafe_allow_html=True)
        st.plotly_chart(historico, use_container_width=True)


with col1:
    st.text_input(
        "Capital Inicial", value=10000, placeholder="Entrar una cantidad de capital incial", key="capital_cetes")
with col2:
    st.selectbox(
        "Periodo de Inversión", options=[28, 91, 182, 364], key="periodo")
with col3:
    st.text_input(
        "Años de Inversión", value=2, placeholder="Entrar cantidad de años a inveritr", key="anios_invertir")

with col4:
    st.button("Calcular", key="calc_button",
              on_click=cambio_parametros, use_container_width=True)

st.write(
    """<style>
    [data-testid="baseButton-secondary"] {
        margin-top: 28px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "Para más información sobre CETES, visita la página de [Banxico](https://www.banxico.org.mx/).")
