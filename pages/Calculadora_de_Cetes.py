import streamlit as st

from cetes_calculator import calculo_cetes

st.me(page_title="Calculadora de Cetes")

df = calculo_cetes(10000000, 28)

df.add(calculo_cetes(1000000, 91))

st.write(df)
