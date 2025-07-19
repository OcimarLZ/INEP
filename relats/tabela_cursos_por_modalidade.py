import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    count(cc.curso) as qtde_cursos,
    COUNT(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.ies ELSE NULL END) AS presencial,
    COUNT(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.ies ELSE NULL END) AS distancia
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
column_names = ['Ano'] + [col.capitalize().replace('_', ' ') for col in df.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'cursos_ano_modalidade_ensino_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por Modalidade de Ensino
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
plot_line(df, 'ano', 'qtde_cursos', 'Geral', '#006400')  # Tomate para linha presencial
plot_line(df, 'ano', 'presencial', 'Presencial', '#FF6347')  # Tomate para linha presencial
plot_line(df, 'ano', 'distancia', 'A Distância', '#1E90FF')  # Azul dodger para linha a distância

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'qtde_cursos' in df.columns:
        plt.annotate(f"{df['qtde_cursos'].iloc[i]}", (df['ano'].iloc[i], df['qtde_cursos'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#006400')
    if 'presencial' in df.columns:
        plt.annotate(f"{df['presencial'].iloc[i]}", (df['ano'].iloc[i], df['presencial'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    if 'a_distancia' in df.columns:
        plt.annotate(f"{df['distancia'].iloc[i]}", (df['ano'].iloc[i], df['distancia'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')

plt.xlabel('Ano')
plt.ylabel('Quantidade de cursos ofertados')
plt.title('Ensino Superior - Nível Graduação: Evolução de cursos ofertados em Chapecó por modalidade de ensino', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
