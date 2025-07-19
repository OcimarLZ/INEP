import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL para obter as 7 IES com mais cursos presenciais somados de 2014 a 2023
sql_top_7 = """
SELECT 
    i.nome AS ies,
    count(cc.curso) AS total_cursos
FROM 
    curso_censo cc
JOIN 
    ies i ON cc.ies = i.codigo
WHERE 
    cc.municipio = 4204202 AND cc.tp_modalidade_ensino = 2 AND cc.ano_censo BETWEEN 2014 AND 2023
GROUP BY 
    i.nome
ORDER BY 
    total_cursos DESC
LIMIT 7
"""
top_7_df = carregar_dataframe(sql_top_7)
top_7_instituicoes = top_7_df['ies'].tolist()

# SQL principal para a evolução ano a ano dos cursos das top 7 IES
sql = f"""
SELECT 
    i.nome AS ies,
    cc.ano_censo AS ano,
    COUNT(cc.curso) AS cursos_ofertados,
    sum(cc.qt_vg_total) as vagas
FROM 
    curso_censo cc
JOIN 
    ies i ON cc.ies = i.codigo
WHERE 
    cc.municipio = 4204202 AND cc.tp_modalidade_ensino = 2 
    AND cc.ano_censo BETWEEN 2014 AND 2023 
    AND i.nome IN ({', '.join(f"'{ies}'" for ies in top_7_instituicoes)})
GROUP BY 
    i.nome, cc.ano_censo
ORDER BY 
    i.nome, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Pivotando o DataFrame para ter uma visualização ano a ano dos cursos por ies
df_pivot = df.pivot(index='ies', columns='ano', values='cursos_ofertados').fillna(0).astype(int)

# Definindo colunas e estilo para o HTML
years = sorted(df['ano'].unique())
column_html = ['100px'] + ['100px'] * len(years)
column_alignments = ['left'] + ['right'] * len(years)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'evolucao_cursos_top_7_ead'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Cursos Ofertados (Modalidade EAD) das Top 7 IES em Chapecó (2014-2023)
        </th>
    </tr>
    <tr style="background-color: #4CAF50;">
        <th rowspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">ies</th>
        {''.join([f'<th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">{year}</th>' for year in years])}
    </tr>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot.reset_index(), column_html, [], column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')
