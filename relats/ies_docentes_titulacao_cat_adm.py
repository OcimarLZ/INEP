import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    tca.nome AS categoria_adm, 
    i.ano_censo AS ano,
    SUM(i.qt_doc_ex_sem_grad) AS sem_graduacao,
    SUM(i.qt_doc_ex_grad) AS graduacao,
    SUM(i.qt_doc_ex_esp) AS especializacao,
    SUM(i.qt_doc_ex_mest) AS mestrado,
    SUM(i.qt_doc_ex_dout) AS doutorado,
    SUM(i.qt_doc_ex_titulacao_ndef) AS titulacao_ndef
FROM 
    ies_censo i
JOIN tp_categoria_administrativa tca ON tca.codigo = i.categoria 
WHERE 
    i.municipio = 4204202
GROUP BY 
    tca.nome, i.ano_censo
ORDER BY 
    tca.nome, i.ano_censo;
"""
df = carregar_dataframe(sql)

# Remover colunas onde todos os valores são zero, exceto para a coluna 'ano'
df = df.loc[:, (df != 0).any(axis=0)]

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['200px', '50px'] + ['100px'] * (len(df.columns) - 2)
column_names = ['Categoria Adm.', 'Ano'] + [col.capitalize().replace('_', ' ') for col in df.columns[2:]]
column_alignments = ['left', 'right'] + ['right'] * (len(df.columns) - 2)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'docentes_categoria_titulacao_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Docentes por Categoria Administrativa e Titulação em Chapecó
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

# Criando um gráfico de barras empilhadas para cada categoria administrativa
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

# Plotando as barras empilhadas para cada categoria
df.set_index(['categoria_adm', 'ano'], inplace=True)
df.plot(kind='bar', stacked=True, ax=ax, color=['#8B0000', '#FF4500', '#FFD700', '#32CD32', '#1E90FF', '#8A2BE2'])

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução dos Docentes por Categoria Administrativa e Titulação em Chapecó', color='#000000')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), ncol=1, fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '_stacked.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
