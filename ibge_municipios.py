import pandas as pd
from bdados.tratar_dados_externos import salvar_bdados
from inep_models import MunicipioCenso

encode = 'ISO-8859-1'
# Definir o caminho do arquivo
file_path = 'd:/Trab/IBGE/2022_municipio.csv'

df = pd.read_csv(file_path, encoding=encode)

# Resetar o índice do DataFrame completo, concatenado com os df dos diversos anaos
df = df.reset_index(drop=True)

# Assumindo que seu DataFrame se chama 'df'
df = df.reset_index(drop=False)
df = df.rename(columns={'index': 'id'})
# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
df['ano_censo'] = 2022
df = df.rename(columns={'id_municipio': 'municipio'})
df = df.rename(columns={'taxa_alfabetizacao': 'tx_alfabetizacao'})
df = df.rename(columns={'idade_mediana': 'idade_media'})
df = df.rename(columns={'razao_sexo': 'idx_razao_sexo'})
df = df.rename(columns={'indice_envelhecimento': 'idx_envelhecimento'})
df = df.rename(columns={'populacao_indigena': 'pop_indigena'})
df = df.rename(columns={'populacao_indigena_terra_indigena': 'pop_indigena_territorio'})
df = df.rename(columns={'populacao_quilombola': 'pop_quilombola'})
df = df.rename(columns={'populacao_quilombola_territorio_quilombola': 'pop_quilombola_territorio'})
df['pop_branca'] = 0
df['pop_preta'] = 0
df['pop_parda'] = 0
df['pop_amarela'] = 0
df['pop_estrangeiros'] = 0
df = df.drop(columns='sigla_uf')
salvar_bdados(df, MunicipioCenso, 'id')

