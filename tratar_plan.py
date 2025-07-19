import configparser
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import Integer

def criar_conexao(modulo):
    # Recuperar config de acesso ao banco do arquivo .ini
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    # Recupera onde fica o destino dos dados do datamart
    sgdb = cfg.get(modulo, "SGDB")
    pasta_local = cfg.get(modulo,"PASTA_LOCAL")
    dbase = cfg.get(modulo,"DW")
    ecoar = cfg.get(modulo,"ECHO")
    salvarxls = cfg.get(modulo,"DESTINO")
    if ecoar == 'S':
        ecoar = True
    else:
        ecoar = False
    engine = create_engine(sgdb + ':' + pasta_local + dbase, echo=ecoar)
    bd_bi_cnx = engine.connect()
    return bd_bi_cnx, salvarxls, dbase

# Salvar dados
def salvar_dados(dados_df, nome_table, db_bi_cnx, metodo, d_type):
    # colocar as colunas do dataframe em lowercasa
    dados_df.columns = [col.lower() for col in dados_df.columns]
    # salvar o dataframe no banco de dados
    status = dados_df.to_sql(nome_table, db_bi_cnx, if_exists=metodo, index=False, dtype=d_type)
    return status

# Função para recalcular as colunas do DataFrame
def sinopse_ies_recalcular_colunas(dados_df, recalc_colunas, calculo_colunas):
    for col in recalc_colunas:
        if col in calculo_colunas:
            # Soma as colunas especificadas no dicionário para calcular o valor total
            dados_df[col] = dados_df[calculo_colunas[col]].sum(axis=1)
    return dados_df
# Tratar os dados
def sinopse_ies_preparar_dados(ano, dados_df, novas_colunas, recalcular_col, calculo_colunas, db_bi_cnx, salvarxls):
    # Insere os dados não existentes em cada um dos anos da sinopse
    for coluna in novas_colunas:
        dados_df[coluna] = 0
    # recalcular os totais, em função de algumas colunas não vierem alimentadas da tabela
    dados_df = sinopse_ies_recalcular_colunas(dados_df, recalcular_col, calculo_colunas)
    # Recalcula o indice para não sobrepor dados
    # Lista para armazenar os novos índices
    novos_indices = []
    # Iterando sobre as linhas do DataFrame
    for index, row in dados_df.iterrows():
        novo_indice = f"{row['ano']}{row['codigo_municipio']}"
        novos_indices.append(novo_indice)
    # Definindo a nova lista de índices no DataFrame
    dados_df['novo_indice'] = novos_indices
    dados_df.set_index('novo_indice', inplace=True)
    # Configurar os dados
    nome_table = 'f_ies_dados_anuais'
    d_type = {'ano': Integer(), 'codigo_municipio': Integer(), 'total_ies': Integer(), 'total_ies_publicas': Integer(),
              'ies_publicas_federais': Integer(), 'ies_publicas_estaduais': Integer(), 'ies_publicas_municipais': Integer(),
              'total_ies_privadas': Integer(), 'ies_privadas_cflucrativos' : Integer(), 'ies_privadas_sflucrativos': Integer(),
              'total_universidades': Integer(), 'total_univ_publicas': Integer(), 'univ_publicas_federais': Integer(),
              'univ_publicas_estatuais': Integer(), 'univ_publicas_municipais': Integer(), 'total_univ_privadas': Integer(),
              'univ_privadas_sflucrativos': Integer(), 'univ_privadas_cflucrativos': Integer(), 'total_cuniv': Integer(),
              'total_cuniv_publicas': Integer(), 'cuniv_federais': Integer(), 'cuniv.estatuais': Integer(), 'cuniv_municipais': Integer(),
              'total_cuniv_privadas': Integer(), 'cuniv_privados_sflucrativos': Integer(), 'cuniv_privados_cflucrativos': Integer(),
              'total_faculdades': Integer(), 'total_faculdades_publicas': Integer(), 'facul_publicas_federais': Integer(),
              'facul_publicas_estatuais': Integer(), 'facul_publicas_municipais': Integer(), 'total_facul_privadas': Integer(),
              'faculd_privadas_sflucrativos': Integer(), 'faculd_privadas_cflucrativos': Integer(), 'institutos_federais_cefets': Integer(),
              'ies_privadas': Integer(), 'univ_privadas': Integer(), 'cuniv_privadas': Integer(), 'facul_privadas': Integer()}
    metodo = 'append'
    status = salvar_dados(dados_df, nome_table, db_bi_cnx, metodo, d_type)
#    logger('I', 'Gerado a tabela de Finalidades do Inventário')


    # calcula o total de
    if ano == '2010':
        "Inserir uma série de dados"
    elif ano == '2021':
        "ooo"
    elif ano == '2022':
        "pp"
    else:
        status = ''
def sinopse_detalhada_lerplanilha(planilha, ano, aba, cablinini, cablinfim, cablindado, nrocol, novos_nomes_col):
    status = 'Erro'
    # Ler a planilha
    df = pd.read_excel(planilha, sheet_name=aba, header=None)
    # Definir os nomes das colunas com base nas linhas inicial e final recebidos por parâmetro para considerar cabeçalho (índices)
    columns = df.iloc[cablinini:cablinfim].fillna('').apply(lambda row: ' '.join(row.values.astype(str)), axis=0).str.strip()
    # Carregar os dados a partir da linha primera linha de dados (recebido por parâmetro)
    dados_df = df.iloc[cablindado:]
    # Aplicar os nomes das colunas
    dados_df.columns = columns
    # Remover as colunas com todos os valores nulos
    dados_df.dropna(axis=1, how='all', inplace=True)

    if ano in ('2021', '2022'):
        # Remover as linhas com quaisquer valores nulos entre as colunas conideradas
        dados_df = dados_df.dropna(subset=dados_df.columns[:nrocol], how='any')
    else:
        # Remover as linhas com todas as colunas com valores nulos
        dados_df  = dados_df.dropna(subset=dados_df.columns[:nrocol], how='all')
    # Remove as linhas onde na primeira coluna tem a palavra "Total"
    dados_df = dados_df[dados_df.iloc[:, 0].apply(lambda x: 'Total' not in str(x))]
    # Remove as linhas onde na segunda coluna tem a palavra "Total"
    dados_df = dados_df[dados_df.iloc[:, 1].apply(lambda x: 'Total' not in str(x))]
    # Remove as linhas onde na segunda coluna tem a palavra "Publica"
    dados_df = dados_df[dados_df.iloc[:, 1].apply(lambda x: 'Pública' not in str(x))]
    # Remove as linhas onde na segunda coluna tem a palavra "Privada"
    dados_df = dados_df[dados_df.iloc[:, 1].apply(lambda x: 'Privada' not in str(x))]
    # renomear o nome das colunas
    dados_df.columns = novos_nomes_col
    dados_df.insert(0, 'ano', ano)
    status = 'Ok'
    return status, dados_df

def modo_2014(planilha):
    status = ''
    return status



# Definir o caminho da pasta
folder_path = 'd:/Trab/INEP/Sinopses'
# Listar todos os arquivos na pasta
files_in_directory = os.listdir(folder_path)
# Filtrar apenas os arquivos com extensão .xlsx
xlsx_files = [file for file in files_in_directory if file.endswith('.xlsx')]
# Criar o banco de dados
modulo = 'BD_INEP'
bd_bi_cnx, salvarxls, dbase = criar_conexao(modulo)

anos_modal_atual = ['2021', '2022']
anos_modal_inicio = ['2014', '2015', '2016', '2017', '2018', '2019', '2020']
# nomes das colunas da tabela de IES para cada ano
nomes_col_2022 = ['regiao', 'uf', 'municipio', 'codigo_municipio', 'total_ies', 'total_ies_publicas',
                  'ies_publicas_federais', 'ies_publicas_estaduais', 'ies_publicas_municipais', 'total_ies_privadas',
                  'ies_privadas_cflucrativos', 'ies_privadas_sflucrativos', 'total_universidades', 'total_univ_publicas',
                  'univ_publicas_federais', 'univ_publicas_estatuais', 'univ_publicas_municipais', 'total_univ_privadas',
                  'univ_privadas_sflucrativos', 'univ_privadas_cflucrativos','total_cuniv', 'total_cuniv_publicas',
                  'cuniv_federais', 'cuniv.estatuais', 'cuniv_municipais', 'total_cuniv_privadas', 'cuniv_privados_sflucrativos',
                  'cuniv_privados_cflucrativos', 'total_faculdades', 'total_faculdades_publicas', 'facul_publicas_federais',
                  'facul_publicas_estatuais', 'facul_publicas_municipais', 'total_facul_privadas', 'faculd_privadas_sflucrativos',
                  'faculd_privadas_cflucrativos', 'institutos_federais_cefets']
nomes_col_2021 = ['regiao', 'uf', 'municipio', 'codigo_municipio', 'total_ies', 'ies_publicas_federais', 'ies_publicas_estaduais',
                  'ies_publicas_municipais', 'ies_privadas', 'total_universidades', 'univ_publicas_federais', 'univ_publicas_estatuais',
                  'univ_publicas_municipais', 'univ_privadas', 'total_cuniv', 'cuniv_federais', 'cuniv.estatuais', 'cuniv_municipais',
                  'cuniv_privadas', 'total_faculdades', 'facul_publicas_federais', 'facul_publicas_estatuais', 'facul_publicas_municipais',
                  'facul_privadas', 'institutos_federais_cefets']
nomes_col_2001 = ['regiao', 'cat_adm', 'esfera', 'total_ies', 'total_ies_capital', 'total_ies_interior', 'total_universidades',
                  'total_univ_capital', 'total_univ_interior', 'total_cuniv', 'total_cuniv_capital', 'total_cuniv.interior',
                  'total_faculdades', 'total_facul_capital', 'total_facul_interior', 'total_facuintegradas', 'total_facint_capital',
                  'total_facint_interior', 'total_cet', 'total_cet_capital', 'total_cet_interior']


# criando as listas com os nomes das colunas que não existem entre as diferentes listas (anos)
# Convertendo as listas em sets
set_2022 = set(nomes_col_2022)
set_2021 = set(nomes_col_2021)
# Encontrando os valores que estão em 2022 mas não em 2021
diferenca_2022_2021 = set_2022 - set_2021
# Encontrando os valores que estão em 2021 mas não em 2022
diferenca_2021_2022 = set_2021 - set_2022
# Convertendo os sets de volta para listas para facilitar a visualização
novas_col_2021 = list(diferenca_2022_2021)
novas_col_2022 = list(diferenca_2021_2022)
# colunas que precisam ser recalculadas
recalc_col_2022 = []
recalc_col_2021 = ['total_ies_publicas', 'total_ies_privadas', 'total_univ_publicas', 'total_univ_privadas',
                   'total_cuniv_publicas', 'total_cuniv_privadas', 'total_faculdades_publicas', 'total_facul_privadas']

# Criando o dicionário
calculo_colunas = {
    'total_ies_publicas': ['ies_publicas_federais', 'ies_publicas_estaduais', 'ies_publicas_municipais'],
    'total_ies_privadas': ['ies_privadas_cflucrativos', 'ies_privadas_sflucrativos', 'ies_privadas'],
    'total_univ_publicas': ['univ_publicas_federais', 'univ_publicas_estatuais', 'univ_publicas_municipais'],
    'total_univ_privadas': ['univ_privadas_sflucrativos', 'univ_privadas_cflucrativos', 'univ_privadas'],
    'total_cuniv_publicas': ['cuniv_federais', 'cuniv.estatuais', 'cuniv_municipais'],
    'total_cuniv_privadas': ['cuniv_privados_sflucrativos', 'cuniv_privados_cflucrativos', 'cuniv_privadas'],
    'total_faculdades_publicas': ['facul_publicas_federais', 'facul_publicas_estatuais', 'facul_publicas_municipais'],
    'total_facul_privadas': ['faculd_privadas_sflucrativos', 'faculd_privadas_cflucrativos', 'facul_privadas']
}

# Cria o formato do dicionário para tratar as planilhas, que são diferentes
anos = range(2001, 2022 + 1)
formato_plan11 = {}
formato_plan21 = {}
formato_plan22 = {}
formato_plan31 = {}
formato_plan32 = {}
for ano in anos:
    if ano == 2021:
        formato_plan11[str(ano)] = {
            'linha_inicial': 5,
            'linha_final': 9,
            'primeira_linha_dados': 10,
            'nro_colunas': 25,
            'nome_colunas': nomes_col_2021,
            'novas_colunas': novas_col_2021,
            'recal_colunas': recalc_col_2021
        }
    elif ano == 2022:
        formato_plan11[str(ano)] = {
            'linha_inicial': 5,
            'linha_final': 9,
            'primeira_linha_dados': 10,
            'nro_colunas': 37,
            'nome_colunas': nomes_col_2022,
            'novas_colunas': novas_col_2022,
            'recal_colunas': recalc_col_2022
        }
    else:
        formato_plan11[str(ano)] = {
            'linha_inicial': 4,
            'linha_final': 16,
            'primeira_linha_dados': 17,
            'nro_colunas': 21,
            'nome_colunas': nomes_col_2001,
            'novas_colunas': novas_col_2022,
            'recal_colunas': recalc_col_2022
        }

# Iterar sobre a lista de arquivos e chamar a função para cada um
for file in xlsx_files:
    ano = file[7:11]
    planilha = folder_path + '/' + file
    #if ano in anos_modal_atual:
    # Planilha de Instituições de Ensino Superior
    aba = '1.1'
    cablinini = formato_plan11[ano]['linha_inicial']
    cablinfim = formato_plan11[ano]['linha_final']
    cablindado = formato_plan11[ano]['primeira_linha_dados']
    nrocol = formato_plan11[ano]['nro_colunas']
    novos_nomes_col = formato_plan11[ano]['nome_colunas']
    status, dados_df = sinopse_detalhada_lerplanilha(planilha, ano, aba, cablinini, cablinfim, cablindado, nrocol, novos_nomes_col)
    if status == 'Ok':
        # Tratar os dados e gravar no banco de dados
        novas_colunas = formato_plan11[ano]['novas_colunas']
        recalcular_col = formato_plan11[ano]['recal_colunas']
        status = sinopse_ies_preparar_dados(ano, dados_df, novas_colunas, recalcular_col, calculo_colunas, bd_bi_cnx, salvarxls)
    # Ler a aba de forma de dedicação dos docentes
        aba = '2.2'
        cablinfim = 12
        cablindado = 13
        nrocol = 111
        #status = sinopse_detalhada_lerplanilha(planilha, ano, aba, cablinini, cablinfim, cablindado, nrocol, novos_nomes_col, bd_bi_cnx, salvarxls)
    else:
        status = modo_2014(planilha)


# Ler a aba de forma de dedicação dos docentes
aba = '2.2'
# Ler a planilha
df = pd.read_excel(planilha, sheet_name=aba, header=None)
# Definir os nomes das colunas com base nas linhas 6 a 13 (índices 6 a 13)
columns = df.iloc[5:12].fillna('').apply(lambda row: ' '.join(row.values.astype(str)), axis=0).str.strip()
# Carregar os dados a partir da linha 14 (índice 13)
doc_ded_df = df.iloc[13:]
# Aplicar os nomes das colunas
doc_ded_df.columns = columns
# Remover as colunas com todos os valores nulos
doc_ded_df.dropna(axis=1, how='all', inplace=True)
# Remover as linhas com quaisquer valores nulos entre as colunas A e DH
doc_ded_df = doc_ded_df.dropna(subset=doc_ded_df.columns[:111], how='any')
# Remove as linhas onde na primeira coluna tem a palavra "Total"
doc_ded_df = doc_ded_df[doc_ded_df.iloc[:, 0].apply(lambda x: 'Total' not in str(x))]
# Remove as linhas onde na segunda coluna tem a palavra "Total"
doc_ded_df = doc_ded_df[doc_ded_df.iloc[:, 1].apply(lambda x: 'Total' not in str(x))]
# renomear o nome das colunas
novos_nomes = ['Região', 'Estado', 'Município', 'Código Municipio', 'Total', 'Total Públicas', 'Públicas Federais', 'Públicas Estaduais', 'Públicas Municipais',
               'Total Privadas', 'Com Fins Lucrativos', 'Sem Fins Lucrativos', 'Total Universidades', 'Total Univ.Públicas', 'Univ.Públicas Federais',
               'Univ.Públicas Estatuais', 'Univ.Públicas Municipais', 'Total Univ.Privadas', 'Univ.Priv.Sem Fins Lucrativos', 'Univ.Priv.Com Fins Lucrativos',
               'Total CUniv', 'Total CUniv.Públicas', 'CUniv.Federais', 'CUuniv.Estatuais', 'CUniv.Municipais', 'Total CUniv.Privadas', 'CUniv.Priv.Sem Fins Lucrativos',
               'CUniv.Priv.Com Fins Lucrativos', 'Total Faculdades', 'Total Fac.Públicas', 'Fac.Públicas Federais', 'Fac.Públicas Estatuais', 'Fac.Públicas Municipais',
               'Total Fac.Privadas', 'Fac.Priv.Sem Fins Lucrativos', 'Fac.Priv.Com Fins Lucrativos', 'IFs_CEFETs']
doc_ded_df.columns = novos_nomes
doc_ded_df['Ano'] = ano
