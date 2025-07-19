import pandas as pd
from bdados.tratar_dados_externos import salvar_bdados
from inep_models import Mesorregiao, Microrregiao, Municipio, RegiaoImediata, RegiaoIntermediaria

de_para_uf = {
    '11': 'RO',
    '12': 'AC',
    '13': 'AM',
    '14': 'RR',
    '15': 'PA',
    '16': 'AP',
    '17': 'TO',
    '21': 'MA',
    '22': 'PI',
    '23': 'CE',
    '24': 'RN',
    '25': 'PB',
    '26': 'PE',
    '27': 'AL',
    '28': 'SE',
    '29': 'BA',
    '31': 'MG',
    '32': 'ES',
    '33': 'RJ',
    '35': 'SP',
    '41': 'PR',
    '42': 'SC',
    '43': 'RS',
    '50': 'MS',
    '51': 'MT',
    '52': 'GO',
    '53': 'DF'
}
soma = '+'
sim_nao = 'S'

encode = 'ISO-8859-1'
# Definir o caminho do arquivo
file_path = 'd:/Trab/IBGE/RELATORIO_DTB_BRASIL_MUNICIPIO.xlsx'

df = pd.read_excel(file_path)

# Resetar o índice do DataFrame completo, concatenado com os df dos diversos anaos
df = df.reset_index(drop=True)

# Região Intermediária
regiao_int_df = df[['regiao_intermediaria_codigo', 'regiao_intermediaria_nome', 'uf']].drop_duplicates()
regiao_int_df = regiao_int_df.rename(columns={'regiao_intermediaria_codigo': 'codigo'})
regiao_int_df = regiao_int_df.rename(columns={'regiao_intermediaria_nome': 'nome'})
regiao_int_df = regiao_int_df.rename(columns={'uf': 'estado'})
# converta a coluna 'estado' para string, caso não esteja
regiao_int_df['estado'] = regiao_int_df['estado'].astype(str)
# aplique o mapeamento
regiao_int_df['estado'] = regiao_int_df['estado'].map(de_para_uf)
salvar_bdados(regiao_int_df, RegiaoIntermediaria, 'codigo')

# Região Imediata
regiao_imed_df = df[['regiao_imediata_codigo', 'regiao_imediata_nome', 'regiao_intermediaria_codigo']].drop_duplicates()
regiao_imed_df = regiao_imed_df.rename(columns={'regiao_imediata_codigo': 'codigo'})
regiao_imed_df = regiao_imed_df.rename(columns={'regiao_intermediaria_codigo': 'regiao_intermediaria'})
regiao_imed_df = regiao_imed_df.rename(columns={'regiao_imediata_nome': 'nome'})
salvar_bdados(regiao_imed_df, RegiaoImediata, 'codigo')

# Mesorregião
mesorregiao_df = df[['mesorregiao_codigo', 'mesorregiao_nome', 'uf']].drop_duplicates()
mesorregiao_df['mesorregiao_codigo'] = mesorregiao_df['uf'].astype(str) + mesorregiao_df['mesorregiao_codigo'].astype(str)
# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
mesorregiao_df = mesorregiao_df.rename(columns={'mesorregiao_codigo': 'codigo'})
mesorregiao_df = mesorregiao_df.rename(columns={'mesorregiao_nome': 'nome'})
mesorregiao_df = mesorregiao_df.rename(columns={'uf': 'estado'})
# converta a coluna 'estado' para string, caso não esteja
mesorregiao_df['estado'] = mesorregiao_df['estado'].astype(str)
# aplique o mapeamento
mesorregiao_df['estado'] = mesorregiao_df['estado'].map(de_para_uf)
salvar_bdados(mesorregiao_df, Mesorregiao, 'codigo')

# Microrregião
microrregiao_df = df[['microrregiao_codigo', 'microrregiao_nome', 'mesorregiao_codigo', 'uf']].drop_duplicates()
microrregiao_df['microrregiao_codigo'] = microrregiao_df['uf'].astype(str) + microrregiao_df['microrregiao_codigo'].astype(str)
microrregiao_df['mesorregiao_codigo'] = microrregiao_df['uf'].astype(str) + microrregiao_df['mesorregiao_codigo'].astype(str)
microrregiao_df = microrregiao_df.rename(columns={'microrregiao_codigo': 'codigo'})
microrregiao_df = microrregiao_df.rename(columns={'microrregiao_nome': 'nome'})
microrregiao_df = microrregiao_df.rename(columns={'mesorregiao_codigo': 'mesorregiao'})
# Remove o campo uf
microrregiao_df = microrregiao_df.drop(columns={'uf'})
salvar_bdados(microrregiao_df, Microrregiao, 'codigo')

# Municipio
municipio_df = df[['municipio_codigo', 'municipio_nome', 'uf', 'mesorregiao_codigo', 'microrregiao_codigo', 'regiao_imediata_codigo', 'regiao_intermediaria_codigo']].drop_duplicates()
municipio_df['microrregiao'] = municipio_df['uf'].astype(str) + municipio_df['microrregiao_codigo'].astype(str)
municipio_df['mesorregiao'] = municipio_df['uf'].astype(str) + municipio_df['mesorregiao_codigo'].astype(str)
# Renomear a coluna 'CO_REGIAO_IES' para 'regiao'
municipio_df = municipio_df.rename(columns={'uf': 'estado'})
municipio_df = municipio_df.rename(columns={'municipio_codigo': 'codigo'})
municipio_df = municipio_df.rename(columns={'municipio_nome': 'nome'})
municipio_df = municipio_df.drop(columns={'mesorregiao_codigo'})
municipio_df = municipio_df.drop(columns={'microrregiao_codigo'})
municipio_df = municipio_df.rename(columns={'regiao_intermediaria_codigo': 'regiao_intermediaria'})
municipio_df = municipio_df.rename(columns={'regiao_imediata_codigo': 'regiao_imediata'})
# converta a coluna 'estado' para string, caso não esteja
municipio_df['estado'] = municipio_df['estado'].astype(str)
# criar as novas colunas do dataframe
municipio_df['hierarquia'] = 'P'
# aplique o mapeamento
municipio_df['estado'] = municipio_df['estado'].map(de_para_uf)
salvar_bdados(municipio_df, Municipio, 'codigo')

x = input('fasdasda')
