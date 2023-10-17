import streamlit as st

from cetes_calculator import calculo_cetes

number_input = None


def cambio_parametros(key):
    print(f"Change on {key}")
    try:
        capital = float(st.session_state["capital_cetes"])
        periodo = float(st.session_state["periodo"])
        anios_invertir = int(st.session_state["anios_invertir"])
    except Exception as e:
        print(e)
        return
    table = st.table(calculo_cetes(
        capital, periodo, anios_invertir))


col1, col2, col3 = st.columns(3)
with col1:
    st.text_input(
        "Capital Inicial", placeholder="Entrar una cantidad de capital incial", key="capital_cetes",  on_change=cambio_parametros, args=("capital_cetes",))
with col2:
    st.selectbox(
        "Periodo de Inversión", options=[28, 91, 182, 364], key="periodo",  on_change=cambio_parametros, args=("periodo",))
with col3:
    st.text_input(
        "Años de Inversión", placeholder="Entrar cantidad de años a inveritr", key="anios_invertir",  on_change=cambio_parametros, args=("anios_invertir",))
