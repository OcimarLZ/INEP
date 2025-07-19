import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL para dados dos discentes
sql = """
SELECT 
    cc.ano_censo AS ano,  
    SUM(cc.qt_vg_total) AS vagas,
    SUM(cc.qt_inscrito_total) AS inscritos,
    SUM(cc.qt_ing) AS ingressos, 
    SUM(cc.qt_mat) AS matriculas,
    SUM(cc.qt_conc) AS concluintes,
    SUM(cc.qt_sit_trancada) AS trancadas,
    SUM(cc.qt_sit_desvinculado) AS desistentes
FROM 
    curso_censo cc 
WHERE 
    cc.municipio = '4204202'
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
column_names = ['Ano', 'Vagas', 'Inscritos', 'Ingressos', 'Matrículas', 'Concluintes', 'Trancadas', 'Desistentes']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'evolucao_discentes_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução dos Discentes por Ano em Chapecó
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
print('Tabela HTML de evolução dos discentes criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(10, 6), facecolor='#F0F0F0')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

# Plotando as linhas para cada métrica
sns.lineplot(data=df, x='ano', y='vagas', marker='o', label='Vagas', color='#4B0082')
sns.lineplot(data=df, x='ano', y='inscritos', marker='o', label='Inscritos', color='#FF4500')
sns.lineplot(data=df, x='ano', y='ingressos', marker='o', label='Ingressos', color='#1E90FF')
sns.lineplot(data=df, x='ano', y='matriculas', marker='o', label='Matrículas', color='#32CD32')
sns.lineplot(data=df, x='ano', y='concluintes', marker='o', label='Concluintes', color='#FFD700')
sns.lineplot(data=df, x='ano', y='trancadas', marker='o', label='Trancadas', color='#FF69B4')
sns.lineplot(data=df, x='ano', y='desistentes', marker='o', label='Desistentes', color='#DC143C')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['vagas'].iloc[i]}", (df['ano'].iloc[i], df['vagas'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#4B0082')
    plt.annotate(f"{df['inscritos'].iloc[i]}", (df['ano'].iloc[i], df['inscritos'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF4500')
    plt.annotate(f"{df['ingressos'].iloc[i]}", (df['ano'].iloc[i], df['ingressos'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['matriculas'].iloc[i]}", (df['ano'].iloc[i], df['matriculas'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#32CD32')
    plt.annotate(f"{df['concluintes'].iloc[i]}", (df['ano'].iloc[i], df['concluintes'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFD700')
    plt.annotate(f"{df['trancadas'].iloc[i]}", (df['ano'].iloc[i], df['trancadas'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF69B4')
    plt.annotate(f"{df['desistentes'].iloc[i]}", (df['ano'].iloc[i], df['desistentes'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#DC143C')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução dos Discentes por Ano em Chapecó', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  # Ajustando a posição da legenda
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()

print('Gráfico de evolução dos discentes criado com sucesso.')
