import pandas as pd
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Monta o SQL
sql = """
select distinct
    c.ano_censo as ano,
    ca.codigo as categoria_codigo,
    ca.nome as categoria_nome,
    count(c.curso) QtdeCursos  
from curso_censo c
join tp_categoria_administrativa ca on ca.codigo = c.categoria
where c.tp_grau_academico = 2 and c.categoria in (1,2,3,5,8,9)
group by c.ano_censo, ca.codigo, ca.nome
order by c.ano_censo, ca.codigo
"""
df = carregar_dataframe(sql)

# Acumular categorias 5, 8 e 9 em uma só (categoria 5)
def agrupar_categorias(row):
    if row['categoria_codigo'] in [5, 8, 9]:
        return 5
    return row['categoria_codigo']

def nome_categoria(row):
    if row['categoria_codigo'] in [5, 8, 9]:
        return 'Privada Sem Fins Lucrativos'
    return row['categoria_nome']

df['categoria_codigo'] = df.apply(agrupar_categorias, axis=1)
df['categoria_nome'] = df.apply(nome_categoria, axis=1)

# Agrupar novamente somando as quantidades
agg_df = df.groupby(['ano', 'categoria_codigo', 'categoria_nome'], as_index=False)['QtdeCursos'].sum()

# Pivotando para ter categorias como colunas
pivot_df = agg_df.pivot(index='ano', columns='categoria_nome', values='QtdeCursos').fillna(0).astype(int)
pivot_df.reset_index(inplace=True)

# Redefinindo a lista de tamanhos para o formato HTML
tam_colunas = ['50px'] + ['100px'] * (len(pivot_df.columns) - 1)
colunas_html = ['Ano'] + list(pivot_df.columns[1:])
alinhamentos = ['left'] + ['right'] * (len(pivot_df.columns) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'licenciaturas_categoria_administrativa'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"{len(pivot_df.columns)}\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Licenciaturas: Qtde de Cursos por Categoria Administrativa
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = 'static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráfico de barras agrupadas (estilo Excel)
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

anos = pivot_df['ano'].astype(str)
categorias = pivot_df.columns[1:]
bar_width = 0.22  # Aumentando um pouco mais a largura das barras
x = range(len(anos))

# Cores para as categorias (estilo Excel)
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47']

for idx, cat in enumerate(categorias):
    pos = [i + idx * bar_width for i in x]
    bars = ax.bar(pos, pivot_df[cat], width=bar_width, label=cat, color=colors[idx % len(colors)], edgecolor='black')
    # Adiciona rótulo acima das barras na vertical
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=90)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Quantidade de Cursos', fontsize=12)
ax.set_title('Licenciaturas: Qtde de Cursos por Categoria Administrativa', color='#000000', fontsize=14)
ax.set_xticks([i + bar_width * (len(categorias) / 2 - 0.5) for i in x])
ax.set_xticklabels(anos, fontsize=11)  # Agora na horizontal
ax.legend(loc='best', fontsize='medium', title='Categoria')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 