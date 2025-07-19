import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    a.nome as area,
    cc.ano_censo AS ano,
    count(cc.curso) as qtde_cursos   
FROM 
    curso_censo cc
JOIN area a on a.codigo = cc.area_geral 
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    a.codigo, cc.ano_censo 
ORDER BY 
    a.codigo, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Pivotando o DataFrame para ter anos como colunas
df_pivot = df.pivot(index='area', columns='ano', values='qtde_cursos')
df_pivot = df_pivot.fillna(0).astype(int)  # Substitui NaN por 0 e converte para inteiros

# Redefinindo a lista de tamanhos para o formato HTML
years = sorted(df['ano'].unique())
column_html = ['200px'] + ['100px'] * len(years)
column_names = ['Área'] + [str(year) for year in years]
column_alignments = ['left'] + ['right'] * len(years)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'cursos_area_ano_qtde_pivot'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por Área de Conhecimento
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot.reset_index(), column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Ajuste para garantir que o cabeçalho da tabela tenha a cor correta
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML pivotada criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Função para plotar uma linha para cada área
areas = df['area'].unique()
for area in areas:
    df_area = df[df['area'] == area]
    sns.lineplot(data=df_area, x='ano', y='qtde_cursos', marker='o', label=f'{area}')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['qtde_cursos'].iloc[i]}",
                 (df['ano'].iloc[i], df['qtde_cursos'].iloc[i]),
                 textcoords="offset points",
                 xytext=(0, 10),
                 ha='center')

plt.xlabel('Ano')
plt.ylabel('Quantidade de cursos ofertados')
plt.title('Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados por Área de Conhecimento em Chapecó', color='#000000')  # Preto para o título

# Ajuste da legenda para o lado direito
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  # Mover legenda para o lado direito

plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()  # Ajusta automaticamente os elementos para caber na figura
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()