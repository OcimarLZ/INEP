import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL para as IES específicas
sql = """
SELECT 
    i.sigla as sigla,
    cc.ano_censo AS ano,
    SUM(cc.qt_vg_total) AS vagas_ofertadas,
    SUM(cc.qt_ing) AS ingressantes
FROM 
    curso_censo cc
JOIN
    ies i ON cc.ies = i.codigo
WHERE 
    cc.municipio = 4204202 AND cc.tp_modalidade_ensino = 1 and i.sigla IN ('UFFS', 'UNOESC', 'UNOCHAPECÓ','FAEM','UDESC')
GROUP BY 
    sigla, ano
"""
df = carregar_dataframe(sql)

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype({'vagas_ofertadas': 'int', 'ingressantes': 'int'})

# Pivotando o DataFrame para o formato desejado
df_pivot = df.pivot(index='sigla', columns='ano', values=['vagas_ofertadas', 'ingressantes'])
df_pivot.columns = [f'{col[0]}_{col[1]}' for col in df_pivot.columns]
df_pivot = df_pivot.fillna(0).astype(int)

# Redefinindo a lista de tamanhos para o formato HTML
years = sorted(df['ano'].unique())
column_html = ['100px'] + ['100px'] * (len(years) * 2)
column_alignments = ['left'] + ['right'] * (len(years) * 2)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'vagas_ingressantes_por_ano_presencial_5ies'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução das Vagas Ofertadas e Ingressantes IES top 5 em Chapecó (Modalidade Presencial)
        </th>
    </tr>
    <tr style="background-color: #4CAF50;">
        <th rowspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">Sigla</th>
        {''.join([f'<th colspan="2" style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">{year}</th>' for year in years])}
    </tr>
    <tr style="background-color: #4CAF50;">
        {''.join(['<th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">Vagas Ofertadas</th><th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">Ingressantes</th>' for _ in years])}
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

# Criando gráficos para as IES selecionadas
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

for sigla in df['sigla'].unique():
    df_ies = df[df['sigla'] == sigla]
    sns.lineplot(data=df_ies, x='ano', y='vagas_ofertadas', marker='o', label=f'{sigla} Vagas Ofertadas')
    sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', label=f'{sigla} Ingressantes')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução das Vagas Ofertadas e Ingressantes IES tOP 5 em Chapecó (Modalidade Presencial)', color='#000000')
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/vagas_ingressantes_5ies.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
