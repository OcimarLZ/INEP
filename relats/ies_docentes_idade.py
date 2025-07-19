import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.ano_censo AS ano,
    SUM(i.qt_doc_ex_0_29) AS idade_0_29,
    SUM(i.qt_doc_ex_30_34) AS idade_30_34,
    SUM(i.qt_doc_ex_35_39) AS idade_35_39,
    SUM(i.qt_doc_ex_40_44) AS idade_40_44,
    SUM(i.qt_doc_ex_45_49) AS idade_45_49,
    SUM(i.qt_doc_ex_50_54) AS idade_50_54,
    SUM(i.qt_doc_ex_55_59) AS idade_55_59,
    SUM(i.qt_doc_ex_60_mais) AS idade_60_mais
FROM 
    ies_censo i
WHERE 
    i.municipio = 4204202
GROUP BY 
    i.ano_censo
ORDER BY 
    i.ano_censo;
"""
df = carregar_dataframe(sql)

# Remover colunas onde todos os valores são zero, exceto para a coluna 'ano'
df = df.loc[:, (df != 0).any(axis=0)]

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano'] + [col.capitalize().replace('_', ' ') for col in df.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'docentes_idade_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Distribuição dos Docentes por Faixa Etária em Chapecó
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
plt.figure(figsize=(10, 6), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Função para plotar uma linha, se a coluna não for zero
def plot_line(data, x, y, label, color):
    if y in data.columns:
        sns.lineplot(data=data, x=x, y=y, marker='o', label=label, color=color)

# Plotando as linhas
colors = ['#FF4500', '#32CD32', '#1E90FF', '#8A2BE2', '#FFD700', '#FF6347', '#4682B4', '#708090']
labels = ['Idade 0-29', 'Idade 30-34', 'Idade 35-39', 'Idade 40-44', 'Idade 45-49', 'Idade 50-54', 'Idade 55-59', 'Idade 60+']

for col, color, label in zip(df.columns[1:], colors, labels):
    plot_line(df, 'ano', col, label, color)

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    for col, color in zip(df.columns[1:], colors):
        plt.annotate(f"{df[col].iloc[i]}", (df['ano'].iloc[i], df[col].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color=color)

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução da Distribuição dos Docentes por Faixa Etária em Chapecó', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
