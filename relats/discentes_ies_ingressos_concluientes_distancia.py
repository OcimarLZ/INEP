import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    i.nome AS ies,
    i.sigla as sigla,
    cc.ano_censo AS ano,
    SUM(cc.qt_ing) AS ingressantes,
    SUM(cc.qt_conc) AS concluintes
FROM 
    curso_censo cc
JOIN
    ies i ON cc.ies = i.codigo
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013 and cc.tp_modalidade_ensino = 2
GROUP BY 
    ies, sigla, ano_censo
ORDER BY 
    ies, sigla, cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Substituindo valores nulos em sigla por "-"
df['sigla'] = df['sigla'].fillna('-')

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype({'ingressantes': 'int', 'concluintes': 'int'})

# Filtrando apenas IES com sigla
df_with_sigla = df[df['sigla'] != '-']

# Pivotando o DataFrame para o formato desejado
df_pivot = df.pivot(index=['ies', 'sigla'], columns='ano', values=['ingressantes', 'concluintes'])
df_pivot.columns = [f'{col[0]}_{col[1]}' for col in df_pivot.columns]
df_pivot = df_pivot.fillna(0).astype(int)

# Redefinindo a lista de tamanhos para o formato HTML
years = sorted(df['ano'].unique())
column_html = ['200px', '50px'] + ['100px'] * (len(years) * 2)
column_alignments = ['left', 'left'] + ['right'] * (len(years) * 2)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'ies_ingressos_concluintes_por_ano_distancia'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 2}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Totais de Ingressantes e Concluintes por IES em Chapecó Modalidade a Distância
        </th>
    </tr>
    <tr style="background-color: #4CAF50;">
        <th rowspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">IES</th>
        <th rowspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">Sigla</th>
        {''.join([f'<th colspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">{year}</th>' for year in years])}
    </tr>
    <tr style="background-color: #4CAF50;">
        {''.join(['<th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">Ingressantes</th><th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">Concluintes</th>' for _ in years])}
    </tr>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot.reset_index(), column_html, [], column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Ajuste para garantir que o cabeçalho da tabela tenha a cor correta
html_text = html_text.replace('<thead>', '').replace('</thead>', '')

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando gráficos separados para cada IES utilizando Seaborn com fundo cinza claro
ies_list = df['ies'].unique()

for ies in ies_list:
    df_ies = df[df['ies'] == ies]
    ies_label = df_ies['sigla'].iloc[0] if df_ies['sigla'].iloc[0] != '-' else ies

    plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
    ax = plt.gca()
    ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

    # Plotando as linhas para cada IES
    sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', color='#FF8C00', label='Ingressantes')  # Laranja escuro
    sns.lineplot(data=df_ies, x='ano', y='concluintes', marker='o', color='#006400', label='Concluintes')  # Verde escuro

    # Adicionando anotações para cada ponto
    for i in range(df_ies.shape[0]):
        plt.annotate(f"{df_ies['ingressantes'].iloc[i]}",
                     (df_ies['ano'].iloc[i], df_ies['ingressantes'].iloc[i]), textcoords="offset points",
                     xytext=(0, 10), ha='center', color='#FF8C00')
        plt.annotate(f"{df_ies['concluintes'].iloc[i]}",
                     (df_ies['ano'].iloc[i], df_ies['concluintes'].iloc[i]), textcoords="offset points",
                     xytext=(0, 10), ha='center', color='#006400')

    plt.xlabel('Ano')
    plt.ylabel('Quantidade de discentes')
    plt.title(f'Evolução dos Totais de Ingressantes e Concluintes na IES Modalidade a Distância: {ies_label}',
              color='#000000')  # Preto para o título
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')  # Mover legenda para o rodapé
    plt.grid(True)

    # Salvando o gráfico para cada IES
    arq_output = f'../static/graficos/{arq_nome}_{ies_label}.png'
    plt.tight_layout()
    plt.savefig(arq_output, bbox_inches='tight')
    plt.show()
    plt.close()

# Criando gráfico com todas as IES para ingressantes
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

for ies in ies_list:
    df_ies = df[df['ies'] == ies]
    ies_label = df_ies['sigla'].iloc[0] if df_ies['sigla'].iloc[0] != '-' else ies
    sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', label=f'{ies_label} Ingressantes')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Ingressantes')
plt.title('Evolução dos Ingressantes por IES em Chapecó Modalidade a Distância', color='#000000')  # Preto para o título
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico para todos os ingressantes
arq_output = '../static/graficos/ingressantes_todas_ies.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()

# Criando gráfico com todas as IES para concluintes
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

for ies in ies_list:
    df_ies = df[df['ies'] == ies]
    ies_label = df_ies['sigla'].iloc[0] if df_ies['sigla'].iloc[0] != '-' else ies
    sns.lineplot(data=df_ies, x='ano', y='concluintes', marker='o', label=f'{ies_label} Concluintes')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Concluintes')
plt.title('Evolução dos Concluintes por IES em Chapecó Modalidade a Distância', color='#000000')  # Preto para o título
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico para todos os concluintes
arq_output = '../static/graficos/concluintes_todas_ies.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()

# Gerando gráficos com as 10 maiores IES em termos de ingressantes, e uma linha com a soma das demais
total_ingressantes = df_with_sigla.groupby('ies')['ingressantes'].sum().sort_values(ascending=False)
top_10_ingressantes = total_ingressantes.head(10)
others_ingressantes = total_ingressantes[10:].sum()

# Filtrando dados das 10 maiores IES e calculando "Outras"
df_top_ingressantes = df_with_sigla[df_with_sigla['ies'].isin(top_10_ingressantes.index)]
df_others_ingressantes = df_with_sigla[~df_with_sigla['ies'].isin(top_10_ingressantes.index)].copy()
df_others_ingressantes['ies'] = 'Outras'
df_others_ingressantes['sigla'] = 'Outras'
df_others_ingressantes = df_others_ingressantes.groupby(['ies', 'sigla', 'ano']).sum().reset_index()

df_top_ingressantes = pd.concat([df_top_ingressantes, df_others_ingressantes])

plt.figure(figsize=(12, 8), facecolor='#CCFFCC')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

for ies in df_top_ingressantes['ies'].unique():
    df_ies = df_top_ingressantes[df_top_ingressantes['ies'] == ies]
    if ies == 'Outras':
        sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', label=f'{ies}', color='black')
    elif df_ies['sigla'].iloc[0] == 'UFFS':
        sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', label=f'{df_ies["sigla"].iloc[0]} Ingressantes', color='darkgreen')
    else:
        sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', label=f'{df_ies["sigla"].iloc[0]} Ingressantes')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Ingressantes')
plt.title('Evolução dos Ingressantes das 10 Maiores IES e Outras em Chapecó Modalidade a Distância', color='#000000')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico para as 10 maiores IES em termos de ingressantes
arq_output = '../static/graficos/ingressantes_top_10_outros.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()

# Gerando gráficos com as 10 maiores IES em termos de concluintes, e uma linha com a soma das demais
total_concluintes = df_with_sigla.groupby('ies')['concluintes'].sum().sort_values(ascending=False)
top_10_concluintes = total_concluintes.head(10)
others_concluintes = total_concluintes[10:].sum()

# Filtrando dados das 10 maiores IES e calculando "Outras"
df_top_concluintes = df_with_sigla[df_with_sigla['ies'].isin(top_10_concluintes.index)]
df_others_concluintes = df_with_sigla[~df_with_sigla['ies'].isin(top_10_concluintes.index)].copy()
df_others_concluintes['ies'] = 'Outras'
df_others_concluintes['sigla'] = 'Outras'
df_others_concluintes = df_others_concluintes.groupby(['ies', 'sigla', 'ano']).sum().reset_index()

df_top_concluintes = pd.concat([df_top_concluintes, df_others_concluintes])

plt.figure(figsize=(12, 8), facecolor='#CCFFCC')
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

for ies in df_top_concluintes['ies'].unique():
    df_ies = df_top_concluintes[df_top_concluintes['ies'] == ies]
    if ies == 'Outras':
        sns.lineplot(data=df_ies, x='ano', y='concluintes', marker='o', label=f'{ies}', color='black')
    elif df_ies['sigla'].iloc[0] == 'UFFS':
        sns.lineplot(data=df_ies, x='ano', y='concluintes', marker='o', label=f'{df_ies["sigla"].iloc[0]} Concluintes', color='darkgreen')
    else:
        sns.lineplot(data=df_ies, x='ano', y='concluintes', marker='o', label=f'{df_ies["sigla"].iloc[0]} Concluintes')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Concluintes')
plt.title('Evolução dos Concluintes das 10 Maiores IES e Outras em Chapecó Modalidade a Distância', color='#000000')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico para as 10 maiores IES em termos de concluintes
arq_output = '../static/graficos/concluintes_top_10_outros.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
