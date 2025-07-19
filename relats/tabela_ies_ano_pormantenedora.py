import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# SQL para totalizar por mantenedora e ano
sql = """
SELECT 
    m.nome AS mantenedora,
    cc.ano_censo AS ano,
    COUNT(DISTINCT cc.ies) AS total_ies
FROM 
    curso_censo cc
JOIN 
    ies i ON i.codigo = cc.ies 
JOIN 
    mantenedora m ON m.codigo = i.mantenedora 
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    m.nome, cc.ano_censo
ORDER BY 
    m.nome, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Pivotando o DataFrame para mostrar as mantenedoras como linhas e anos como colunas
df_pivot = df.pivot(index='mantenedora', columns='ano', values='total_ies').fillna(0).astype(int)

# Convertendo o índice 'mantenedora' em uma coluna regular
df_pivot.reset_index(inplace=True)

# Definindo estilos e nomes das colunas
column_html = ['200px'] + ['100px'] * (len(df_pivot.columns) - 1)
column_names = ['Mantenedora'] + [str(col) for col in df_pivot.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df_pivot.columns) - 1)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó por Mantenedora
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para HTML
html_text = dataframe_to_html(df_pivot, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_nome = 'ies_ano_mantenedora_qtde'
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)

print('Tabela HTML criada com sucesso.')
