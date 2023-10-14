import streamlit as st

from cetes_calculator import calculo_cetes

number_input = None


def cambio_capital(key):
    try:
        capital = float(st.session_state[key])
    except:
        st.write("Formato inválido.")
        return
    table = st.table(calculo_cetes(
        capital, [28, 91, 182, 364]))


number_input = st.text_input(
    "Capital Inicial", placeholder="Entrar una cantidad", key="capital_cetes",  on_change=cambio_capital, args=("capital_cetes",))

table_placeholder = st.container()
