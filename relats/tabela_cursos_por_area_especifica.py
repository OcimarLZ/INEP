import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    ae.nome as area_especifica,
    cc.ano_censo AS ano,
    count(cc.curso) as qtde_cursos   
FROM 
    curso_censo cc
JOIN area_especifica ae on ae.codigo = cc.area_especifica 
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    ae.codigo, cc.ano_censo 
ORDER BY 
    ae.codigo, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Pivotando o DataFrame para ter anos como colunas
df_pivot = df.pivot(index='area_especifica', columns='ano', values='qtde_cursos')
df_pivot = df_pivot.fillna(0).astype(int)

# Redefinindo a lista de tamanhos para o formato HTML
years = sorted(df['ano'].unique())
column_html = ['200px'] + ['100px'] * len(years)
column_names = ['Área Específica'] + [str(year) for year in years]
column_alignments = ['left'] + ['right'] * len(years)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'cursos_area_especifica_ano_qtde_pivot'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados em Chapecó por Área Específica
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot.reset_index(), column_html, column_names, column_alignments, header_style, row_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML pivotada criada com sucesso.')

# Gerando o gráfico com as 10 maiores áreas e uma linha com a soma das demais
total_cursos = df.groupby('area_especifica')['qtde_cursos'].sum().sort_values(ascending=False)
top_10_areas = total_cursos.head(10)
others_cursos = total_cursos[10:].sum()

# Filtrando dados das 10 maiores áreas e calculando "Outras"
df_top_areas = df[df['area_especifica'].isin(top_10_areas.index)]
df_others = df[~df['area_especifica'].isin(top_10_areas.index)].copy()
df_others['area_especifica'] = 'Outras'
df_others = df_others.groupby(['area_especifica', 'ano']).sum().reset_index()

df_top_areas = pd.concat([df_top_areas, df_others])

plt.figure(figsize=(12, 8), facecolor='#CCFFCC')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

for area in df_top_areas['area_especifica'].unique():
    df_area = df_top_areas[df_top_areas['area_especifica'] == area]
    if area == 'Outras':
        sns.lineplot(data=df_area, x='ano', y='qtde_cursos', marker='o', label=f'{area}', color='black')
    else:
        sns.lineplot(data=df_area, x='ano', y='qtde_cursos', marker='o', label=f'{area}')

plt.xlabel('Ano')
plt.ylabel('Quantidade de cursos ofertados')
plt.title('Evolução do número de cursos ofertados por Área Específica (Top 10 + Outras)', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
plt.grid(True)

arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
