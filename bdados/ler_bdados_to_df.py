import pandas as pd
from bdados.tratar_bdados_app import criar_conexao

def carregar_dataframe(sql):
    # Conectar ao banco de dados SQLite
    modulo = "BD_INEP"
    db_bi_cnx, salvarxls, dbase = criar_conexao(modulo)
    # Executar a query e carregar os resultados em um DataFrame
    df = pd.read_sql_query(sql, db_bi_cnx)
    # Fechar a conexão com o banco de dados
    db_bi_cnx.close()
    return df


