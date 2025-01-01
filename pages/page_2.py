import pandas as pd
import streamlit as st
import polars as pol
import plotly.express as px
from src import database

st.title("Detalhes dos Crimes")

crime_table = database.retorna_query('data/crime_data.duckdb', database.ler_query('queries/detalhes.sql'))

teste = pd.pivot_table(crime_table, index='BAIRRO', values='NUM_BO', aggfunc='count').reset_index().sort_values(by='NUM_BO', ascending=False)[:10]

teste = teste.rename(columns={'BAIRRO': 'Bairro', 'NUM_BO': 'Número de BOs'})

teste = teste.reset_index(drop=True)

st.header("Top 10 maiores bairros em números de BOs registrados", divider='gray')

st.table(teste)

st.bar_chart(teste, x='Bairro', y='Número de BOs', horizontal=True, x_label='Número de BOs', y_label='Bairros')

st.header("Número de BOs por período do dia", divider=True)

teste2 = pd.pivot_table(crime_table, index='DESCR_PERIODO', values='NUM_BO', aggfunc='count').reset_index()

teste2 = teste2.rename(columns={'DESCR_PERIODO': 'Período do Dia', 'NUM_BO': 'Número de BOs'})

fig = px.pie(data_frame=teste2, names='Período do Dia', values='Número de BOs', hole=0.3)

st.plotly_chart(fig)

st.header("Principais crimes envolvidos", divider=True)

teste3 = pd.pivot_table(crime_table, index='RUBRICA_MOD', values='NUM_BO', aggfunc='count').reset_index()

teste3 = teste3.rename(columns={'RUBRICA_MOD': 'Tipo de Crime', 'NUM_BO': 'Número de BOs'})

st.table(teste3)

fig3 = px.pie(data_frame=teste3, names='Tipo de Crime', values='Número de BOs', hole=0.3)

st.plotly_chart(fig3)
