import pandas as pd

# Função para transformar os dados conforme necessário (gerar linhas para os dados que estão em colunas como "capital" e "interior"
def transform_data(df):
    data = []
    for i, row in df.iterrows():
        # Adiciona linha para a capital
        data.append([
            row['Unidade_Federacao'], 'Capital', row['Categoria_Adm'], row['esfera'],
            row['Total_Geral'], row['Total_Geral_Capital'], row['Universidades'], row['Universidades_Capital'],
            row['Centros_Universitarios'], row['Centros_Universitarios_Capital'], row['Faculdades_Integradas'], row['Faculdades_Integradas_Capital'],
            row['Faculdades_Escolas'], row['Faculdades_Escolas_Capital'], row['Centros_Educacao_Tecnologica'], row['Centros_Educacao_Tecnologica_Capital']
        ])
        # Adiciona linha para o interior
        data.append([
            row['Unidade_Federacao'], 'Interior', row['Categoria_Adm'], row['esfera'],
            row['Total_Geral'], row['Total_Geral_Interior'], row['Universidades'], row['Universidades_Interior'],
            row['Centros_Universitarios'], row['Centros_Universitarios_Interior'], row['Faculdades_Integradas'], row['Faculdades_Integradas_Interior'],
            row['Faculdades_Escolas'], row['Faculdades_Escolas_Interior'], row['Centros_Educacao_Tecnologica'], row['Centros_Educacao_Tecnologica_Interior']
        ])
    aux_df = pd.DataFrame(data)
    novas_colunas = ['uf', 'municipio', 'categoria', 'esfera', 'total_geral', 'total_local', 'universidades', 'universidades_local', 'centros_universitarios',
                     'centros_universitarios_local', 'faculdades_integradas', 'faculdades_integradas_local', 'faculdades_escolas',
                     'faculdades_escolas_local', 'centros_educacao_tecnologica', 'centros_educacao_tecnologica_local']
    aux_df.columns = novas_colunas
    return pd.DataFrame(aux_df)

def trocar_nome_capitais(trab_df):
    # Dicionário com informações sobre as unidades da federação do Brasil
    unidades_federacao = {
        "Acre": {"capital": "Rio Branco", "regiao": "Norte", "codigo_municipio": 1200401},
        "Alagoas": {"capital": "Maceió", "regiao": "Nordeste", "codigo_municipio": 2704302},
        "Amapá": {"capital": "Macapá", "regiao": "Norte", "codigo_municipio": 1600303},
        "Amazonas": {"capital": "Manaus", "regiao": "Norte", "codigo_municipio": 1302603},
        "Bahia": {"capital": "Salvador", "regiao": "Nordeste", "codigo_municipio": 2927408},
        "Ceará": {"capital": "Fortaleza", "regiao": "Nordeste", "codigo_municipio": 2304400},
        "Distrito Federal": {"capital": "Brasília", "regiao": "Centro-Oeste", "codigo_municipio": 5300108},
        "Espírito Santo": {"capital": "Vitória", "regiao": "Sudeste", "codigo_municipio": 3205309},
        "Goiás": {"capital": "Goiânia", "regiao": "Centro-Oeste", "codigo_municipio": 5208707},
        "Maranhão": {"capital": "São Luís", "regiao": "Nordeste", "codigo_municipio": 2111300},
        "Mato Grosso": {"capital": "Cuiabá", "regiao": "Centro-Oeste", "codigo_municipio": 5103403},
        "Mato Grosso do Sul": {"capital": "Campo Grande", "regiao": "Centro-Oeste", "codigo_municipio": 5002704},
        "Minas Gerais": {"capital": "Belo Horizonte", "regiao": "Sudeste", "codigo_municipio": 3106200},
        "Pará": {"capital": "Belém", "regiao": "Norte", "codigo_municipio": 1501402},
        "Paraíba": {"capital": "João Pessoa", "regiao": "Nordeste", "codigo_municipio": 2507507},
        "Paraná": {"capital": "Curitiba", "regiao": "Sul", "codigo_municipio": 4106902},
        "Pernambuco": {"capital": "Recife", "regiao": "Nordeste", "codigo_municipio": 2611606},
        "Piauí": {"capital": "Teresina", "regiao": "Nordeste", "codigo_municipio": 2211001},
        "Rio de Janeiro": {"capital": "Rio de Janeiro", "regiao": "Sudeste", "codigo_municipio": 3304557},
        "Rio Grande do Norte": {"capital": "Natal", "regiao": "Nordeste", "codigo_municipio": 2408102},
        "Rio Grande do Sul": {"capital": "Porto Alegre", "regiao": "Sul", "codigo_municipio": 4314902},
        "Rondônia": {"capital": "Porto Velho", "regiao": "Norte", "codigo_municipio": 1100205},
        "Roraima": {"capital": "Boa Vista", "regiao": "Norte", "codigo_municipio": 1400100},
        "Santa Catarina": {"capital": "Florianópolis", "regiao": "Sul", "codigo_municipio": 4205407},
        "São Paulo": {"capital": "São Paulo", "regiao": "Sudeste", "codigo_municipio": 3550308},
        "Sergipe": {"capital": "Aracaju", "regiao": "Nordeste", "codigo_municipio": 2800308},
        "Tocantins": {"capital": "Palmas", "regiao": "Norte", "codigo_municipio": 1721000}
    }
    def substituir_capital(row):
        uf = row['uf']
        cidade = row['municipio']
        if uf in unidades_federacao:
            cd_mun = str(unidades_federacao[uf]['codigo_municipio'])
            row['regiao'] = unidades_federacao[uf]['regiao']
            if cidade == 'Capital':
                row['municipio'] = unidades_federacao[uf]['capital']
                row['codigo_municipio'] = int(cd_mun)
            else:
                row['codigo_municipio'] = int(cd_mun[0:2]+ '90000')
            y = ''
        return row

    # Aplicar a função no DataFrame
    trab_df = trab_df.apply(substituir_capital, axis=1)
    x = ''
    return trab_df

file_path = 'd:/Temp/PlanilhaOrigem.xlsx'
df = pd.read_excel(file_path, sheet_name='Planilha1', skiprows=5)

# Definir novas colunas baseadas nas posições do DataFrame
columns = [
    'Unidade_Federacao', 'Categoria_Adm', 'esfera', 'Total_Geral', 'Total_Geral_Capital', 'Total_Geral_Interior',
    'Universidades', 'Universidades_Capital', 'Universidades_Interior',
    'Centros_Universitarios', 'Centros_Universitarios_Capital', 'Centros_Universitarios_Interior',
    'Faculdades_Integradas', 'Faculdades_Integradas_Capital', 'Faculdades_Integradas_Interior',
    'Faculdades_Escolas', 'Faculdades_Escolas_Capital', 'Faculdades_Escolas_Interior',
    'Centros_Educacao_Tecnologica', 'Centros_Educacao_Tecnologica_Capital', 'Centros_Educacao_Tecnologica_Interior'
]
# Atribui nomes às colunas do dataframe
df.columns = columns
# Preencher os dados da unidade da federação que estão nulas
df['Unidade_Federacao'] = df['Unidade_Federacao'].fillna(method='ffill')
# Preencher os dados da catgegoria administrativa que estão nulas
df['Categoria_Adm'] = df['Categoria_Adm'].fillna(method='ffill')

# Filtrar linhas válidas (removendo linhas que não têm dados relevantes)
df = df.dropna(subset=['Unidade_Federacao'])
df = df.dropna(subset=['Categoria_Adm'])
df = df.dropna(subset=['esfera'])
# Remover as linhas de totais
df = df[df.iloc[:, 0].apply(lambda x: 'Brasil' not in str(x))]
df = df[df.iloc[:, 0].apply(lambda x: 'Norte' not in str(x))]
df = df[df.iloc[:, 0].apply(lambda x: 'Nordeste' not in str(x))]
df = df[df.iloc[:, 0].apply(lambda x: 'Sudeste' not in str(x))]
df = df[df.iloc[:, 0].apply(lambda x: 'Sul' not in str(x))]
df = df[df.iloc[:, 0].apply(lambda x: 'Centro-Oeste' not in str(x))]

# Preencher valores nulos com zero, se necessário
df.fillna(0, inplace=True)

# Transformar os dados
trab_df = transform_data(df)
trab_df.insert(2, 'codigo_municipio', 0)
trab_df.insert(0, 'regiao', '')

trab_df = trocar_nome_capitais(trab_df)
# Exibir o DataFrame transformado
