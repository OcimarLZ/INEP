import pandas as pd
# Planilha de Instituições de Ensino Superior
aba = '1.1'
ano = 2020
planilha = ''
# Ler a planilha
df = pd.read_excel(planilha, sheet_name=aba, header=None)
# Definir os nomes das colunas com base nas linhas 6 a 9 (índices 5 a 8)
columns = df.iloc[5:9].fillna('').apply(lambda row: ' '.join(row.values.astype(str)), axis=0).str.strip()
# Carregar os dados a partir da linha 11 (índice 10)
ies_df = df.iloc[10:]
# Aplicar os nomes das colunas
ies_df.columns = columns
# Remover as colunas com todos os valores nulos
ies_df.dropna(axis=1, how='all', inplace=True)
# Remover as linhas com quaisquer valores nulos entre as colunas A e AK
ies_df = ies_df.dropna(subset=ies_df.columns[:37], how='any')
# Remove as linhas onde na primeira coluna tem a palavra "Total"
ies_df = ies_df[ies_df.iloc[:, 0].apply(lambda x: 'Total' not in str(x))]
# Remove as linhas onde na segunda coluna tem a palavra "Total"
ies_df = ies_df[ies_df.iloc[:, 1].apply(lambda x: 'Total' not in str(x))]
# renomear o nome das colunas
novos_nomes = ['Região', 'Estado', 'Município', 'Código Municipio', 'Total', 'Total Públicas', 'Públicas Federais', 'Públicas Estaduais', 'Públicas Municipais',
               'Total Privadas', 'Com Fins Lucrativos', 'Sem Fins Lucrativos', 'Total Universidades', 'Total Univ.Públicas', 'Univ.Públicas Federais',
               'Univ.Públicas Estatuais', 'Univ.Públicas Municipais', 'Total Univ.Privadas', 'Univ.Priv.Sem Fins Lucrativos', 'Univ.Priv.Com Fins Lucrativos',
               'Total CUniv', 'Total CUniv.Públicas', 'CUniv.Federais', 'CUuniv.Estatuais', 'CUniv.Municipais', 'Total CUniv.Privadas', 'CUniv.Priv.Sem Fins Lucrativos',
               'CUniv.Priv.Com Fins Lucrativos', 'Total Faculdades', 'Total Fac.Públicas', 'Fac.Públicas Federais', 'Fac.Públicas Estatuais', 'Fac.Públicas Municipais',
               'Total Fac.Privadas', 'Fac.Priv.Sem Fins Lucrativos', 'Fac.Priv.Com Fins Lucrativos', 'IFs_CEFETs']
ies_df.columns = novos_nomes
ies_df['Ano'] = ano

# Planilha de Docentes
aba = '2.1'
# Ler a planilha
df = pd.read_excel(planilha, sheet_name=aba, header=None)
# Definir os nomes das colunas com base nas linhas 6 a 9 (índices 5 a 8)
columns = df.iloc[5:9].fillna('').apply(lambda row: ' '.join(row.values.astype(str)), axis=0).str.strip()
# Carregar os dados a partir da linha 11 (índice 10)
doc_df = df.iloc[10:]
# Aplicar os nomes das colunas
doc_df.columns = columns
# Remover as colunas com todos os valores nulos
doc_df.dropna(axis=1, how='all', inplace=True)
# Remover as linhas com quaisquer valores nulos entre as colunas A e AK
doc_df = doc_df.dropna(subset=doc_df.columns[:37], how='any')
# Remove as linhas onde na primeira coluna tem a palavra "Total"
doc_df = doc_df[doc_df.iloc[:, 0].apply(lambda x: 'Total' not in str(x))]
# Remove as linhas onde na segunda coluna tem a palavra "Total"
doc_df = doc_df[doc_df.iloc[:, 1].apply(lambda x: 'Total' not in str(x))]
# renomear o nome das colunas
novos_nomes = ['Região', 'Estado', 'Município', 'Código Municipio', 'Total', 'Total Públicas', 'Públicas Federais', 'Públicas Estaduais', 'Públicas Municipais',
               'Total Privadas', 'Com Fins Lucrativos', 'Sem Fins Lucrativos', 'Total Universidades', 'Total Univ.Públicas', 'Univ.Públicas Federais',
               'Univ.Públicas Estatuais', 'Univ.Públicas Municipais', 'Total Univ.Privadas', 'Univ.Priv.Sem Fins Lucrativos', 'Univ.Priv.Com Fins Lucrativos',
               'Total CUniv', 'Total CUniv.Públicas', 'CUniv.Federais', 'CUuniv.Estatuais', 'CUniv.Municipais', 'Total CUniv.Privadas', 'CUniv.Priv.Sem Fins Lucrativos',
               'CUniv.Priv.Com Fins Lucrativos', 'Total Faculdades', 'Total Fac.Públicas', 'Fac.Públicas Federais', 'Fac.Públicas Estatuais', 'Fac.Públicas Municipais',
               'Total Fac.Privadas', 'Fac.Priv.Sem Fins Lucrativos', 'Fac.Priv.Com Fins Lucrativos', 'IFs_CEFETs']
doc_df.columns = novos_nomes
doc_df['Ano'] = ano
