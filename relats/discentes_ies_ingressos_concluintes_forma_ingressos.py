import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_vg_nova) AS vg_nova,
    SUM(cc.qt_ing_vestibular) AS vestibular,
    SUM(cc.qt_ing_enem) AS enem,
    SUM(cc.qt_ing_avaliacao_seriada) AS avaliacao_seriada,
    SUM(cc.qt_ing_selecao_simplifica) AS selecao_simplificada,
    SUM(cc.qt_ing_egr) AS egressos,
    SUM(cc.qt_ing_outro_tipo_selecao) AS outro_tipo_selecao,
    SUM(cc.qt_ing_proc_seletivo) AS proc_seletivo,
    SUM(cc.qt_ing_vg_remanesc) AS vg_remanescente,
    SUM(cc.qt_ing_vg_prog_especial) AS vg_prog_especial,
    SUM(cc.qt_ing_outra_forma) AS outra_forma
FROM 
    curso_censo cc
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Pivotando o DataFrame para ter os anos como colunas e as formas de ingresso como linhas
df_pivot = df.set_index('ano').T

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['150px'] + ['100px'] * len(df_pivot.columns)
column_names = ['Forma de Ingresso'] + [str(year) for year in df_pivot.columns]
column_alignments = ['left'] + ['right'] * len(df_pivot.columns)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'ingressantes_por_forma_ingresso'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Ingressantes por Forma de Ingresso em Chapecó
        </th>
    </tr>
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
print('Tabela HTML criada com sucesso.')

# Criando o gráfico de linhas para cada forma de ingresso
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas para cada forma de ingresso
for forma in df_pivot.index:
    sns.lineplot(data=df_pivot.T, x=df_pivot.columns, y=forma, marker='o', label=forma)

plt.xlabel('Ano')
plt.ylabel('Quantidade de Ingressantes')
plt.title('Evolução dos Ingressantes por Forma de Ingresso em Chapecó', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  # Legenda à direita do gráfico
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/ingressantes_por_forma_ingresso.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
