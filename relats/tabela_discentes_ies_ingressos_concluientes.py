import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.nome AS ies,
    i.sigla as sigla,
    cc.ano_censo AS ano,
    SUM(cc.qt_ing) AS ingressantes,
    SUM(cc.qt_conc) AS concluintes
FROM 
    curso_censo cc
JOIN
    ies i ON cc.ies = i.codigo
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    ies, sigla, ano_censo
ORDER BY 
    ies, sigla, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Substituindo valores nulos em sigla por "-"
df['sigla'] = df['sigla'].fillna('-')

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype({'ingressantes': 'int', 'concluintes': 'int'})

# Pivotando o DataFrame para o formato desejado
df_pivot = df.pivot_table(index=['ies', 'sigla'], columns='ano', values=['ingressantes', 'concluintes'], fill_value=0)
df_pivot.columns = [f'{col[1]}_{col[0]}' for col in df_pivot.columns]
df_pivot = df_pivot.reset_index()

# Redefinindo a lista de tamanhos para o formato HTML
years = sorted(df['ano'].unique())
column_html = ['200px', '50px'] + ['100px'] * (len(years) * 2)
column_names = ['IES', 'Sigla'] + [f'{year}_Ingressantes' for year in years] + [f'{year}_Concluintes' for year in years]
column_alignments = ['left', 'left'] + ['right'] * (len(years) * 2)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'ies_ingressos_concluintes_por_ano'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 2}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Totais de Ingressantes e Concluintes por IES em Chapecó
        </th>
    </tr>
    <tr style="background-color: #4CAF50;">
        <th rowspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">IES</th>
        <th rowspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">Sigla</th>
        {''.join([f'<th colspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">{year}</th>' for year in years])}
    </tr>
    <tr style="background-color: #4CAF50;">
        {''.join(['<th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">Ingressantes</th><th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">Concluintes</th>' for _ in years])}
    </tr>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')
