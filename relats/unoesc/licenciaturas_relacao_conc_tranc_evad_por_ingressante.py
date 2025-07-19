import pandas as pd
import matplotlib.pyplot as plt
import itertools
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Monta o SQL
sql = """
SELECT
  c.ano_censo AS ano,
  CASE WHEN c.tp_rede = 1 THEN 'Públicas' ELSE 'Privadas Sem Fins Lucrativos' END AS rede,
  CASE 
    WHEN c.tp_modalidade_ensino = 1 THEN 'Presencial'
    WHEN c.tp_modalidade_ensino = 2 THEN 'EAD'
    ELSE 'Outra'
  END AS modalidade,
  SUM(c.qt_ing) AS QtdeIngressantes,
  SUM(c.qt_sit_trancada) AS QtdeTrancados,
  SUM(c.qt_conc) AS QtdeConcluintes,
  SUM(c.qt_sit_desvinculado + c.qt_sit_falecido + c.qt_sit_transferido) AS QtdeEvadidos
FROM curso_censo c
WHERE c.tp_grau_academico = 2 AND c.categoria IN (1,2,3,5,8,9)
GROUP BY c.ano_censo, c.tp_rede, c.tp_modalidade_ensino
ORDER BY c.ano_censo, rede, modalidade
"""
df = carregar_dataframe(sql)

# Calcula os percentuais
for col in ['QtdeConcluintes', 'QtdeTrancados', 'QtdeEvadidos']:
    df[col + '_perc'] = (df[col] / df['QtdeIngressantes'] * 100).round(2)

# Prepara DataFrame para tabela
pivot_df = df[['ano', 'rede', 'modalidade', 'QtdeConcluintes_perc', 'QtdeTrancados_perc', 'QtdeEvadidos_perc']].copy()

# Monta tabela HTML
colunas_html = ['Ano', 'Rede', 'Modalidade', '% Concluintes', '% Trancados', '% Evadidos']
tam_colunas = ['50px', '120px', '100px', '100px', '100px', '100px']
alinhamentos = ['left', 'left', 'left', 'right', 'right', 'right']
cabecalho_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
linha_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'licenciaturas_relacao_conc_tranc_evad_por_ingressante'

html_title = f"""
<table style=\"width: 100%; border-collapse: collapse;\">
    <tr style=\"background-color: #2E7D32;\">
        <th colspan=\"6\" style=\"font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;\">
            Relação (%) de Concluintes, Trancados e Evadidos sobre Ingressantes em Licenciaturas por Tipo de Rede e Modalidade
        </th>
    </tr>
</table>
"""

html_text = dataframe_to_html(pivot_df, tam_colunas, colunas_html, alinhamentos, cabecalho_style, linha_style)
html_text = html_title + html_text
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = 'static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w', encoding='utf-8') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Gráficos separados para EAD e Presencial
modalidades_plot = ['EAD', 'Presencial']
labels = {'QtdeConcluintes_perc': '% Concluintes', 'QtdeTrancados_perc': '% Trancados', 'QtdeEvadidos_perc': '% Evadidos'}
linestyles = {'QtdeConcluintes_perc': '-', 'QtdeTrancados_perc': '--', 'QtdeEvadidos_perc': ':'}
# Paleta grande de cores para garantir variedade
palette = [
    '#4472C4', '#ED7D31', '#A5A5A5', '#FFC000', '#5B9BD5', '#70AD47', '#C00000', '#00B0F0',
    '#FF69B4', '#008080', '#B8860B', '#4682B4', '#8B0000', '#228B22', '#800080', '#FF8C00',
    '#20B2AA', '#B22222', '#DAA520', '#2E8B57', '#6A5ACD', '#D2691E', '#DC143C', '#008B8B'
]

for modalidade_plot in modalidades_plot:
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
    ax.set_facecolor('white')
    subdf = df[df['modalidade'] == modalidade_plot]
    redes = subdf['rede'].unique()
    # Gera todas as combinações possíveis para garantir cor única
    combinacoes = [(rede, col) for rede in redes for col in ['QtdeConcluintes_perc', 'QtdeTrancados_perc', 'QtdeEvadidos_perc']]
    color_cycle = itertools.cycle(palette)
    cor_linha = {comb: next(color_cycle) for comb in combinacoes}
    for rede in redes:
        sub = subdf[subdf['rede'] == rede]
        x = sub['ano'].astype(str)
        for col in ['QtdeConcluintes_perc', 'QtdeTrancados_perc', 'QtdeEvadidos_perc']:
            ax.plot(x, sub[col], marker='o', label=f"{labels[col]} - {rede}", color=cor_linha[(rede, col)], linestyle=linestyles[col], linewidth=2)
    # Linha preta em 100%
    ax.axhline(100, color='black', linestyle='-', linewidth=2, label='100% Ingressantes')
    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel('Percentual sobre Ingressantes (%)', fontsize=12)
    ax.set_title(f'Relação (%) de Concluintes, Trancados e Evadidos sobre Ingressantes em Licenciaturas - {modalidade_plot}', color='#000000', fontsize=14)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.18), ncol=4, fontsize='small', title='Indicador - Rede', frameon=False)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    # Salvando o gráfico
    arq_output = f'static/graficos/{arq_nome}_{modalidade_plot.lower()}.png'
    plt.savefig(arq_output, bbox_inches='tight')
    plt.show()
    plt.close() 