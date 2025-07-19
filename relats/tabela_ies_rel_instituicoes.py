from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html
import pandas as pd

# Monta o SQL
# Carregando dados de uma tabela para um DataFrame
sql = """
SELECT distinct
    cc.ano_censo,
    i.nome AS nome_ies,
    i.sigla as sigla_ies
FROM 
    curso_censo cc
JOIN 
    ies i ON cc.ies = i.codigo
WHERE 
    cc.municipio = 4204202 and cc.ano_censo > 2013
ORDER BY 
    cc.ano_censo, i.nome;
"""
df = carregar_dataframe(sql)


# Função para adicionar linhas de totais
def add_totals(df, group_column):
    new_rows = []
    for name, group in df.groupby(group_column):
        new_rows.append(group)
        total_row = pd.DataFrame({group_column: [name], 'nome_ies': [f'Total: {len(group)}']})
        new_rows.append(total_row)
    return pd.concat(new_rows).reset_index(drop=True)


df_with_totals = add_totals(df, 'ano_censo')

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px', '600px', '60px']
column_names = ['Ano', 'Nome da Instituição', 'Sigla']
column_alignments = ['left', 'left', 'left']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: #ffffff;"  # Estilo do cabeçalho
row_style = "font-size: 10px; font-family: Tahoma, sans-serif; background-color: #E8F5E9;"  # Estilo das linhas de dados
title_style = "font-size: 14px; font-family: Tahoma, sans-serif; background-color: #388E3C; color: #ffffff; text-align: center;"  # Estilo do título
total_style = "font-size: 10px; font-family: Tahoma, sans-serif; font-weight: bold; background-color: #A5D6A7;"  # Estilo das linhas de totais
arq_nome = 'ies_ano_rel_Instituicoes'


# Função para converter DataFrame para HTML com linhas de totais estilizadas
def dataframe_to_html_with_totals(df, column_html, column_names, column_alignments, header_style, row_style,
                                  total_style):
    html = "<table>"
    # Cabeçalho
    html += f"<tr><th colspan='{len(column_names)}' style='{title_style}'>Relação das Instituições de Ensino Superior no Município de Chapecó entre 2014 e 2022</th></tr>"
    html += "<tr>"
    for name, width, align in zip(column_names, column_html, column_alignments):
        html += f"<th style='{header_style} width: {width}; text-align: {align};'>{name}</th>"
    html += "</tr>"

    # Dados e totais
    for i, row in df.iterrows():
        if "Total:" in row.iloc[1]:
            html += f"<tr style='{total_style}'>"
        else:
            html += f"<tr style='{row_style}'>"

        for item in row:
            cell_style = total_style if "Total:" in row.iloc[1] else row_style
            html += f"<td style='{cell_style}'>{item}</td>"
        html += "</tr>"

    html += "</table>"
    return html


# Convertendo o DataFrame para texto HTML com linhas de totais estilizadas
html_text = dataframe_to_html_with_totals(df_with_totals, column_html, column_names, column_alignments, header_style,
                                          row_style, total_style)

arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')