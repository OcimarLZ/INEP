import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# SQL para agrupar dados de discentes por gênero
sql = """
SELECT 
    cc.ano_censo AS ano,  
    SUM(cc.qt_vg_total) AS vagas,
    SUM(cc.qt_inscrito_total) AS inscritos,
    SUM(cc.qt_ing_masc) AS ingressos_masc, 
    SUM(cc.qt_ing_fem) AS ingressos_fem, 
    SUM(cc.qt_mat_masc) AS matriculas_masc,
    SUM(cc.qt_mat_fem) AS matriculas_fem,
    SUM(cc.qt_conc_masc) AS concluintes_masc,
    SUM(cc.qt_conc_fem) AS concluintes_fem,
FROM 
    curso_censo cc 
WHERE 
    cc.municipio = '4204202' AND cc.ano_censo > 2013 AND cc.tp_modalidade_ensino = 1
GROUP BY 
    cc.ano_censo 
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Preenchendo valores NaN com 0 e convertendo para inteiros
df = df.fillna(0).astype(int)

# Convertendo o DataFrame para o formato HTML
column_html = ['150px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano', 'Vagas', 'Inscritos', 'Ingressos Masculinos', 'Ingressos Femininos',
                'Matrículas Masculinas', 'Matrículas Femininas', 'Concluintes Masculinos', 'Concluintes Femininos',
                'Trancadas Masculinas', 'Trancadas Femininas', 'Desistentes Masculinos', 'Desistentes Femininos']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'evolucao_discentes_presencial_qtde_genero'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução dos Discentes por Gênero e Ano em Chapecó
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML de evolução dos discentes por gênero criada com sucesso.')

# Criando um gráfico de linhas para cada métrica por gênero
plt.figure(figsize=(12, 8), facecolor='#F0F0F0')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

# Plotando as linhas para cada métrica e gênero
sns.lineplot(data=df, x='ano', y='ingressos_masc', marker='o', label='Ingressos Masc', color='#1E90FF')
sns.lineplot(data=df, x='ano', y='ingressos_fem', marker='o', label='Ingressos Fem', color='#FF69B4')
sns.lineplot(data=df, x='ano', y='matriculas_masc', marker='o', label='Matrículas Masc', color='#32CD32')
sns.lineplot(data=df, x='ano', y='matriculas_fem', marker='o', label='Matrículas Fem', color='#FFD700')
sns.lineplot(data=df, x='ano', y='concluintes_masc', marker='o', label='Concluintes Masc', color='#8A2BE2')
sns.lineplot(data=df, x='ano', y='concluintes_fem', marker='o', label='Concluintes Fem', color='#FF4500')
sns.lineplot(data=df, x='ano', y='trancadas_masc', marker='o', label='Trancadas Masc', color='#9400D3')
sns.lineplot(data=df, x='ano', y='trancadas_fem', marker='o', label='Trancadas Fem', color='#FFA500')
sns.lineplot(data=df, x='ano', y='desistentes_masc', marker='o', label='Desistentes Masc', color='#2E8B57')
sns.lineplot(data=df, x='ano', y='desistentes_fem', marker='o', label='Desistentes Fem', color='#DC143C')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingressos_masc'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['ingressos_fem'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF69B4')
    plt.annotate(f"{df['matriculas_masc'].iloc[i]}", (df['ano'].iloc[i], df['matriculas_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#32CD32')
    plt.annotate(f"{df['matriculas_fem'].iloc[i]}", (df['ano'].iloc[i], df['matriculas_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFD700')
    plt.annotate(f"{df['concluintes_masc'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    plt.annotate(f"{df['concluintes_fem'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF4500')
    plt.annotate(f"{df['trancadas_masc'].iloc[i]}", (df['ano'].iloc[i], df['trancadas_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#9400D3')
    plt.annotate(f"{df['trancadas_fem'].iloc[i]}", (df['ano'].iloc[i], df['trancadas_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFA500')
    plt.annotate(f"{df['desistentes_masc'].iloc[i]}", (df['ano'].iloc[i], df['desistentes_masc'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#2E8B57')
    plt.annotate(f"{df['desistentes_fem'].iloc[i]}", (df['ano'].iloc[i], df['desistentes_fem'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#DC143C')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução dos Discentes por Gênero e Ano em Chapecó', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
plt.grid(True)

