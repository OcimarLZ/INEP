import pandas as pd
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_0_17 + cc.qt_ing_18_24) AS ingresso_jovens,
    SUM(cc.qt_ing_25_29 + cc.qt_ing_30_34 + cc.qt_ing_35_39) AS ingresso_adultos,
    SUM(cc.qt_ing_40_49 + cc.qt_ing_50_59) AS ingresso_segunda_idade,
    SUM(cc.qt_ing_60_mais) AS ingresso_terceira_idade,
    SUM(cc.qt_conc_0_17 + cc.qt_conc_18_24) AS concluintes_jovens,
    SUM(cc.qt_conc_25_29 + cc.qt_conc_30_34 + cc.qt_conc_35_39) AS concluintes_adultos,
    SUM(cc.qt_conc_40_49 + cc.qt_conc_50_59) AS concluintes_segunda_idade,
    SUM(cc.qt_conc_60_mais) AS concluintes_terceira_idade
FROM 
    curso_censo cc  
JOIN 
    municipio m ON m.codigo = cc.municipio
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Remover colunas onde todos os valores são zero, exceto para a coluna 'ano'
df = df.loc[:, (df != 0).any(axis=0)]

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano', 'Ingresso Jovens', 'Ingresso Adultos', 'Ingresso Segunda Idade', 'Ingresso Terceira Idade',
                'Concluintes Jovens', 'Concluintes Adultos', 'Concluintes Segunda Idade', 'Concluintes Terceira Idade']
column_alignments = ['left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'evolucao_ingressos_concluintes_faixa_etaria'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes em Chapecó por Faixa Etária
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Ajuste para garantir que o cabeçalho da tabela tenha a cor correta
html_text = html_text.replace('<thead>', '<thead style="background-color: #4CAF50;">')

# Salvando a tabela HTML
arq_output = 'static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico de barras empilhadas utilizando Matplotlib
fig, ax = plt.subplots(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo verde muito claro para a figura
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Configurando os dados para o gráfico de barras empilhadas
df['ano'] = df['ano'].astype(str)  # Convertendo anos para string para evitar problemas na plotagem
ingressos_cols = ['ingresso_jovens', 'ingresso_adultos', 'ingresso_segunda_idade', 'ingresso_terceira_idade']
concluintes_cols = ['concluintes_jovens', 'concluintes_adultos', 'concluintes_segunda_idade', 'concluintes_terceira_idade']

# Definindo cores para as faixas etárias
colors_ingressos = ['#ADD8E6', '#87CEEB', '#4682B4', '#1E90FF']  # Tons de azul
colors_concluintes = ['#FFD700', '#FFA500', '#FF8C00', '#FF4500']  # Tons do amarelo ao vermelho

# Plotando as barras empilhadas para ingressos e concluintes
bar_width = 0.35
r1 = range(len(df))
r2 = [x + bar_width for x in r1]

# Plotando barras empilhadas para ingressos
bottom_ingressos = [0] * len(df)
for idx, col in enumerate(ingressos_cols):
    ax.bar(r1, df[col], bottom=bottom_ingressos, width=bar_width, label=col.replace('_', ' ').capitalize(), color=colors_ingressos[idx])
    for i in range(len(df)):
        if df[col].iloc[i] > 20:  # Mover os valores menores para fora da barra
            ax.text(r1[i], bottom_ingressos[i] + df[col].iloc[i] / 2, str(df[col].iloc[i]), ha='center', va='center', fontsize=9)
        else:
            ax.text(r1[i], bottom_ingressos[i] + df[col].iloc[i] + 10, str(df[col].iloc[i]), ha='center', va='bottom', fontsize=9)
    bottom_ingressos = [i + j for i, j in zip(bottom_ingressos, df[col])]

# Plotando barras empilhadas para concluintes
bottom_concluintes = [0] * len(df)
for idx, col in enumerate(concluintes_cols):
    ax.bar(r2, df[col], bottom=bottom_concluintes, width=bar_width, label=col.replace('_', ' ').capitalize(), color=colors_concluintes[idx])
    for i in range(len(df)):
        if df[col].iloc[i] > 20:  # Mover os valores menores para fora da barra
            ax.text(r2[i], bottom_concluintes[i] + df[col].iloc[i] / 2, str(df[col].iloc[i]), ha='center', va='center', fontsize=9)
        else:
            ax.text(r2[i], bottom_concluintes[i] + df[col].iloc[i] + 10, str(df[col].iloc[i]), ha='center', va='bottom', fontsize=9)
    bottom_concluintes = [i + j for i, j in zip(bottom_concluintes, df[col])]

# Definindo títulos e rótulos
ax.set_xlabel('Ano')
ax.set_ylabel('Quantidade')
ax.set_title('Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes em Chapecó por Faixa Etária', color='#000000')  # Preto para o título
ax.set_xticks([r + bar_width / 2 for r in range(len(df))])
ax.set_xticklabels(df['ano'])
ax.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small', title='Faixa Etária')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = 'static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
