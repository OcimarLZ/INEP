import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_fem) AS ingressantes_fem,
    SUM(cc.qt_ing_masc) AS ingressantes_masc,
    SUM(cc.qt_conc_fem) AS concluintes_fem,
    SUM(cc.qt_conc_masc) AS concluintes_masc,
    SUM(cc.qt_mat_fem) AS matriculas_fem,
    SUM(cc.qt_mat_masc) AS matriculas_masc
FROM 
    curso_censo cc
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Remover colunas onde todos os valores são zero, exceto para a coluna 'ano'
df = df.loc[:, (df != 0).any(axis=0)]

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano'] + [col.replace('_', ' ').capitalize() for col in df.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'ingressantes_concluintes_matriculas_por_genero'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Ingressantes, Concluintes e Matrículas por Gênero em Chapecó
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Ajuste para garantir que o cabeçalho da tabela tenha a cor correta
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas para ingressantes, concluintes e matrículas por gênero
sns.lineplot(data=df, x='ano', y='ingressantes_fem', marker='o', color='#FF69B4', label='Ingressantes Fem')  # Rosa para linha ingressantes feminino
sns.lineplot(data=df, x='ano', y='ingressantes_masc', marker='o', color='#1E90FF', label='Ingressantes Masc')  # Azul para linha ingressantes masculino
sns.lineplot(data=df, x='ano', y='concluintes_fem', marker='o', color='#FFB6C1', label='Concluintes Fem')  # Rosa claro para linha concluintes feminino
sns.lineplot(data=df, x='ano', y='concluintes_masc', marker='o', color='#4682B4', label='Concluintes Masc')  # Azul aço para linha concluintes masculino
sns.lineplot(data=df, x='ano', y='matriculas_fem', marker='o', color='#DC143C', label='Matrículas Fem')  # Vermelho para linha matrículas feminino
sns.lineplot(data=df, x='ano', y='matriculas_masc', marker='o', color='#8B0000', label='Matrículas Masc')  # Vermelho escuro para linha matrículas masculino

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingressantes_fem'].iloc[i]}", (df['ano'].iloc[i], df['ingressantes_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF69B4')
    plt.annotate(f"{df['ingressantes_masc'].iloc[i]}", (df['ano'].iloc[i], df['ingressantes_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['concluintes_fem'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFB6C1')
    plt.annotate(f"{df['concluintes_masc'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#4682B4')
    plt.annotate(f"{df['matriculas_fem'].iloc[i]}", (df['ano'].iloc[i], df['matriculas_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#DC143C')
    plt.annotate(f"{df['matriculas_masc'].iloc[i]}", (df['ano'].iloc[i], df['matriculas_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8B0000')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução dos Totais de Ingressantes, Concluintes e Matrículas por Gênero em Chapecó', color='#000000')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize='small')  # Legenda abaixo
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
