import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.ano_censo AS ano,
    SUM(i.qt_doc_ex_bra) AS brasileiros,
    SUM(i.qt_doc_ex_est) AS estrangeiros
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
    'brasileiros': 'int',
    'estrangeiros': 'int'
})

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano'] + [col.replace('_', ' ').capitalize() for col in df.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'evolucao_docentes_nacionalidade_ano'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução de Docentes Por Nacionalidade e por Ano em Chapecó
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

sns.lineplot(data=df, x='ano', y='brasileiros', marker='o', label='Brasileiros', color='#006400')
sns.lineplot(data=df, x='ano', y='estrangeiros', marker='o', label='Estrangeiros', color='#FF6347')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['brasileiros'].iloc[i]}", (df['ano'].iloc[i], df['brasileiros'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#006400')
    plt.annotate(f"{df['estrangeiros'].iloc[i]}", (df['ano'].iloc[i], df['estrangeiros'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução dos Docentes por Nacionalidade e Por Ano em Chapecó', color='#000000')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = f'../static/graficos/{arq_nome}.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
