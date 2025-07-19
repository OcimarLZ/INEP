import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe


sql = """
WITH OrderedData AS (
    SELECT 
        i.nome AS nome_ies,
        i.sigla as sigla_ies,
        cc.ano_censo
    FROM 
        curso_censo cc
    JOIN 
        ies i ON cc.ies = i.codigo
    WHERE 
        cc.municipio = 4204202 AND cc.ano_censo > 2013 and cc.tp_modalidade_ensino = 1 
    ORDER BY 
        i.nome, cc.ano_censo
)
SELECT 
    nome_ies,
    sigla_ies,
    ano_censo
FROM 
    OrderedData
ORDER BY 
    nome_ies;
"""

data = carregar_dataframe(sql)
# Anos a serem considerados
anos = list(range(2014, 2023))


# Substituindo valores nulos em sigla_ies por "-"
data['sigla_ies'] = data['sigla_ies'].fillna('-')


# Construindo a nova DataFrame
df = pd.DataFrame(data, columns=['nome_ies', 'sigla_ies'])
for ano in anos:
    df[ano] = False

# Preenchendo a nova DataFrame
for index, row in data.iterrows():
    ano = row['ano_censo']
    df.loc[(df['nome_ies'] == row['nome_ies']) & (df['sigla_ies'] == row['sigla_ies']), ano] = True

# Removendo duplicatas
df = df.drop_duplicates(subset=['nome_ies', 'sigla_ies'])

# Exportando para Excel
with pd.ExcelWriter('relatorio_ies_presencial.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Relatorio')

    # Formatação do Excel
    workbook = writer.book
    worksheet = writer.sheets['Relatorio']

    # Formatando o cabeçalho
    header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D7E4BC', 'border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Formatando as células de presença
    presence_format = workbook.add_format({'bg_color': '#FFDAB9', 'border': 1})
    empty_format = workbook.add_format({'border': 1})
    for row_num in range(1, len(df) + 1):
        for col_num in range(2, len(df.columns)):
            if df.iloc[row_num - 1, col_num]:
                worksheet.write(row_num, col_num, '', presence_format)
            else:
                worksheet.write(row_num, col_num, '', empty_format)

print("Relatório gerado com sucesso!")