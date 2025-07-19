import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_branca) AS ingressantes_branca,
    SUM(cc.qt_ing_preta) AS ingressantes_preta,
    SUM(cc.qt_ing_parda) AS ingressantes_parda,
    SUM(cc.qt_ing_amarela) AS ingressantes_amarela,
    SUM(cc.qt_ing_indigena) AS ingressantes_indigena,
    SUM(cc.qt_ing_cornd) AS ingressantes_cornd,
    SUM(cc.qt_conc_branca) AS concluintes_branca,
    SUM(cc.qt_conc_preta) AS concluintes_preta,
    SUM(cc.qt_conc_parda) AS concluintes_parda,
    SUM(cc.qt_conc_amarela) AS concluintes_amarela,
    SUM(cc.qt_conc_indigena) AS concluintes_indigena,
    SUM(cc.qt_conc_cornd) AS concluintes_cornd
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

# Preenchendo valores nulos com 0 e convertendo para inteiros
df = df.fillna(0).astype(int)

# Pivotando o DataFrame para colocar os anos como colunas e as raças como linhas
df_pivot = df.melt(id_vars=['ano'], var_name='categoria', value_name='quantidade')
df_pivot['categoria'] = df_pivot['categoria'].str.replace('ingressantes_', 'Ingressantes ').str.replace('concluintes_', 'Concluintes ')
df_pivot = df_pivot.pivot(index='categoria', columns='ano', values='quantidade')
df_pivot = df_pivot.fillna(0).astype(int)

# Configurando a tabela HTML
column_html = ['150px'] + ['100px'] * len(df_pivot.columns)
column_names = ['Categoria'] + [str(col) for col in df_pivot.columns]
column_alignments = ['left'] + ['right'] * len(df_pivot.columns)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'ingressantes_concluintes_por_raca'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Ingressantes e Concluintes por Raça em Chapecó
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
print('Tabela HTML criada com sucesso.')

# Criando o gráfico de linhas
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

# Definindo as cores para as linhas
cores = {
    'ingressantes_branca': '#1E90FF',   # Azul claro
    'concluintes_branca': '#0000FF',    # Azul escuro
    'ingressantes_preta': '#FF8C00',    # Laranja escuro
    'concluintes_preta': '#FF4500',     # Vermelho tijolo
    'ingressantes_parda': '#32CD32',    # Verde lima
    'concluintes_parda': '#006400',     # Verde escuro
    'ingressantes_amarela': '#FFD700',  # Ouro
    'concluintes_amarela': '#FFA500',   # Laranja
    'ingressantes_indigena': '#8A2BE2', # Roxo
    'concluintes_indigena': '#4B0082',  # Índigo
    'ingressantes_cornd': '#B22222',    # Marrom escuro
    'concluintes_cornd': '#A52A2A',     # Marrom
}

# Plotando as linhas
for col in df.columns[1:]:
    sns.lineplot(data=df, x='ano', y=col, marker='o', label=col.replace('_', ' ').capitalize(), color=cores[col])

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Ingressantes e Concluintes por Raça em Chapecó (Modalidade Presencial)', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), ncol=1, fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/ingressantes_concluintes_por_raca.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
