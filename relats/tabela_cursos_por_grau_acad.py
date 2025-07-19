import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    COUNT(CASE WHEN tga.codigo = 0 THEN cc.tp_grau_academico ELSE NULL END) AS indefinido,
    COUNT(CASE WHEN tga.codigo = 1 THEN cc.tp_grau_academico ELSE NULL END) AS bacharelado,
    COUNT(CASE WHEN tga.codigo = 2 THEN cc.tp_grau_academico ELSE NULL END) AS licenciatura,
    COUNT(CASE WHEN tga.codigo = 3 THEN cc.tp_grau_academico ELSE NULL END) AS tecnológico,
    COUNT(CASE WHEN tga.codigo = 4 THEN cc.tp_grau_academico ELSE NULL END) AS bacharel_lic
FROM 
    curso_censo cc
JOIN 
    tp_grau_academico tga ON cc.tp_grau_academico = tga.codigo
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
arq_nome = 'cursos_ano_grau_academico_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por Grau Acadêmico
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
plot_line(df, 'ano', 'bacharelado', 'Bacharelado', '#FF6347')  # Tomate para linha bacharelado
plot_line(df, 'ano', 'licenciatura', 'Licenciatura', '#1E90FF')  # Azul dodger para linha licenciatura
plot_line(df, 'ano', 'tecnológico', 'Tecnológico', '#32CD32')  # Verde lima para linha tecnologia
plot_line(df, 'ano', 'indefinido', 'Não Identificado', '#48D1CC')  # Verde lima para linha tecnologia
plot_line(df, 'ano', 'bacharel_lic', 'Bacharelado e Licenciatura', '#1E90FF')  # Verde lima para linha tecnologia

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'bacharelado' in df.columns:
        plt.annotate(f"{df['bacharelado'].iloc[i]}", (df['ano'].iloc[i], df['bacharelado'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    if 'licenciatura' in df.columns:
        plt.annotate(f"{df['licenciatura'].iloc[i]}", (df['ano'].iloc[i], df['licenciatura'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    if 'tecnológico' in df.columns:
        plt.annotate(f"{df['tecnológico'].iloc[i]}", (df['ano'].iloc[i], df['tecnológico'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#32CD32')
    if 'bacharel_lic' in df.columns:
        plt.annotate(f"{df['bacharel_lic'].iloc[i]}", (df['ano'].iloc[i], df['bacharel_lic'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    if 'indefinido' in df.columns:
        plt.annotate(f"{df['indefinido'].iloc[i]}", (df['ano'].iloc[i], df['indefinido'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#48D1CC')

plt.xlabel('Ano')
plt.ylabel('Quantidade de cursos ofertados')
plt.title('Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por grau acadêmico', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
