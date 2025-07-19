import pandas as pd
from sqlalchemy import create_engine

# Crie uma conexão com o banco de dados SQLite
engine = create_engine('sqlite:///INEP.db')

anos = range(1995, 2022 + 1)
encode = 'ISO-8859-1'
for ano in anos:
    # Caminho do arquivo CSV
    file_path = f'd:/Trab/INEP/Microdados/ies/IES_{ano}.csv'
    if ano < 2009:
        delimitador = '|'
    else:
        delimitador = ';'
    # Carregar o arquivo CSV em um DataFrame, especificando o delimitador correto
    df = pd.read_csv(file_path, delimiter=delimitador, encoding=encode)

    # Nome da tabela no formato IES_ano
    tabela_nome = f'IES_{ano}'

    # Salvar o DataFrame no banco de dados SQLite
    df.to_sql(tabela_nome, con=engine, if_exists='replace', index=False)

    print(f'Dados do ano {ano} foram salvos na tabela {tabela_nome}')

# Exibir as primeiras linhas do DataFrame para verificar a estrutura
x = ''
