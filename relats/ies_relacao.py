import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe

# SQL com as colunas adicionais
sql = """
SELECT 
    i.nome AS nome_ies,
    i.sigla AS sigla_ies,
    ca.nome AS categoria_administrativa,
    CASE 
        WHEN cc.tp_modalidade_ensino = 1 THEN 'Presencial'
        WHEN cc.tp_modalidade_ensino = 2 THEN 'A Distância'
    END AS modalidade
FROM 
    curso_censo cc
JOIN 
    ies i ON cc.ies = i.codigo
JOIN 
    tp_categoria_administrativa ca ON i.categoria = ca.codigo
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
ORDER BY 
    i.nome;
"""

# Carregar dados
data = carregar_dataframe(sql)

# Substituir valores nulos em sigla_ies por "-"
data['sigla_ies'] = data['sigla_ies'].fillna('-')

# Agrupar por nome da IES, sigla, sede, e categoria administrativa, concatenando as modalidades
df = (data.groupby(['nome_ies', 'sigla_ies', 'categoria_administrativa'])['modalidade']
      .apply(lambda x: ', '.join(sorted(set(x))))
      .reset_index())

# Renomeando colunas para a saída final
df.columns = ['Nome da IES', 'Sigla', 'Categoria Administrativa', 'Modalidades de Ensino']

# Exportando para Excel
with pd.ExcelWriter('relatorio_ies_detalhado.xlsx', engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Relatorio')

    # Formatação do Excel
    workbook = writer.book
    worksheet = writer.sheets['Relatorio']

    # Formatando o cabeçalho
    header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'valign': 'top', 'fg_color': '#D7E4BC', 'border': 1})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)

    # Formatando as células de conteúdo
    cell_format = workbook.add_format({'border': 1})
    for row_num in range(1, len(df) + 1):
        for col_num in range(len(df.columns)):
            worksheet.write(row_num, col_num, df.iloc[row_num - 1, col_num], cell_format)

print("Relatório gerado com sucesso!")
