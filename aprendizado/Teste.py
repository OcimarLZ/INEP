import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo,
    oa.nome, 
    COUNT(DISTINCT cc.ies) AS total_ies
FROM 
    curso_censo cc
JOIN 
    tp_organizacao_academica oa on oa.codigo = cc.org_academica 
WHERE 
    cc.municipio = 4204202 and cc.ano_censo > 2013
GROUP BY 
    cc.ano_censo, cc.org_academica 
ORDER BY 
    cc.ano_censo, cc.org_academica;
"""
# Carregando dados de uma tabela para um DataFrame
df = carregar_dataframe(sql)

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px', '600px', '100px']
column_names = ['Ano', 'Organização Acadêmica', 'Instituições']
column_alignments = ['left', 'left', 'right']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: #ffffff;"  # Estilo do cabeçalho
row_style = "font-size: 10px; font-family: Tahoma, sans-serif; background-color: #E8F5E9;"  # Estilo das linhas de dados
title_style = "font-size: 14px; font-family: Tahoma, sans-serif; background-color: #388E3C; color: #ffffff; text-align: center;"  # Estilo do título
total_style = "font-size: 10px; font-family: Tahoma, sans-serif; background-color: #A5D6A7; font-weight: bold;"  # Estilo das linhas de totais
arq_nome = 'qtde_ies_ano_por_orgacad'

def montar_html_com_totais(df, column_html, column_names, column_alignments, header_style, row_style,
                           title_style, total_style):
    html = "<table>"
    # Cabeçalho
    html += f"<tr><th colspan='{len(column_names)}' style='{title_style}'>Totais das Ensino Superior no Município de Chapecó por Tipo de Organização Acadêmica</th></tr>"
    html += "<tr>"
    for name, width, align in zip(column_names, column_html, column_alignments):
        html += f"<th style='{header_style} width: {width}; text-align: {align};'>{name}</th>"
    html += "</tr>"
    # Dados
    previous_year = None
    year_total = 0
    for i, row in df.iterrows():
        current_year = row['ano_censo']
        if previous_year is not None and current_year != previous_year:
            html += f"<tr style='{total_style}'>"
            html += f"<td colspan='2' style='text-align: right;'>Total para {previous_year}</td>"
            html += f"<td style='text-align: right;'>{year_total}</td>"
            html += "</tr>"
            year_total = 0

        html += f"<tr style='{row_style}'>"
        for item, align in zip(row, column_alignments):
            html += f"<td style='text-align: {align};'>{item}</td>"
        html += "</tr>"

        year_total += row['total_ies']
        previous_year = current_year

    # Adiciona o total para o último ano
    if previous_year is not None:
        html += f"<tr style='{total_style}'>"
        html += f"<td colspan='2' style='text-align: right;'>Total para {previous_year}</td>"
        html += f"<td style='text-align: right;'>{year_total}</td>"
        html += "</tr>"

    html += "</table>"
    return html

# Convertendo o DataFrame para texto HTML com linhas de totais estilizadas
html_text = montar_html_com_totais(df, column_html, column_names, column_alignments, header_style, row_style,
                                   title_style, total_style)
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn
plt.figure(figsize=(10, 6))
lineplot_cursos = sns.lineplot(data=df, x='ano_censo', y='total_ies', hue='nome', marker='o')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['total_ies'].iloc[i]}", (df['ano_censo'].iloc[i], df['total_ies'].iloc[i]),
                 textcoords="offset points", xytext=(0, 10), ha='center')

plt.xlabel('Ano Censo')
plt.ylabel('Instituições')
plt.title('Evolução do número de instituições de ensino por organização acadêmica em Chapecó entre 2014 e 2022',
          fontsize=14, color='#388E3C', fontname='Tahoma', ha='center')
plt.legend(title='Organização Acadêmica')
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output)
plt.show()
plt.close()