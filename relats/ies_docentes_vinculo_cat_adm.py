import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL para considerar anos maiores que 2013
sql = """
SELECT 
    i.ano_censo AS ano,
    tca.nome AS categoria_adm, 
    SUM(i.qt_doc_ex_int_de) AS integral_de,
    SUM(i.qt_doc_ex_int_sem_de) AS integral_sem_de,
    SUM(i.qt_doc_ex_parc) AS parcial,
    SUM(i.qt_doc_ex_hor) AS horista
FROM 
    ies_censo i
JOIN tp_categoria_administrativa tca on tca.codigo = i.categoria 
WHERE 
    i.municipio = 4204202 AND i.ano_censo > 2013
GROUP BY 
    i.ano_censo, tca.nome
ORDER BY 
    i.ano_censo, tca.nome;
"""
df = carregar_dataframe(sql)

# Remover colunas onde todos os valores são zero
df = df.loc[:, (df != 0).any(axis=0)]

# Substituindo valores nulos por 0
df = df.fillna(0)

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['100px', '150px'] + ['100px'] * (len(df.columns) - 2)
column_names = ['Ano', 'Categoria Adm'] + [col.replace('_', ' ').capitalize() for col in df.columns[2:]]
column_alignments = ['right', 'left'] + ['right'] * (len(df.columns) - 2)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'docentes_ano_categoria_adm_vinculo'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução dos Docentes por Ano e Categoria Administrativa (A partir de 2014)
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Transformando o DataFrame para plotar gráfico
df_melted = df.melt(id_vars=['ano', 'categoria_adm'], var_name='vinculo', value_name='quantidade')

# Criando um gráfico de barras empilhadas para cada ano e categoria administrativa
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
sns.barplot(data=df_melted, x='ano', y='quantidade', hue='categoria_adm', palette='Set2')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Docentes')
plt.title('Evolução dos Docentes por Ano e Categoria Administrativa (A partir de 2014)', color='#000000')
plt.legend(title='Categoria Administrativa', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
