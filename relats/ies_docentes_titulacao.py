import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.ano_censo AS ano,
    SUM(i.qt_doc_ex_sem_grad) AS sem_graduacao,
    SUM(i.qt_doc_ex_grad) AS graduacao,
    SUM(i.qt_doc_ex_esp) AS especializacao,
    SUM(i.qt_doc_ex_mest) AS mestrado,
    SUM(i.qt_doc_ex_dout) AS doutorado,
    SUM(i.qt_doc_ex_titulacao_ndef) AS titulacao_ndef
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
column_names = ['Ano', 'Sem Graduação', 'Graduação', 'Especialização', 'Mestrado', 'Doutorado', 'Titulação Não Definida']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'docentes_por_titulacao'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução da Titulação dos Docentes em Exercício
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
plot_line(df, 'ano', 'sem_graduacao', 'Sem Graduação', '#FF6347')  # Tomate
plot_line(df, 'ano', 'graduacao', 'Graduação', '#32CD32')  # Verde Lima
plot_line(df, 'ano', 'especializacao', 'Especialização', '#1E90FF')  # Azul Dodger
plot_line(df, 'ano', 'mestrado', 'Mestrado', '#8A2BE2')  # Roxo
plot_line(df, 'ano', 'doutorado', 'Doutorado', '#48D1CC')  # Azul Escuro
plot_line(df, 'ano', 'titulacao_ndef', 'Titulação Não Definida', '#FFD700')  # Ouro

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'sem_graduacao' in df.columns:
        plt.annotate(f"{df['sem_graduacao'].iloc[i]}", (df['ano'].iloc[i], df['sem_graduacao'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')
    if 'graduacao' in df.columns:
        plt.annotate(f"{df['graduacao'].iloc[i]}", (df['ano'].iloc[i], df['graduacao'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#32CD32')
    if 'especializacao' in df.columns:
        plt.annotate(f"{df['especializacao'].iloc[i]}", (df['ano'].iloc[i], df['especializacao'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    if 'mestrado' in df.columns:
        plt.annotate(f"{df['mestrado'].iloc[i]}", (df['ano'].iloc[i], df['mestrado'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    if 'doutorado' in df.columns:
        plt.annotate(f"{df['doutorado'].iloc[i]}", (df['ano'].iloc[i], df['doutorado'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#48D1CC')
    if 'titulacao_ndef' in df.columns:
        plt.annotate(f"{df['titulacao_ndef'].iloc[i]}", (df['ano'].iloc[i], df['titulacao_ndef'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFD700')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução da Titulação dos Docentes em Exercício', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
