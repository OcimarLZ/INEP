import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL para incluir o tipo de rede
sql = """
SELECT 
    cc.ano_censo AS ano,
    CASE 
        WHEN cc.tp_rede = '1' THEN 'Pública'
        WHEN cc.tp_rede = '2' THEN 'Privada'
        ELSE 'Outros'
    END AS tipo_rede,
    CASE 
        WHEN cc.area_geral = 0 THEN 'Indefinida'
        WHEN cc.area_geral = 1 THEN 'Educação'
        WHEN cc.area_geral = 2 THEN 'Artes'
        WHEN cc.area_geral = 3 THEN 'Sociais'
        WHEN cc.area_geral = 4 THEN 'Administração'
        WHEN cc.area_geral = 5 THEN 'Naturais'
        WHEN cc.area_geral = 6 THEN 'Informática'
        WHEN cc.area_geral = 7 THEN 'Engenharias'
        WHEN cc.area_geral = 8 THEN 'Agrárias'
        WHEN cc.area_geral = 9 THEN 'Saúde'
        WHEN cc.area_geral = 10 THEN 'Serviços'
        ELSE 'Outros'
    END AS area,
    COUNT(*) AS qtde_cursos
FROM curso_censo cc
WHERE cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY cc.ano_censo, tipo_rede, cc.area_geral
ORDER BY ano, tipo_rede, area;
"""
df = carregar_dataframe(sql)

# Convertendo a contagem de cursos para inteiros
df['qtde_cursos'] = df['qtde_cursos'].astype(int)

# Criando a tabela pivotada com áreas e tipos de rede nas linhas e anos nas colunas
df_pivot = df.pivot_table(index=['area', 'tipo_rede'], columns='ano', values='qtde_cursos', fill_value=0)

# Configurações para exportação em HTML
years = sorted(df['ano'].unique())
column_html = ['200px', '150px'] + ['100px'] * len(years)
column_names = ['Área', 'Tipo de Rede'] + [str(year) for year in years]
column_alignments = ['left', 'left'] + ['right'] * len(years)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'cursos_area_rede_ano_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 2}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por Área de Conhecimento e Tipo de Rede
        </th>
    </tr>
</table>
"""


# Convertendo o DataFrame para HTML e formatando os valores como inteiros
def dataframe_to_html_with_format(df, column_widths, column_names, column_alignments, header_style, row_style):
    styles = f"""
        <style>
            table {{width: 100%; border-collapse: collapse;}}
            th {{ background-color: #4CAF50; color: white; {header_style}}}
            td {{{row_style}}}
            tr:nth-child(even) {{background-color: #f2f2f2;}}
            tr:hover {{background-color: #ddd;}}
            .left {{text-align: left;}}
            .center {{text-align: center;}}
            .right {{text-align: right;}}
        </style>
    """

    html = "<html><head>" + styles + "</head><body>"
    html += "<table border='1'>"

    # Adicionando cabeçalho com larguras
    html += "<tr>"
    for col_name, col_align, col_width in zip(column_names, column_alignments, column_widths):
        html += f"<th class='{col_align}' style='width: {col_width};'>{col_name}</th>"
    html += "</tr>"

    # Adicionando dados e formatando como inteiros
    for _, row in df.iterrows():
        html += "<tr>"
        for i, item in enumerate(row):
            align = column_alignments[i]
            if isinstance(item, (int, float)):
                item = f"{int(item)}"  # Remover o .0 para valores inteiros
            html += f"<td class='{align}'>{item}</td>"
        html += "</tr>"

    html += "</table></body></html>"
    return html


# Convertendo o DataFrame para HTML com formatação personalizada
html_text = dataframe_to_html_with_format(df_pivot.reset_index(), column_html, column_names, column_alignments,
                                          header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML com separação por área e tipo de rede criada com sucesso, sem precisão decimal.')
