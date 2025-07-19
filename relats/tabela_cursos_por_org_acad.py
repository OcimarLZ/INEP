import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    COUNT(CASE WHEN toa.codigo = 1 THEN cc.org_academica ELSE NULL END) AS universidade,
    COUNT(CASE WHEN toa.codigo = 2 THEN cc.org_academica ELSE NULL END) AS centro_universitario,
    COUNT(CASE WHEN toa.codigo = 3 THEN cc.org_academica ELSE NULL END) AS faculdade,
    COUNT(CASE WHEN toa.codigo = 4 THEN cc.org_academica ELSE NULL END) AS instituto_federal,
    COUNT(CASE WHEN toa.codigo = 5 THEN cc.org_academica ELSE NULL END) AS cefet
FROM 
    curso_censo cc
JOIN 
    tp_organizacao_academica toa ON cc.org_academica = toa.codigo
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
arq_nome = 'cursos_ano_organizacao_academica_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por Organização Acadêmica
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
plot_line(df, 'ano', 'universidade', 'Universidade', '#FF6347')  # Tomate para linha universidade
plot_line(df, 'ano', 'centro_universitario', 'Centro Universitário', '#1E90FF')  # Azul dodger para linha centro_universitário
plot_line(df, 'ano', 'faculdade', 'Faculdade', '#FFA500')  # Laranja para linha faculdade
plot_line(df, 'ano', 'instituto_federal', 'Instituto Federal', '#006400')  # Dark Green lima para linha instituto federal
plot_line(df, 'ano', 'cefet', 'CEFET', '#8A2BE2')  # Azul violeta para linha cefet

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'universidade' in df.columns:
        plt.annotate(f"{df['universidade'].iloc[i]}", (df['ano'].iloc[i], df['universidade'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    if 'centro_universitario' in df.columns:
        plt.annotate(f"{df['centro_universitario'].iloc[i]}", (df['ano'].iloc[i], df['centro_universitario'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    if 'faculdade' in df.columns:
        plt.annotate(f"{df['faculdade'].iloc[i]}", (df['ano'].iloc[i], df['faculdade'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFA500')
    if 'instituto_federal' in df.columns:
        plt.annotate(f"{df['instituto_federal'].iloc[i]}", (df['ano'].iloc[i], df['instituto_federal'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#006400')
    if 'cefet' in df.columns:
        plt.annotate(f"{df['cefet'].iloc[i]}", (df['ano'].iloc[i], df['cefet'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#8A2BE2')

plt.xlabel('Ano')
plt.ylabel('Quantidade de cursos ofertados')
plt.title('Ensino Superior - Nível Graduação: Evolução de cursos ofertados em Chapecó por organização acadêmica', color='#000000')  # Verde oliva forte para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
