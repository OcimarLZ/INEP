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
            municipio_censo.pop_19a24anos = row['pop_19a24anos']

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
    # Preencher valores NaN na coluna 'municipio'
    df['municipio'] = df['municipio'].fillna(method='ffill')

    # Verificar se a coluna 'idade' existe
    if 'idade' not in df.columns:
        print("ERRO: Coluna 'idade' não encontrada")
        return None

    # Pivotear os dados com tratamento de erros
    try:
        df_pivot = df.pivot_table(
            index='municipio',
            columns='idade',
            values='total',
            aggfunc='first',  # Usar first para evitar agregações indesejadas
            fill_value=0
        )

        # Resetar índice
        df_pivot = df_pivot.reset_index()

        # Verificar colunas específicas
        colunas_idade = ['19 anos', '20 a 24 anos']
        for col in colunas_idade:
            if col not in df_pivot.columns:
                print(f"AVISO: Coluna {col} não encontrada")
                df_pivot[col] = 0

        # Calcular população 19-24 anos
        df_pivot['pop_19a24anos'] = df_pivot.get('19 anos', 0) + df_pivot.get('20 a 24 anos', 0)

        # Aplicar a extração
        df_pivot[['municipio', 'estado']] = df_pivot['municipio'].apply(extrair_municipio_estado).apply(pd.Series)

        # Limpar espaços
        df_pivot['municipio'] = df_pivot['municipio'].str.strip()
        df_pivot.drop(columns='19 anos')
        df_pivot.drop(columns='20 a 24 anos')
        return df_pivot

    except Exception as e:
        print(f"Erro no processamento: {e}")
        return None

# Carregamento do arquivo
encode = 'ISO-8859-1'
file_path = 'd:/Trab/IBGE/Municipio_idade.xlsx'
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
df.drop(columns='19 anos', inplace=True)
df.drop(columns='20 a 24 anos', inplace=True)
df.drop(columns='estado', inplace=True)
df.rename(columns={'codigo': 'municipio'}, inplace=True)
df['ano_censo']=2022

modulo = 'BD_INEP'
engine, x, y = criar_conexao(modulo)
atualizar_bdados(engine, df)

print(df)
# Exibindo o DataFrame resultante


# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
df['ano_censo'] = 2022
salvar_bdados(df, MunicipioCenso, 'id')

