import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    COUNT(DISTINCT cc.ies) AS total_ies,
    COUNT(DISTINCT CASE WHEN toa.codigo = 1 THEN cc.ies ELSE NULL END) AS universidade,
    COUNT(DISTINCT CASE WHEN toa.codigo = 2 THEN cc.ies ELSE NULL END) AS centro_universitario,
    COUNT(DISTINCT CASE WHEN toa.codigo = 3 THEN cc.ies ELSE NULL END) AS faculdade,
    COUNT(DISTINCT CASE WHEN toa.codigo = 4 THEN cc.ies ELSE NULL END) AS instituto_federal,
    COUNT(DISTINCT CASE WHEN toa.codigo = 5 THEN cc.ies ELSE NULL END) AS cefet
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

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px', '100px', '100px', '100px', '100px', '100px', '100px']
column_names = ['Ano', 'Geral', 'Universidade', 'Centro Universitário', 'Faculdade', 'Instituto Federal', 'CEFET']
column_alignments = ['left', 'right', 'right', 'right', 'right', 'right', 'right']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'ies_ano_organizacao_academica_qtde'

# HTML para o título da tabela
html_title = """
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="7" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó por Organização Acadêmica
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
plt.figure(figsize=(10, 6), facecolor='#F0F0F0')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Gráfico total de IES por ano
sns.lineplot(data=df, x='ano', y='total_ies', marker='o', label='Total Instituições', color='#98FB98')  # Verde claro para a linha total

# Gráfico de universidades por ano
sns.lineplot(data=df, x='ano', y='universidade', marker='o', label='Universidade', color='#FF6347')  # Tomate para linha universidade

# Gráfico de centros universitários por ano
sns.lineplot(data=df, x='ano', y='centro_universitario', marker='o', label='Centro Universitário', color='#1E90FF')  # Azul dodger para linha centro_universitário

# Gráfico de faculdades por ano
sns.lineplot(data=df, x='ano', y='faculdade', marker='o', label='Faculdade', color='#FFA500')  # Laranja para linha faculdade

# Gráfico de institutos federais por ano
sns.lineplot(data=df, x='ano', y='instituto_federal', marker='o', label='Instituto Federal', color='#32CD32')  # Verde lima para linha instituto federal

# Gráfico de CEFETs por ano
sns.lineplot(data=df, x='ano', y='cefet', marker='o', label='CEFET', color='#8A2BE2')  # Azul violeta para linha cefet

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['total_ies'].iloc[i]}", (df['ano'].iloc[i], df['total_ies'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"{df['universidade'].iloc[i]}", (df['ano'].iloc[i], df['universidade'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    plt.annotate(f"{df['centro_universitario'].iloc[i]}", (df['ano'].iloc[i], df['centro_universitario'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['faculdade'].iloc[i]}", (df['ano'].iloc[i], df['faculdade'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFA500')
    plt.annotate(f"{df['instituto_federal'].iloc[i]}", (df['ano'].iloc[i], df['instituto_federal'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#32CD32')
    plt.annotate(f"{df['cefet'].iloc[i]}", (df['ano'].iloc[i], df['cefet'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#8A2BE2')

plt.xlabel('Ano')
plt.ylabel('Quantidade de instituições')
plt.title('Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó por organização acadêmica', color='#556B2F')  # Verde oliva forte para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
