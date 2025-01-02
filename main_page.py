import polars as pol
import folium
import streamlit as st
from streamlit.components.v1 import html
from folium.plugins import MarkerCluster
from src import database

query = database.ler_query('queries/lat_long.sql') 
cluster_data = database.retorna_query('data/crime_data.duckdb', query).values.tolist()

@st.cache_data
def cria_mapa_cluster(cluster=cluster_data):
    m = folium.Map(location=(-23.533773, -46.625290), zoom_start=12)
    MarkerCluster(cluster_data).add_to(m)
    mapa_html = m._repr_html_()
    return mapa_html

# Renderizar o mapa como HTML e exibir no Streamlit
st.set_page_config(page_title="Mapa de Crime", layout="wide")
st.title("Projeto de Dados - Crime contra Celulares em SP")
st.header("Mapa com Folium no Streamlit")
st.write("""Este projeto tem como objetivo ilustrar os incidentes com
         celulares na cidade de São Paulo. Segue abaixos um mapa interativo com os clusters - neste mapa, pode-se navegar entre os bairros e ruas:""")

html(cria_mapa_cluster(), height=600)
