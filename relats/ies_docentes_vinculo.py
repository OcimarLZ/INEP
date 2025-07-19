import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.ano_censo AS ano,
    SUM(i.qt_doc_ex_int_de) AS integral_com_dedicacao,
    SUM(i.qt_doc_ex_int_sem_de) AS integral_sem_dedicacao,
    SUM(i.qt_doc_ex_parc) AS parcial,
    SUM(i.qt_doc_ex_hor) AS horista,
    SUM(i.qt_doc_ex_dedicacao_ndef) AS dedicacao_nao_definida
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
column_names = ['Ano', 'Integral c/ DE', 'Integral s/ DE', 'Parcial', 'Horista', 'Dedicação Não Definida']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'docentes_por_tipo_vinculo'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução do Vínculo Empregatício dos Docentes em Exercício
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
plot_line(df, 'ano', 'integral_com_dedicacao', 'Integral c/ DE', '#FF6347')  # Tomate
plot_line(df, 'ano', 'integral_sem_dedicacao', 'Integral s/ DE', '#32CD32')  # Verde Lima
plot_line(df, 'ano', 'parcial', 'Parcial', '#1E90FF')  # Azul Dodger
plot_line(df, 'ano', 'horista', 'Horista', '#8A2BE2')  # Roxo
plot_line(df, 'ano', 'dedicacao_nao_definida', 'Dedicação Não Definida', '#FFD700')  # Ouro

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'integral_com_dedicacao' in df.columns:
        plt.annotate(f"{df['integral_com_dedicacao'].iloc[i]}", (df['ano'].iloc[i], df['integral_com_dedicacao'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')
    if 'integral_sem_dedicacao' in df.columns:
        plt.annotate(f"{df['integral_sem_dedicacao'].iloc[i]}", (df['ano'].iloc[i], df['integral_sem_dedicacao'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#32CD32')
    if 'parcial' in df.columns:
        plt.annotate(f"{df['parcial'].iloc[i]}", (df['ano'].iloc[i], df['parcial'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    if 'horista' in df.columns:
        plt.annotate(f"{df['horista'].iloc[i]}", (df['ano'].iloc[i], df['horista'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    if 'dedicacao_nao_definida' in df.columns:
        plt.annotate(f"{df['dedicacao_nao_definida'].iloc[i]}", (df['ano'].iloc[i], df['dedicacao_nao_definida'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFD700')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução do Vínculo Empregatício dos Docentes em Exercício', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
