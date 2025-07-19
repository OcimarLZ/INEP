import pandas as pd
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Monta o SQL
sql = """
select 
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
    sum(c.qt_sit_trancada) QtdeTrancadas  
from curso_censo c
where c.tp_grau_academico = 2 and c.categoria in (1,2,3,5,8,9)
group by c.ano_censo, c.tp_rede, c.tp_modalidade_ensino
order by c.ano_censo, rede, modalidade
"""
df = carregar_dataframe(sql)

# Pivotando para ter colunas combinando rede e modalidade
pivot_df = df.pivot_table(index='ano', columns=['rede', 'modalidade'], values='QtdeTrancadas', fill_value=0).astype(int)
pivot_df.columns = [f'{rede} - {modalidade}' for rede, modalidade in pivot_df.columns]
pivot_df.reset_index(inplace=True)

# Redefinindo a lista de tamanhos para o formato HTML
tam_colunas = ['50px'] + ['120px'] * (len(pivot_df.columns) - 1)
colunas_html = ['Ano'] + list(pivot_df.columns[1:])
alinhamentos = ['left'] + ['right'] * (len(pivot_df.columns) - 1)
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'licenciaturas_trancadas_por_rede_modalidade'

# HTML para o título da tabela
html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"{len(pivot_df.columns)}\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Matrículas Trancadas em Licenciaturas por Tipo de Rede e Modalidade
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

# Gráfico de linhas (um para cada categoria)
fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

anos = pivot_df['ano'].astype(str)
categorias = pivot_df.columns[1:]

# Cores para as categorias (estilo Excel)
colors = ['#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000', '#00B0F0']

for idx, cat in enumerate(categorias):
    ax.plot(anos, pivot_df[cat], marker='o', label=cat, color=colors[idx % len(colors)], linewidth=2)

# --- Ajuste para evitar sobreposição de rótulos em valores iguais ---
for i, ano in enumerate(anos):
    valores_ano = [pivot_df[cat][i] for cat in categorias]
    valor_posicoes = {}
    for idx, v in enumerate(valores_ano):
        if v > 0:
            key = (ano, v)
            if key not in valor_posicoes:
                offset = 8
                valor_posicoes[key] = 1
            else:
                offset = 8 + 12 * valor_posicoes[key]
                if valor_posicoes[key] % 2 == 1:
                    offset = -offset
                valor_posicoes[key] += 1
            ax.annotate(f'{int(v)}',
                        xy=(ano, v),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

ax.set_xlabel('Ano', fontsize=12)
ax.set_ylabel('Quantidade de Matrículas Trancadas', fontsize=12)
ax.set_title('Matrículas Trancadas em Licenciaturas por Tipo de Rede e Modalidade', color='#000000', fontsize=14)
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3, fontsize='medium', title='Rede - Modalidade', frameon=False)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

# Salvando o gráfico
arq_output = 'static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close() 