import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_diurno) AS ingressantes_diurno,
    SUM(cc.qt_ing_noturno) AS ingressantes_noturno,
    SUM(cc.qt_conc_diurno) AS concluintes_diurno,
    SUM(cc.qt_conc_noturno) AS concluintes_noturno
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
arq_nome = 'ingressantes_concluintes_por_turno'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Ingressantes e Concluintes por Turno em Chapecó
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
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
sns.lineplot(data=df, x='ano', y='ingressantes_diurno', marker='o', color='#1E90FF', label='Ingressantes Diurno')
sns.lineplot(data=df, x='ano', y='ingressantes_noturno', marker='o', color='#FF4500', label='Ingressantes Noturno')
sns.lineplot(data=df, x='ano', y='concluintes_diurno', marker='o', color='#6495ED', label='Concluintes Diurno')
sns.lineplot(data=df, x='ano', y='concluintes_noturno', marker='o', color='#FF6347', label='Concluintes Noturno')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingressantes_diurno'].iloc[i]}",
                 (df['ano'].iloc[i], df['ingressantes_diurno'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['ingressantes_noturno'].iloc[i]}",
                 (df['ano'].iloc[i], df['ingressantes_noturno'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF4500')
    plt.annotate(f"{df['concluintes_diurno'].iloc[i]}",
                 (df['ano'].iloc[i], df['concluintes_diurno'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#6495ED')
    plt.annotate(f"{df['concluintes_noturno'].iloc[i]}",
                 (df['ano'].iloc[i], df['concluintes_noturno'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Ingressantes e Concluintes')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Ingressantes e Concluintes por Turno em Chapecó', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
