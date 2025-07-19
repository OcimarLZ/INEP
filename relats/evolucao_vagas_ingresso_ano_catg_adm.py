import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    tca.nome AS categoria_administrativa,
    cc.ano_censo AS ano,
    SUM(cc.qt_vg_total) AS vagas_ofertadas,
    SUM(cc.qt_ing) AS ingressantes
FROM 
    curso_censo cc
JOIN 
    tp_categoria_administrativa tca ON cc.categoria = tca.codigo
WHERE 
    cc.municipio = 4204202 AND cc.tp_modalidade_ensino = 1 AND cc.ano_censo > 2013
GROUP BY 
    tca.nome, cc.ano_censo
ORDER BY 
    tca.nome, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype({'vagas_ofertadas': 'int', 'ingressantes': 'int'})

# Pivotando o DataFrame para que os anos sejam colunas e as categorias administrativas sejam linhas
df_pivot = df.pivot(index='categoria_administrativa', columns='ano', values=['vagas_ofertadas', 'ingressantes'])

# Ajustando os nomes das colunas
df_pivot.columns = [f'{col[0]}_{col[1]}' for col in df_pivot.columns]

# Substituindo NaN por 0 e convertendo para inteiros
df_pivot = df_pivot.fillna(0).astype(int)

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['300px'] + ['100px'] * len(df_pivot.columns)
column_names = ['Categoria Administrativa'] + [f'{col.replace("_", " ")}' for col in df_pivot.columns]
column_alignments = ['left'] + ['right'] * len(df_pivot.columns)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'vagas_ingressantes_presenciais_categoria_administrativa_pivotado'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução da Oferta de Vagas e Ingressantes por Categoria Administrativa em Chapecó (Cursos Presenciais)
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

# Criando o gráfico de linhas para a evolução das vagas ofertadas e ingressantes por categoria administrativa
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Ajustando o tamanho do gráfico
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
for categoria in df['categoria_administrativa'].unique():
    df_categoria = df[df['categoria_administrativa'] == categoria]
    sns.lineplot(data=df_categoria, x='ano', y='vagas_ofertadas', marker='o', label=f'{categoria} - Vagas Ofertadas')
    sns.lineplot(data=df_categoria, x='ano', y='ingressantes', marker='o', label=f'{categoria} - Ingressantes')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['vagas_ofertadas'].iloc[i]}", (df['ano'].iloc[i], df['vagas_ofertadas'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center')
    plt.annotate(f"{df['ingressantes'].iloc[i]}", (df['ano'].iloc[i], df['ingressantes'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução da Oferta de Vagas e Ingressantes por Categoria Administrativa em Chapecó (Cursos Presenciais)', color='#000000')

# Movendo a legenda para a parte inferior, distribuída em três colunas
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')
plt.grid(True)

# Ajustando a área do gráfico para não cortar a legenda
plt.tight_layout()

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
