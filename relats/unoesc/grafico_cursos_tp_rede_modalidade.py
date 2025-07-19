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
    case 
        when c.tp_rede = 1 then 'Públicas'
        else 'Privadas Sem Fins Lucrativos'
    end as rede, 
    case 
        when c.tp_modalidade_ensino = 1 then 'Presencial'
        when c.tp_modalidade_ensino = 2 then 'EAD'
        else 'Outra'
    end as modalidade,
    count(c.curso) QtdeCursos  
from curso_censo c
where c.tp_grau_academico = 2 and c.categoria in (1,2,3,5,8,9)
group by c.ano_censo, c.tp_rede, c.tp_modalidade_ensino
order by c.ano_censo, rede, modalidade
"""
df = carregar_dataframe(sql)

# Pivotando para ter colunas combinando rede e modalidade
pivot_df = df.pivot_table(index='ano', columns=['rede', 'modalidade'], values='QtdeCursos', fill_value=0).astype(int)
pivot_df.columns = [f'{rede} - {modalidade}' for rede, modalidade in pivot_df.columns]
pivot_df.reset_index(inplace=True)

# Redefinindo a lista de tamanhos para o formato HTML
tam_colunas = ['50px'] + ['120px'] * (len(pivot_df.columns) - 1)
colunas_html = ['Ano'] + list(pivot_df.columns[1:])
alinhamentos = ['left'] + ['right'] * (len(pivot_df.columns) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'cursos_tp_rede_modalidade'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"{len(pivot_df.columns)}\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Cursos de Licenciatura por Tipo de Rede e Modalidade
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style=\"background-color: #4CAF50;\">')

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
bar_width = 0.22
x = range(len(anos))

# Cores para as categorias (estilo Excel)
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000', '#00B0F0']

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
ax.set_title('Cursos de Licenciatura por Tipo de Rede e Modalidade', color='#000000', fontsize=14)
ax.set_xticks([i + bar_width * (len(categorias) / 2 - 0.5) for i in x])
ax.set_xticklabels(anos, fontsize=11)
ax.legend(loc='best', fontsize='medium', title='Rede - Modalidade')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 