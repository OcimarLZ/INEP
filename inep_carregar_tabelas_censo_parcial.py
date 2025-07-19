import pandas as pd
import numpy as np
from bdados.tratar_dados_externos import salvar_bdados, ler_ies
from inep_models import (Area, Area_especifica, Area_detalhada, Tp_rede, Tp_modal_ensino, Tp_nivel_academico, Tp_grau_academico,
                         Tp_dimensao, Cine_rotulo, Curso, Curso_censo)

def tratar_df_rotulos(df):
    # Criar um dicionário para armazenar os índices gerados para cada 'NO_CINE_ROTULO' único
    cine_rotulo_map = {}
    # Atribuir o índice do DataFrame à coluna 'codigo' onde o valor original é nulo
    print('Tratando os Dados...Refazendo campo de Rotulo para os em branco')
    # Iterar sobre o DataFrame e preencher 'CO_CINE_ROTULO' com índices gerados onde o valor original é nulo
    for idx, row in df.iterrows():
        if pd.isnull(row['CO_CINE_ROTULO']):
            no_cine_rotulo = row['NO_CINE_ROTULO']
            # Verificar se há outro registro com o mesmo 'NO_CINE_ROTULO' e 'CO_CINE_ROTULO' não nulo
            matching_rows = df[(df['NO_CINE_ROTULO'] == no_cine_rotulo) & df['CO_CINE_ROTULO'].notnull()]
            if not matching_rows.empty:
                # Atribuir o mesmo código encontrado
                df.at[idx, 'CO_CINE_ROTULO'] = matching_rows.iloc[0]['CO_CINE_ROTULO']
            else:
                # Gerar um novo código se não encontrar
                if no_cine_rotulo not in cine_rotulo_map:
                    cine_rotulo_map[no_cine_rotulo] = f"ind_{len(cine_rotulo_map)}"
                df.at[idx, 'CO_CINE_ROTULO'] = cine_rotulo_map[no_cine_rotulo]
    return df

def tratar_coluna_nula(nul_df, coluna, ies_df, coluna_ies, metodo):
    # Criar um dicionário para armazenar os índices gerados para cada 'NO_CINE_ROTULO' único
    cine_rotulo_map = {}
    # Atribuir o índice do DataFrame à coluna 'codigo' onde o valor original é nulo
    print(f'Tratando os Dados...Refazendo da coluna {coluna } com valores em branco')
    # Iterar sobre o DataFrame e preencher 'CO_CINE_ROTULO' com índices gerados onde o valor original é nulo
    for idx, row in nul_df.iterrows():
        if pd.isnull(row[coluna]):
            ies = row['CO_IES']
            # Recupera os valores da ies associada
            matching_rows = ies_df[(ies_df['codigo'] == ies)]
            if not matching_rows.empty:
                valor = matching_rows.iloc[0][coluna_ies]
                # Atribuir o mesmo código encontrado
                if metodo == 'S':
                    nul_df.at[idx, coluna] = valor
                elif metodo == 'C':
                    if coluna == 'TP_REDE':
                        if valor < 4:
                            nul_df.at[idx, coluna] = 1
                        else:
                            nul_df.at[idx, coluna] = 2
                    if coluna == 'IN_GRATUITO':
                        if valor < 4:
                            nul_df.at[idx, coluna] = 0
                        else:
                            nul_df.at[idx, coluna] = 1
                    if coluna == 'TP_GRAU_ACADEMICO':
                        nul_df.at[idx, coluna] = 0
    return nul_df


def seta_zero_colunas_com_nan(df):
    # Itera sobre todas as colunas do DataFrame
    for column in df.columns:
        # Verifica se a coluna é do tipo float, integer ou boolean
        if np.issubdtype(df[column].dtype, np.number) or df[column].dtype == bool:
            # Substitui NaN por 0 na coluna
            df[column] = df[column].fillna(0)
    return df

tp_rede = {
     1: 'Pública',
     2: 'Privada'}

tp_dimensao = {
    1: 'Cursos presenciais ofertados no Brasil',
    2: 'Cursos a distância ofertados no Brasil',
    3: 'Cursos a distância com dimensão de dados somente a nível Brasil',
    4: 'Cursos a distância ofertados por instituições brasileiras no exterior'}

tp_grau_acad = {
    0: 'Não Aplicável',
    1: 'Bacharelado',
    2: 'Licenciatura',
    3: 'Tecnológico',
    4: 'Bacharelado e Licenciatura'}

tp_nivel_acad = {
    1: 'Graduação',
    2: 'Sequencial de Formação Específica'}

tp_modal = {
    1: 'Presencial',
    2: 'Curso a distância'}

# Remover logo no inicia do processo
remover_cols = ['NO_REGIAO', 'NO_UF', 'NO_MUNICIPIO', 'IN_CAPITAL', 'CO_UF']
# Remover antes de salvar a tabela de censo dos cursos
remover_cols2 = ['NO_CURSO', 'NO_CINE_ROTULO', 'NO_CINE_AREA_GERAL', 'NO_CINE_AREA_ESPECIFICA', 'NO_CINE_AREA_DETALHADA']

de_para_censo = {'NU_ANO_CENSO': 'ano_censo',
    'CO_REGIAO': 'regiao',
    'SG_UF': 'estado',
    'CO_MUNICIPIO': 'municipio',
    'TP_ORGANIZACAO_ACADEMICA': 'org_academica',
    'TP_CATEGORIA_ADMINISTRATIVA': 'categoria',
    'TP_DIMENSAO': 'dimensao',
    'CO_IES': 'ies',
    'CO_CURSO': 'curso',
    'CO_CINE_ROTULO': 'cine_rotulo',
    'CO_CINE_AREA_GERAL': 'area_geral',
    'CO_CINE_AREA_ESPECIFICA': 'area_especifica',
    'CO_CINE_AREA_DETALHADA': 'area_detalhada'}
encode = 'ISO-8859-1'
delimitador = ';'
df = pd.DataFrame()
# Definir o caminho da pasta
ano = 2023
file_patch = f'd:/Trab/INEP/Microdados/censo/Censo_{ano}.CSV'
# Carregar o arquivo CSV em um DataFrame, especificando o delimitador correto
df_parc = pd.read_csv(file_patch, delimiter=delimitador, encoding=encode)
# Remover algumas colunas do dataframe
df_parc = df_parc.drop(columns=remover_cols)
# Criar um dicionário com o nome da coluna e o tipo de dados
if 'CO_CINE_ROTULO2' in df_parc.columns:
    df.rename(columns={'CO_CINE_ROTULO2': 'CO_CINE_ROTULO'})
    print('Renomeando label rotulo')
df = pd.concat([df, df_parc])
print(f'Leitura finalizada do censo do ano {ano} com {len(df_parc)} registros')
print(f'Total de registros carregados {len(df)}')
# Veririca se há valores nulos nas colunas
# Resetar o índice do DataFrame completo, concatenado com os df dos diversos anaos
print('Tratando os Dados... Reindexando DF')
df = df.reset_index(drop=True)
# Conta os valores nulos em cada coluna
valores_nuls = df.isnull().sum()
# Filtra colunas com contagem de nulos maior que zero
valores_nuls_filtrado = valores_nuls[valores_nuls > 0]
# Cria um DataFrame para exibir os resultados de forma mais organizada
nulos_df = pd.DataFrame(valores_nuls_filtrado, columns=['Qtde']).reset_index()
nulos_df.columns = ['Coluna', 'Qtde']
qtd_nulls = df['CO_CINE_ROTULO'].isnull().sum()
if qtd_nulls > 0:
    df = tratar_df_rotulos(df)
# Exibe o DataFrame com as contagens de valores nulos
# Filtrando os estados com valor nulo
# lER E carregar o dataframe das IES para calcular o valores a serem trocados
ies_df = ler_ies()
# Filtra as linhas onde a coluna 'regioes' possui valores nulos
nul_df = df[df['CO_REGIAO'].isnull()]
if len(nul_df) > 0:
    nul_df = tratar_coluna_nula(nul_df, 'CO_REGIAO', ies_df, 'regiao', 'S')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'MUNICIPIOS' possui valores nulos
nul_df = df[df['SG_UF'].isnull()]
if len(nul_df) > 0:
    nul_df = tratar_coluna_nula(nul_df, 'SG_UF', ies_df, 'estado', 'S')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'municipios' possui valores nulos
nul_df = df[df['CO_MUNICIPIO'].isnull()]
if len(nul_df) > 0:
    nul_df = tratar_coluna_nula(nul_df, 'CO_MUNICIPIO', ies_df, 'municipio', 'S')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'municipios' possui valores nulos
nul_df = df[df['TP_REDE'].isnull()]
if len(nul_df) > 0:
    nul_df = tratar_coluna_nula(nul_df, 'TP_REDE', ies_df, 'categoria', 'C')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'GRATUÍTO' possui valores nulos
nul_df = df[df['IN_GRATUITO'].isnull()]
if len(nul_df) > 0:
    nul_df = tratar_coluna_nula(nul_df, 'IN_GRATUITO', ies_df, 'categoria', 'C')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'GRATUÍTO' possui valores nulos
nul_df = df[df['TP_GRAU_ACADEMICO'].isnull()]
if len(nul_df) > 0:
    nul_df = tratar_coluna_nula(nul_df, 'TP_GRAU_ACADEMICO', ies_df, 'categoria', 'C')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Remover aspas dos valores na coluna 'codigo'
print('Tratando os Dados...Retirando as aspas do código do rotulo')
df['CO_CINE_ROTULO'] = df['CO_CINE_ROTULO'].str.strip('"')
print('Tratando os Dados...Retirando os .0 do código do municipio')
# Remover decimal e converter para inteiro
df['CO_MUNICIPIO'] = df['CO_MUNICIPIO'].astype(int)
df['CO_CINE_ROTULO'] = df['CO_CINE_ROTULO'].str.strip('"')
# Setar 0 emn valores com NAN
print('Tratando os Dados... Setando zeros em valores com NAN')
df = seta_zero_colunas_com_nan(df)
print('Gerando Dados...Área')
# Area Geral
area_df = df[['CO_CINE_AREA_GERAL', 'NO_CINE_AREA_GERAL']].drop_duplicates()
# Renomear as colunas para cfe o Model
area_df = area_df.rename(columns={'CO_CINE_AREA_GERAL': 'codigo', 'NO_CINE_AREA_GERAL': 'nome'})
# Salvar os dados da tabela Area
salvar_bdados(area_df, Area, 'codigo')

# Area Específica
print('Gerando Dados...Área Específica')

area_e_df = df[['CO_CINE_AREA_ESPECIFICA', 'NO_CINE_AREA_ESPECIFICA', 'CO_CINE_AREA_GERAL']].drop_duplicates()
# Renomear as colunas para cfe o Model
area_e_df = area_e_df.rename(columns={'CO_CINE_AREA_ESPECIFICA': 'codigo', 'NO_CINE_AREA_ESPECIFICA': 'nome', 'CO_CINE_AREA_GERAL': 'area' })
# Salvar os dados da tabela Area Especifica
salvar_bdados(area_e_df, Area_especifica, 'codigo')

# Area Detalhada
print('Gerando Dados...Área Detalhada')
area_d_df = df[['CO_CINE_AREA_ESPECIFICA', 'NO_CINE_AREA_DETALHADA', 'CO_CINE_AREA_DETALHADA']].drop_duplicates()
# Renomear as colunas para cfe o Model
area_d_df = area_d_df.rename(columns={'CO_CINE_AREA_ESPECIFICA': 'area_especifica', 'NO_CINE_AREA_DETALHADA': 'nome', 'CO_CINE_AREA_DETALHADA': 'codigo' })
# Salvar os dados da tabela Area Detalhada
salvar_bdados(area_d_df, Area_detalhada, 'codigo')

# Curso
print('Gerando Dados...Curso')
curso_df = df[['CO_CURSO', 'NO_CURSO', 'CO_CINE_AREA_DETALHADA']].drop_duplicates()
# Renomear as colunas para cfe o Model
curso_df = curso_df.rename(columns={'CO_CURSO': 'codigo', 'NO_CURSO': 'nome', 'CO_CINE_AREA_DETALHADA': 'area_detalhada' })
# Salvar os dados da tabela Area Detalhada
salvar_bdados(curso_df, Curso, 'codigo')

# Rotulos
print('Gerando Dados...Rótulos')
rotulo_df = df[['CO_CINE_ROTULO', 'NO_CINE_ROTULO']].drop_duplicates()
# Renomear as colunas para cfe o Model
rotulo_df = rotulo_df.rename(columns={'CO_CINE_ROTULO': 'codigo', 'NO_CINE_ROTULO': 'nome'})
# Salvar os dados da tabela Cine_Rotulo
salvar_bdados(rotulo_df, Cine_rotulo, 'codigo')

# Tipo de Dimensão
print('Gerando Dados...Dimensão')
# Transformar o dicionário em um DataFrame
dimensao_df = pd.DataFrame.from_dict(tp_dimensao, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
dimensao_df = dimensao_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(dimensao_df, Tp_dimensao, 'codigo')

# Tipo de Nivel Acadêmico
print('Gerando Dados...Nível Acad')
# Transformar o dicionário em um DataFrame
nivel_df = pd.DataFrame.from_dict(tp_nivel_acad, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
nivel_df = nivel_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(nivel_df, Tp_nivel_academico, 'codigo')

# Tipo de Modalidade de Ensino
print('Gerando Dados...Modalidades')
# Transformar o dicionário em um DataFrame
modal_df = pd.DataFrame.from_dict(tp_modal, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
modal_df = modal_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(modal_df, Tp_modal_ensino, 'codigo')

# Tipo de Grau Acadêmico
print('Gerando Dados...Grau Acad')
# Transformar o dicionário em um DataFrame
grau_df = pd.DataFrame.from_dict(tp_grau_acad, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
grau_df = grau_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(grau_df, Tp_grau_academico, 'codigo')

# Tipo de Rede
print('Gerando Dados...Tipo Rede')
# Transformar o dicionário em um DataFrame
rede_df = pd.DataFrame.from_dict(tp_rede, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
rede_df = rede_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(rede_df, Tp_rede, 'codigo')

# Gravar o censo de cada ano na tabela
print('Gerando Dados...Censo')
# Remover as colunas do dataframe que não interessam mais
df = df.drop(columns=remover_cols2)
# Renomear as colunas do DataFrame de acordo com o dicionário
df = df.rename(columns=de_para_censo)
# Renomear todas as colunas para letras minúsculas
df.columns = df.columns.str.lower()
# Atribuir o indice do dataframe ao valor da coluna codigo, qdo nulo
df = df.reset_index()
# Troca o nome da primeira coluna
# Renomeando a coluna criada a partir do índice para 'id'
df.columns.values[0] = 'id'
# Conta os valores nulos em cada coluna
valores_nuls = df.isnull().sum()
# Filtra colunas com contagem de nulos maior que zero
valores_nuls_filtrado = valores_nuls[valores_nuls > 0]
# Cria um DataFrame para exibir os resultados de forma mais organizada
nulos_df = pd.DataFrame(valores_nuls_filtrado, columns=['Qtde']).reset_index()
nulos_df.columns = ['Coluna', 'Qtde']
print(nulos_df)
# Exibe o DataFrame com as contagens de valores nulos
# Salvar no Bdados os DataFrames separados
# Determinar o tamanho de cada parte
n_parts = 20
size_of_part = len(df) // n_parts
# Dividir o DataFrame em partes aproximadamente iguais
dfs_parts = [df.iloc[i*size_of_part : (i+1)*size_of_part].reset_index(drop=True) for i in range(n_parts)]
# Exibir os DataFrames separados
for i, df_part in enumerate(dfs_parts):
    print(f"\nDataFrame parte {i+1}:")
    salvar_bdados(df_part, Curso_censo, 'id')
print('Final do Processo')
