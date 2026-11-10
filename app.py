import os
import streamlit as st

st.title("Prueba de estructura")

st.write("Directorio actual:", os.getcwd())
st.write("Archivos encontrados:", os.listdir("."))
st.write("Carpetas encontradas:", os.listdir("config"))
st.write("Archivos de módulos:", os.listdir("modulos"))
