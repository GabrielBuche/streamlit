import streamlit as st
from buche.exercicio import pegarDadosBuche

BtnBuche = st.button("carregar dados Buche")

if BtnBuche:
    data = pegarDadosBuche()
    st.dataframe(data)



    