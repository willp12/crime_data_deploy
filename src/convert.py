import duckdb
import sqlite3
import pandas as pd

# Caminhos dos arquivos
sqlite_file = "D:/OneDrive/Code/crime_map/data/crime_data.db"
duckdb_file = "D:/OneDrive/Code/crime_map/data/crime_data.duckdb"

# Conectando ao SQLite
sqlite_conn = sqlite3.connect(sqlite_file)

# Conectando ao DuckDB
duckdb_conn = duckdb.connect(duckdb_file)

# Obtenha a lista de tabelas no SQLite
cursor = sqlite_conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterar pelas tabelas e copiar os dados para o DuckDB
for table_name, in tables:
    print(f"Importando tabela: {table_name}")
    
    # Leia os dados da tabela SQLite para um DataFrame
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, sqlite_conn)
    
    # Escreva os dados no DuckDB
    duckdb_conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

# Fechando conexões
sqlite_conn.close()
duckdb_conn.close()
