import pandas as pd
from inep_models import (Uf, Regiao, Mesorregiao, Microrregiao, Municipio, Tp_organizacao_academica, Tp_categoria_administrativa,
                         Mantenedora, Ies, Ies_censo)
from bdados.tratar_dados_externos import salvar_bdados

tp_status_juridico = {
     1: 'Federal',
     2: 'Estadual',
     3: 'Municipal',
     4: 'Privada'
}
uf = {
     1: 'Federal',
     2: 'Estadual',
     3: 'Municipal',
     4: 'Privada'
}

de_para_colunas = {'NU_ANO_CENSO': 'ano_censo',
     'NO_REGIAO_IES': 'nome',
     'CO_REGIAO_IES': 'codigo',
     'NO_UF_IES': 'nome',
     'SG_UF_IES': 'sigla',
     'CO_UF_IES': 'codigo',
     'NO_MUNICIPIO_IES': 'nome',
     'CO_MUNICIPIO_IES': 'codigo',
     'IN_CAPITAL_IES': 'capital',
     'NO_MESORREGIAO_IES': 'nome',
     'CO_MESORREGIAO_IES': 'codigo',
     'NO_MICRORREGIAO_IES': 'nome',
     'CO_MICRORREGIAO_IES': 'codigo',
     'TP_ORGANIZACAO_ACADEMICA': 'codigo',
     'TP_CATEGORIA_ADMINISTRATIVA': 'codigo',
     'NO_MANTENEDORA': 'nome',
     'CO_MANTENEDORA': 'codigo',
     'CO_IES': 'codigo',
     'NO_IES': 'nome',
     'SG_IES': 'sigla',
     'DS_ENDERECO_IES': 'endereco_logradouro',
     'DS_NUMERO_ENDERECO_IES': 'endereco_numero',
     'DS_COMPLEMENTO_ENDERECO_IES': 'endereco_complemento',
     'NO_BAIRRO_IES': 'bairro',
     'NU_CEP_IES': 'cep'}
encode = 'ISO-8859-1'
delimitador = ';'
df = pd.DataFrame()
# Definir o caminho da pasta
nros = range(2014, 2023 + 1)
for nro in nros:
     file_patch = f'd:/Trab/Geocapes/bolsas/por_ies/bolsa_por_ies_{nro}.xlsx'
     # Carregar o arquivo CSV em um DataFrame, especificando o delimitador correto
     df_parc = pd.read_csv(file_patch, delimiter=delimitador, encoding=encode)
     # Criar um dicionário de mapeamento para as colunas a serem renomeadas
     rename_dict = {col: 'QT_' + col for col in df_parc.columns if col.startswith('DOC_EX_')}
     # Adicionar as colunas específicas ao dicionário de mapeamento
     # Verificar se a coluna 'qtd_doc_total' existe no DataFrame
     if 'QT_DOCENTE_TOTAL' in df_parc.columns:
          rename_dict.update({
               'QT_DOCENTE_TOTAL': 'QT_DOC_TOTAL',
               'QT_DOCENTE_EXE': 'QT_DOC_EXE'
          })
     # Renomear as colunas usando o método rename
     df_parc = df_parc.rename(columns=rename_dict)
     df = pd.concat([df, df_parc])

# Resetar o índice do DataFrame completo, concatenado com os df dos diversos anaos
df = df.reset_index(drop=True)
# Selecionar estados distintos
uf_df = df[['UF', 'SG_UF_IES', 'CO_UF_IES', 'CO_REGIAO_IES']].drop_duplicates()
# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
uf_df = uf_df.rename(columns={'CO_REGIAO_IES': 'regiao'})
# Renomear as colunas do DataFrame de acordo com o dicionário
bd_df = uf_df.rename(columns=de_para_cadbase)
# Salvar os dados da tabela UFs
salvar_bdados(bd_df, Uf, 'sigla')

# Região
regiao_df = df[['CO_REGIAO_IES', 'NO_REGIAO_IES']].drop_duplicates()
bd_df = regiao_df.rename(columns=de_para_cadbase)
salvar_bdados(bd_df, Regiao, 'codigo')

# Mesorregião
mesorregiao_df = df[['CO_MESORREGIAO_IES', 'NO_MESORREGIAO_IES', 'SG_UF_IES', 'CO_UF_IES']].drop_duplicates()
mesorregiao_df['codigo'] = mesorregiao_df['CO_UF_IES'].astype(str) + mesorregiao_df['CO_MESORREGIAO_IES'].astype(str)
# Selecionar apenas as colunas 'codigo', 'NO_MESORREGIAO_IES' e 'SG_UF_IES'
mesorregiao_df = mesorregiao_df[['codigo', 'NO_MESORREGIAO_IES', 'SG_UF_IES']]
# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
mesorregiao_df = mesorregiao_df.rename(columns={'SG_UF_IES': 'estado'})
bd_df = mesorregiao_df.rename(columns=de_para_cadbase)
salvar_bdados(bd_df, Mesorregiao, 'codigo')

# Microrregião
microrregiao_df = df[['CO_MICRORREGIAO_IES', 'NO_MICRORREGIAO_IES', 'CO_MESORREGIAO_IES', 'SG_UF_IES', 'CO_UF_IES']].drop_duplicates()
microrregiao_df['codigo'] = microrregiao_df['CO_UF_IES'].astype(str) + microrregiao_df['CO_MICRORREGIAO_IES'].astype(str)
microrregiao_df['mesorregiao'] = microrregiao_df['CO_UF_IES'].astype(str) + microrregiao_df['CO_MESORREGIAO_IES'].astype(str)
# Selecionar apenas as colunas 'codigo', 'NO_MICRORREGIAO_IES' e 'mesorregiao'
microrregiao_df = microrregiao_df[['codigo', 'NO_MICRORREGIAO_IES', 'mesorregiao']]
bd_df = microrregiao_df.rename(columns=de_para_cadbase)
salvar_bdados(bd_df, Microrregiao, 'codigo')

# Municipio
municipio_df = df[['CO_MUNICIPIO_IES', 'NO_MUNICIPIO_IES', 'IN_CAPITAL_IES', 'SG_UF_IES', 'CO_UF_IES', 'CO_MESORREGIAO_IES', 'CO_MICRORREGIAO_IES']].drop_duplicates()
municipio_df['microrregiao'] = municipio_df['CO_UF_IES'].astype(str) + municipio_df['CO_MICRORREGIAO_IES'].astype(str)
municipio_df['mesorregiao'] = municipio_df['CO_UF_IES'].astype(str) + municipio_df['CO_MESORREGIAO_IES'].astype(str)
# Selecionar apenas as colunas 'codigo', 'NO_MESORREGIAO_IES' e 'SG_UF_IES'
municipio_df = municipio_df[['CO_MUNICIPIO_IES', 'NO_MUNICIPIO_IES', 'IN_CAPITAL_IES', 'SG_UF_IES', 'mesorregiao', 'microrregiao']]
# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
municipio_df = municipio_df.rename(columns={'SG_UF_IES': 'estado'})
bd_df = municipio_df.rename(columns=de_para_cadbase)
salvar_bdados(bd_df, Municipio, 'codigo')

# Organização acadêmica
# Transformar o dicionário em um DataFrame
tp_org_df = pd.DataFrame.from_dict(tp_org_acad, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
bd_df = tp_org_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(bd_df, Tp_organizacao_academica, 'codigo')

tp_categ_df = df[['TP_CATEGORIA_ADMINISTRATIVA']].drop_duplicates()
# Organização acadêmica
# Transformar o dicionário em um DataFrame
tp_categ_df = pd.DataFrame.from_dict(tp_categ, orient='index', columns=['nome'])
# Redefinir o índice para que a chave do dicionário seja uma coluna
bd_df = tp_categ_df.reset_index().rename(columns={'index': 'codigo'})
salvar_bdados(bd_df, Tp_categoria_administrativa, 'codigo')

mant_df = df[['CO_MANTENEDORA', 'NO_MANTENEDORA', 'NU_ANO_CENSO']].drop_duplicates()
# Marcar os registros com o maior 'NU_ANO_CENSO' em cada grupo de 'CO_MANTENEDORA' para pegar a versão mais atual dos dados
mant_df['max_ano'] = mant_df.groupby('CO_MANTENEDORA')['NU_ANO_CENSO'].transform('max')
# Filtrar para manter apenas os registros onde 'NU_ANO_CENSO' é igual a 'max_ano'
manten_df = mant_df[mant_df['NU_ANO_CENSO'] == mant_df['max_ano']]
# Remover a coluna auxiliar 'max_ano' e a do ano
manten_df = manten_df.drop(columns='NU_ANO_CENSO')
manten_df = manten_df.drop(columns='max_ano')
bd_df = manten_df.rename(columns=de_para_cadbase)
# transformar a coluna nome em letras maísculas
bd_df['nome'] = bd_df['nome'].str.upper()
salvar_bdados(bd_df, Mantenedora, 'codigo')

ies_df = df[['CO_IES', 'NO_IES', 'SG_IES', 'CO_MUNICIPIO_IES', 'CO_MANTENEDORA', 'DS_ENDERECO_IES', 'DS_NUMERO_ENDERECO_IES',
             'DS_COMPLEMENTO_ENDERECO_IES', 'NO_BAIRRO_IES', 'NU_CEP_IES', 'CO_UF_IES', 'SG_UF_IES', 'CO_MESORREGIAO_IES',
             'CO_MICRORREGIAO_IES', 'TP_ORGANIZACAO_ACADEMICA', 'TP_CATEGORIA_ADMINISTRATIVA', 'CO_REGIAO_IES', 'NU_ANO_CENSO']].drop_duplicates()
ies_df['microrregiao'] = ies_df['CO_UF_IES'].astype(str) + ies_df['CO_MICRORREGIAO_IES'].astype(str)
ies_df['mesorregiao'] = ies_df['CO_UF_IES'].astype(str) + ies_df['CO_MESORREGIAO_IES'].astype(str)
ies_df = ies_df.rename(columns={'SG_UF_IES': 'estado'})
ies_df = ies_df.rename(columns={'CO_MUNICIPIO_IES': 'municipio'})
ies_df = ies_df.rename(columns={'CO_MANTENEDORA': 'mantenedora'})
ies_df = ies_df.rename(columns={'TP_ORGANIZACAO_ACADEMICA': 'org_academica'})
ies_df = ies_df.rename(columns={'TP_CATEGORIA_ADMINISTRATIVA': 'categoria'})
ies_df = ies_df.rename(columns={'CO_REGIAO_IES': 'regiao'})
# Remover a coluna antoigas de meso e microrregiao
ies_df = ies_df.drop(columns='CO_MESORREGIAO_IES')
ies_df = ies_df.drop(columns='CO_MICRORREGIAO_IES')
ies_df = ies_df.drop(columns='CO_UF_IES')
# Marcar os registros com o maior 'NU_ANO_CENSO' em cada grupo de 'CO_MANTENEDORA' para pegar a versão mais atual dos dados
ies_df['max_ano'] = ies_df.groupby('CO_IES')['NU_ANO_CENSO'].transform('max')
# Filtrar para manter apenas os registros onde 'NU_ANO_CENSO' é igual a 'max_ano'
iesf_df = ies_df[ies_df['NU_ANO_CENSO'] == ies_df['max_ano']]
# Remover a coluna auxiliar 'max_ano' e a do ano
iesf_df = iesf_df.drop(columns='NU_ANO_CENSO')
iesf_df = iesf_df.drop(columns='max_ano')
bd_df = iesf_df.rename(columns=de_para_cadbase)
# transformar a coluna nome em letras maísculas
bd_df['nome'] = bd_df['nome'].str.upper()
salvar_bdados(bd_df, Ies, 'codigo')

# Carregar os dados de censo das ies em cada ano
ies_censo_df = df.rename(columns=de_para_cadies)
# Renomear as colunas que começam com 'qt_' ou 'in_'
ies_censo_df.columns = [col.lower() if col.startswith('QT_') or col.startswith('IN_') else col for col in ies_censo_df.columns]
# Filtrar as colunas que não começam com 'CO_' ou 'NO_'
colunas_to_keep = [col for col in ies_censo_df.columns if not (col.startswith('CO_') or col.startswith('NO_') or col.startswith('SG_') or col.startswith('DS_') or col.startswith('NU_'))]
# Manter apenas as colunas filtradas
bd_df = ies_censo_df[colunas_to_keep]
bd_df = bd_df.drop(columns='in_capital_ies')
# Adiciona as colunas que foram colocados para uso dos anos anteriores, para dados sem classificação por raça, cor, titulação, etc (para os dados anteriores a 2009)
novas_cols = ['qt_tec_titulacao_ndef', 'qt_doc_ex_genero_ndef', 'qt_doc_ex_titulacao_ndef', 'qt_doc_ex_dedicacao_ndef', 'qt_doc_ex_idade_ndef', 'qt_doc_ex_raca_ndef', 'qt_doc_ex_nacional_ndef']
# Adicionar novas colunas ao DataFrame com valor inicial 0
for col in novas_cols:
    bd_df[col] = 0
# Resetando o índice para transformar o índice na primeira coluna
bd_df = bd_df.reset_index()
# Troca o nome da primeira coluna
# Renomeando a coluna criada a partir do índice para 'id'
bd_df.columns.values[0] = 'id'
# Salvar os dados da ies_censo
salvar_bdados(bd_df, Ies_censo, 'id')
