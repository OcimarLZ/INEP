import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    'Indefinida' AS area,
    COUNT(CASE WHEN cc.area_geral = 0 THEN cc.area_geral ELSE NULL END) AS qtde_cursos
FROM curso_censo cc
WHERE cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY cc.ano_censo, area

UNION ALL

SELECT 
    cc.ano_censo AS ano,
    CASE 
        WHEN cc.area_geral = 1 THEN 'Educação'
        WHEN cc.area_geral = 2 THEN 'Artes'
        WHEN cc.area_geral = 3 THEN 'Sociais'
        WHEN cc.area_geral = 4 THEN 'Administração'
        WHEN cc.area_geral = 5 THEN 'Naturais'
        WHEN cc.area_geral = 6 THEN 'Informática'
        WHEN cc.area_geral = 7 THEN 'Engenharias'
        WHEN cc.area_geral = 8 THEN 'Agrárias'
        WHEN cc.area_geral = 9 THEN 'Saúde'
        WHEN cc.area_geral = 10 THEN 'Serviços'
        ELSE 'Outros'
    END AS area,
    COUNT(cc.area_geral) AS qtde_cursos
FROM curso_censo cc
WHERE cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY cc.ano_censo, cc.area_geral
ORDER BY ano, area;
"""
df = carregar_dataframe(sql)

# Criando a tabela pivotada com áreas nas linhas e anos nas colunas
df_pivot = df.pivot(index='area', columns='ano', values='qtde_cursos').fillna(0).astype(int)

# Configurações para exportação em HTML
years = sorted(df['ano'].unique())
column_html = ['200px'] + ['100px'] * len(years)
column_names = ['Área'] + [str(year) for year in years]
column_alignments = ['left'] + ['right'] * len(years)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'cursos_area_ano_qtde'

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

# Convertendo o DataFrame para HTML
html_text = dataframe_to_html(df_pivot.reset_index(), column_html, column_names, column_alignments, header_style, row_style)
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML pivotada criada com sucesso.')

# Criando um gráfico de linhas para mostrar a evolução dos cursos por área
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando uma linha para cada área
for area in df_pivot.index:
    sns.lineplot(data=df_pivot.loc[area], marker='o', label=area)

# Adicionando anotações para cada ponto
for area in df_pivot.index:
    for year in df_pivot.columns:
        plt.annotate(f"{df_pivot.loc[area, year]}",
                     (year, df_pivot.loc[area, year]),
                     textcoords="offset points",
                     xytext=(0, 10),
                     ha='center')

plt.xlabel('Ano')
plt.ylabel('Quantidade de cursos ofertados')
plt.title('Ensino Superior - Nível Graduação: Evolução do número de cursos ofertados por Área de Conhecimento em Chapecó', color='#000000')

# Ajuste da legenda para o lado direito
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
