import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe

sql = """
WITH OrderedData AS (
    SELECT 
        i.nome AS nome_ies,
        i.sigla as sigla_ies,
        cc.ano_censo,
        cc.tp_modalidade_ensino
    FROM 
        curso_censo cc
    JOIN 
        ies i ON cc.ies = i.codigo
    WHERE 
        cc.municipio = 4204202 AND cc.ano_censo > 2013
    ORDER BY 
        i.nome, cc.ano_censo
)
SELECT 
    nome_ies,
    sigla_ies,
    ano_censo,
    tp_modalidade_ensino
FROM 
    OrderedData
ORDER BY 
    nome_ies;
"""

data = carregar_dataframe(sql)

# Substituindo valores nulos em sigla_ies por "-"
data['sigla_ies'] = data['sigla_ies'].fillna('-')

# Anos a serem considerados
anos = list(range(2014, 2023))

# Construindo a nova DataFrame com colunas para cada ano e modalidade
df = pd.DataFrame(data, columns=['nome_ies', 'sigla_ies'])
for ano in anos:
    df[f'{ano}_presencial'] = False
    df[f'{ano}_distancia'] = False

# Preenchendo a nova DataFrame
for index, row in data.iterrows():
    ano = row['ano_censo']
    modalidade = row['tp_modalidade_ensino']
    if modalidade == 1:
        df.loc[(df['nome_ies'] == row['nome_ies']) & (df['sigla_ies'] == row['sigla_ies']), f'{ano}_presencial'] = True
    elif modalidade == 2:
        df.loc[(df['nome_ies'] == row['nome_ies']) & (df['sigla_ies'] == row['sigla_ies']), f'{ano}_distancia'] = True

# Removendo duplicatas
df = df.drop_duplicates(subset=['nome_ies', 'sigla_ies'])

# Exportando para Excel
with pd.ExcelWriter('relatorio_ies_ofertaporanmo.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Relatorio')

    # Formatação do Excel
    workbook = writer.book
    worksheet = writer.sheets['Relatorio']

    # Formatando o cabeçalho
    header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D7E4BC', 'border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Formatando as células de presença
    presencial_format = workbook.add_format({'bg_color': '#ADD8E6', 'border': 1})  # Azul claro para presencial
    distancia_format = workbook.add_format({'bg_color': '#FFDAB9', 'border': 1})  # Laranja claro para a distância
    ambas_format = workbook.add_format({'bg_color': '#98FB98', 'border': 1})  # Verde claro para ambas
    empty_format = workbook.add_format({'border': 1})

    for row_num in range(1, len(df) + 1):
        for ano in anos:
            col_presencial = df.columns.get_loc(f'{ano}_presencial')
            col_distancia = df.columns.get_loc(f'{ano}_distancia')
            if df.iloc[row_num - 1, col_presencial] and df.iloc[row_num - 1, col_distancia]:
                worksheet.write(row_num, col_presencial, '', ambas_format)
                worksheet.write(row_num, col_distancia, '', ambas_format)
            elif df.iloc[row_num - 1, col_presencial]:
                worksheet.write(row_num, col_presencial, '', presencial_format)
            elif df.iloc[row_num - 1, col_distancia]:
                worksheet.write(row_num, col_distancia, '', distancia_format)
            else:
                worksheet.write(row_num, col_presencial, '', empty_format)
                worksheet.write(row_num, col_distancia, '', empty_format)

print("Relatório gerado com sucesso!")
