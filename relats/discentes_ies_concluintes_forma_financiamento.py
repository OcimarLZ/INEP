import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_conc_financ) AS total_financ,
    SUM(cc.qt_conc_financ_reemb) AS total_financ_reemb,
    SUM(cc.qt_conc_fies) AS total_fies,
    SUM(cc.qt_conc_rpfies) AS total_rpfies,
    SUM(cc.qt_conc_financ_reemb_outros) AS total_financ_reemb_outros,
    SUM(cc.qt_conc_financ_nreemb) AS total_financ_nreemb,
    SUM(cc.qt_conc_prounii) AS total_prounii,
    SUM(cc.qt_conc_prounip) AS total_prounip,
    SUM(cc.qt_conc_nrpfies) AS total_nrpfies,
    SUM(cc.qt_conc_financ_nreemb_outros) AS total_financ_nreemb_outros
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

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype(int)

# Pivotando o DataFrame para que os anos estejam nas colunas e as formas de financiamento nas linhas
df_pivot = df.melt(id_vars=['ano'], var_name='Financiamento', value_name='Quantidade')
df_pivot = df_pivot.pivot(index='Financiamento', columns='ano', values='Quantidade').fillna(0).astype(int)

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['300px'] + ['100px'] * len(df_pivot.columns)
column_names = ['Tipo de Financiamento'] + [str(year) for year in df_pivot.columns]
column_alignments = ['left'] + ['right'] * len(df_pivot.columns)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'concluintes_financiamento_qtde_pivot'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Concluintes por Tipo de Financiamento em Chapecó
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

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(10, 6), facecolor='#CCFFCC')  # Fundo cinza claro para a figura, largura ajustada
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
sns.lineplot(data=df, x='ano', y='total_financ', marker='o', label='Total Financiamento', color='#006400')
sns.lineplot(data=df, x='ano', y='total_financ_reemb', marker='o', label='Financiamento Reembolsável', color='#FF6347')
sns.lineplot(data=df, x='ano', y='total_fies', marker='o', label='FIES', color='#1E90FF')
sns.lineplot(data=df, x='ano', y='total_rpfies', marker='o', label='RP FIES', color='#FFA500')
sns.lineplot(data=df, x='ano', y='total_financ_reemb_outros', marker='o', label='Outros Reembolsáveis', color='#9400D3')
sns.lineplot(data=df, x='ano', y='total_financ_nreemb', marker='o', label='Financiamento Não Reembolsável', color='#8A2BE2')
sns.lineplot(data=df, x='ano', y='total_prounii', marker='o', label='Prouni Integral', color='#FF1493')
sns.lineplot(data=df, x='ano', y='total_prounip', marker='o', label='Prouni Parcial', color='#8B4513')
sns.lineplot(data=df, x='ano', y='total_nrpfies', marker='o', label='Não Reembolsável RP FIES', color='#2E8B57')
sns.lineplot(data=df, x='ano', y='total_financ_nreemb_outros', marker='o', label='Outros Não Reembolsáveis', color='#4682B4')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['total_financ'].iloc[i]}", (df['ano'].iloc[i], df['total_financ'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#006400')
    plt.annotate(f"{df['total_financ_reemb'].iloc[i]}", (df['ano'].iloc[i], df['total_financ_reemb'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')
    plt.annotate(f"{df['total_fies'].iloc[i]}", (df['ano'].iloc[i], df['total_fies'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['total_rpfies'].iloc[i]}", (df['ano'].iloc[i], df['total_rpfies'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFA500')
    plt.annotate(f"{df['total_financ_reemb_outros'].iloc[i]}", (df['ano'].iloc[i], df['total_financ_reemb_outros'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#9400D3')
    plt.annotate(f"{df['total_financ_nreemb'].iloc[i]}", (df['ano'].iloc[i], df['total_financ_nreemb'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    plt.annotate(f"{df['total_prounii'].iloc[i]}", (df['ano'].iloc[i], df['total_prounii'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF1493')
    plt.annotate(f"{df['total_prounip'].iloc[i]}", (df['ano'].iloc[i], df['total_prounip'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8B4513')
    plt.annotate(f"{df['total_nrpfies'].iloc[i]}", (df['ano'].iloc[i], df['total_nrpfies'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#2E8B57')
    plt.annotate(f"{df['total_financ_nreemb_outros'].iloc[i]}", (df['ano'].iloc[i], df['total_financ_nreemb_outros'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#4682B4')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Concluintes')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Concluintes por Tipo de Financiamento em Chapecó', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  # Ajustando a posição da legenda
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
