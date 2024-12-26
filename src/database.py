import os
import sqlite3
import duckdb
import polars as pl
import pandas as pd
import sqlalchemy

def checa_ou_cria_db(path):
    """
    Verifica se existe um arquivo .db na pasta especificada.
    Se não existir, cria um arquivo .db vazio.
    
    :param path: Caminho para o diretório onde o arquivo será verificado/criado.
    """
    if not os.path.exists(path):
        raise ValueError(f"O caminho '{path}' não existe.")

    # Lista todos os arquivos no diretório
    arquivos = os.listdir(path)
    
    # Verifica se existe um arquivo .db
    for arquivo in arquivos:
        if arquivo.endswith(".db"):
            print(f"Arquivo .db encontrado: {arquivo}")
            return os.path.join(path, arquivo)

    # Se não encontrou, cria um novo arquivo .db
    novo_db = os.path.join(path, "crime_data.db")
    with sqlite3.connect(novo_db) as conn:
        print(f"Arquivo .db criado: {novo_db}")
    
    return novo_db


def check_or_create_table_polars(db_path, table_name, dataframe):
    """
    Verifica se uma tabela existe no banco de dados SQLite.
    Se não existir, cria a tabela a partir de um DataFrame do Polars.

    :param db_path: Caminho para o arquivo do banco de dados.
    :param table_name: Nome da tabela a ser verificada/criada.
    :param dataframe: Polars DataFrame usado para criar a tabela.
    """
    if not os.path.exists(db_path):
        raise ValueError(f"O arquivo de banco de dados '{db_path}' não existe.")
    
    # Conecta ao banco de dados
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Verifica se a tabela existe
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        result = cursor.fetchone()
        
        if result:
            print(f"Tabela '{table_name}' já existe no banco de dados.")
        else:
            # Converte o Polars DataFrame para Pandas e cria a tabela
            dataframe.write_database(table_name, connection="sqlite:///data/crime_data.db", if_table_exists="replace")
            print(f"Tabela '{table_name}' criada com sucesso a partir do DataFrame do Polars.")

def ler_query(arquivo):
    with open(arquivo, 'r') as file:
        return file.read()

def retorna_query(db_path, query):
    conn = duckdb.connect(db_path)
    output = conn.execute(query).fetchdf()
    conn.close()
    return output