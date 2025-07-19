import pandas as pd
from sqlalchemy import create_engine

# Defina suas conexões e tabelas aqui
sqlite_engine = create_engine('sqlite:///INEP.db')
postgres_engine = create_engine('postgresql+psycopg2://postgres:Sem@Senha#@localhost:5433/observa_edubr')

# Listar tabelas para migração
tabelas = ["comum.regiao", "comum.uf", "comum.mesorregiao", "comum.microrregiao", "comum.municipio"]


def migrate_table(schema_table_name, table_name):
    # Lê os dados do SQLite
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, sqlite_engine)

    # Converte colunas de bytes para strings, se necessário
    for column in df.columns:
        if pd.api.types.is_object_dtype(df[column]):
            df[column] = df[column].apply(lambda x: x.decode('latin-1') if isinstance(x, bytes) else x)

    # Tenta gravar no PostgreSQL
    schema, tabela = schema_table_name.split('.')
    df.to_sql(tabela, postgres_engine, schema=schema, if_exists='append', index=False, method="multi", chunksize=1000)


# Migração das tabelas
for schema_table in tabelas:
    print(f"Migrando {schema_table}...")
    schema, table = schema_table.split(".")
    migrate_table(schema_table, table)
    print(f"Conclusão da migração de {schema_table}.")
