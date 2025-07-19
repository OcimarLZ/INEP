import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.ano_censo AS ano,
    SUM(i.qt_doc_ex_branca) AS branca,
    SUM(i.qt_doc_ex_preta) AS preta,
    SUM(i.qt_doc_ex_parda) AS parda,
    SUM(i.qt_doc_ex_amarela) AS amarela,
    SUM(i.qt_doc_ex_indigena) AS indigena,
    SUM(i.qt_doc_ex_cor_nd) AS cor_nd
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
column_names = ['Ano', 'Branca', 'Preta', 'Parda', 'Amarela', 'Indígena', 'Cor Não Definida']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'docentes_por_raca'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução dos Docentes em Exercício por Raça
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
plot_line(df, 'ano', 'branca', 'Branca', '#1E90FF')  # Azul
plot_line(df, 'ano', 'preta', 'Preta', '#FF6347')  # Tomate
plot_line(df, 'ano', 'parda', 'Parda', '#32CD32')  # Verde Lima
plot_line(df, 'ano', 'amarela', 'Amarela', '#FFD700')  # Ouro
plot_line(df, 'ano', 'indigena', 'Indígena', '#8A2BE2')  # Roxo
plot_line(df, 'ano', 'cor_nd', 'Cor Não Definida', '#8B4513')  # Marrom

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'branca' in df.columns:
        plt.annotate(f"{df['branca'].iloc[i]}", (df['ano'].iloc[i], df['branca'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    if 'preta' in df.columns:
        plt.annotate(f"{df['preta'].iloc[i]}", (df['ano'].iloc[i], df['preta'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')
    if 'parda' in df.columns:
        plt.annotate(f"{df['parda'].iloc[i]}", (df['ano'].iloc[i], df['parda'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#32CD32')
    if 'amarela' in df.columns:
        plt.annotate(f"{df['amarela'].iloc[i]}", (df['ano'].iloc[i], df['amarela'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFD700')
    if 'indigena' in df.columns:
        plt.annotate(f"{df['indigena'].iloc[i]}", (df['ano'].iloc[i], df['indigena'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    if 'cor_nd' in df.columns:
        plt.annotate(f"{df['cor_nd'].iloc[i]}", (df['ano'].iloc[i], df['cor_nd'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8B4513')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução dos Docentes em Exercício por Raça', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
