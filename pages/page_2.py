import pandas as pd
import streamlit as st
import polars as pol
import plotly.express as px
from src import database

st.title("Detalhes dos Crimes")

crime_table = database.retorna_query('data/crime_data.duckdb', database.ler_query('queries/detalhes.sql'))

teste = pd.pivot_table(crime_table, index='BAIRRO', values='NUM_BO', aggfunc='count').reset_index().sort_values(by='NUM_BO', ascending=False)[:10]

st.table(teste)

st.bar_chart(teste, x='BAIRRO', y='NUM_BO', horizontal=True, x_label='Número de BOs', y_label='Bairros')

teste2 = pd.pivot_table(crime_table, index='DESCR_PERIODO', values='NUM_BO', aggfunc='count').reset_index()

fig = px.pie(data_frame=teste2, names='DESCR_PERIODO', values='NUM_BO', hole=0.3)

st.plotly_chart(fig)

teste3 = pd.pivot_table(crime_table, index='RUBRICA_MOD', values='NUM_BO', aggfunc='count').reset_index()

st.table(teste3)

fig3 = px.pie(data_frame=teste3, names='RUBRICA_MOD', values='NUM_BO', hole=0.3)

st.plotly_chart(fig3)
