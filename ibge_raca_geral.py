import pandas as pd
from sqlalchemy.orm import sessionmaker

from bdados.tratar_bdados_app import criar_conexao
from bdados.tratar_dados_externos import salvar_bdados
from bdados.ler_bdados_to_df import carregar_dataframe
from inep_models import MunicipioCenso
import re

def atualizar_bdados(engine, df):

    Session = sessionmaker(bind=engine)
    session = Session()

    # Iterar sobre o DataFrame e atualizar os registros
    for index, row in df.iterrows():
        # Filtrar o objeto MunicipioCenso correspondente
        municipio_censo = session.query(MunicipioCenso).filter_by(
            municipio=row['municipio'],
            ano_censo=row['ano_censo']
        ).first()

        # Se o registro existir, atualize a coluna pop_19a24anos
        if municipio_censo:
            municipio_censo.pop_branca = row['pop_branca']
            municipio_censo.pop_preta = row['pop_preta']
            municipio_censo.pop_amarela = row['pop_amarela']
            municipio_censo.pop_parda = row['pop_parda']
            municipio_censo.pop_indigena = row['pop_indigena']
    # Commit as alterações no banco de dados
    session.commit()

    # Fechar a sessão
    session.close()

# Função para extrair município e estado
def extrair_municipio_estado(texto):
    municipio = ""
    estado = ""

    if '(' in texto and ')' in texto:
        # Extrai o texto antes do primeiro parêntese
        municipio = texto.split(' (')[0].strip()
        # Extrai os dois caracteres dentro dos parênteses
        estado = texto[texto.find('(') + 1:texto.find('(') + 3]
    else:
        # Caso não haja parênteses, retorna o texto original
        municipio = texto.strip()

    return municipio, estado

# Tratamento de dados
def tratar_dados(df):
    try:
        # Aplicar a extração
        df[['municipio', 'estado']] = df['municipio'].apply(extrair_municipio_estado).apply(pd.Series)

        # Limpar espaços
        df['municipio'] = df['municipio'].str.strip()
        return df

    except Exception as e:
        print(f"Erro no processamento: {e}")
        return None

# Carregamento do arquivo
encode = 'ISO-8859-1'
file_path = 'd:/Trab/IBGE/Municipio_raca_geral.xlsx'
df = pd.read_excel(file_path)

# Aplicar tratamento
df = tratar_dados(df)

# recuperar o código do municipio
sql = 'select codigo, nome, estado from municipio'
df_mun = carregar_dataframe(sql)

# Adicionando a coluna 'codigo' ao df1, com 0 como valor padrão
df['codigo'] = 0

# Fazendo a mesclagem com as condições especificadas
for i, row in df.iterrows():
    # Encontrar o código correspondente com base no município e estado
    match = df_mun[(df_mun['nome'] == row['municipio']) & (df_mun['estado'] == row['estado'])]
    if not match.empty:
        df.at[i, 'codigo'] = match['codigo'].values[0]  # Atribui o código encontrado
    else:
        df.at[i, 'codigo'] = 0  # Se não encontrar, mantém o zero

# deletar o que não precisa
df.drop(columns='municipio', inplace=True)
df.rename(columns={'codigo': 'municipio'}, inplace=True)
df['ano_censo']=2022

modulo = 'BD_INEP'
engine, x, y = criar_conexao(modulo)
atualizar_bdados(engine, df)


