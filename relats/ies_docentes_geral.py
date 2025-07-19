import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.ano_censo AS ano,
    SUM(i.qt_doc_total) AS total_docentes,
    SUM(i.qt_doc_exe) AS docentes_em_exercicio,
    (SUM(i.qt_doc_total) - SUM(i.qt_doc_exe)) AS docentes_afastados,
    SUM(i.qt_doc_ex_femi) AS docentes_femininos,
    SUM(i.qt_doc_ex_masc) AS docentes_masculinos
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

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype({
    'total_docentes': 'int',
    'docentes_em_exercicio': 'int',
    'docentes_afastados': 'int',
    'docentes_femininos': 'int',
    'docentes_masculinos': 'int'
})

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano'] + [col.replace('_', ' ').capitalize() for col in df.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'evolucao_docentes_ano'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução do Total de Docentes por Ano em Chapecó
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
arq_output = f'../static/tabelas/{arq_nome}.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico com os dados agregados por ano
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

sns.lineplot(data=df, x='ano', y='total_docentes', marker='o', label='Total Docentes', color='#006400')
sns.lineplot(data=df, x='ano', y='docentes_em_exercicio', marker='o', label='Em Exercício', color='#FF6347')
sns.lineplot(data=df, x='ano', y='docentes_afastados', marker='o', label='Afastados', color='#8A2BE2')
sns.lineplot(data=df, x='ano', y='docentes_femininos', marker='o', label='Femininos', color='#1E90FF')
sns.lineplot(data=df, x='ano', y='docentes_masculinos', marker='o', label='Masculinos', color='#8A2BE2')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['total_docentes'].iloc[i]}", (df['ano'].iloc[i], df['total_docentes'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#006400')
    plt.annotate(f"{df['docentes_em_exercicio'].iloc[i]}", (df['ano'].iloc[i], df['docentes_em_exercicio'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')
    plt.annotate(f"{df['docentes_afastados'].iloc[i]}", (df['ano'].iloc[i], df['docentes_afastados'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    plt.annotate(f"{df['docentes_femininos'].iloc[i]}", (df['ano'].iloc[i], df['docentes_femininos'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['docentes_masculinos'].iloc[i]}", (df['ano'].iloc[i], df['docentes_masculinos'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução dos Docentes por Ano em Chapecó', color='#000000')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = f'../static/graficos/{arq_nome}.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
