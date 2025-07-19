import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe

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
    cc.municipio = 4204202 AND cc.ano_censo > 2013 AND cc.tp_modalidade_ensino = 1
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

# Definindo as cores para cada IES
color_map = {
    'Unochapecó': ('#0000FF', '#6495ED'),  # Azul escuro e azul claro
    'UFFS': ('#006400', '#32CD32'),        # Verde escuro e verde claro
    'IFSC': ('#8B0000', '#CD5C5C'),        # Vermelho escuro e vermelho claro
    'UNOESC': ('#8B4513', '#D2B48C'),      # Marrom escuro e marrom claro
    'FACESC': ('#FF8C00', '#FFA07A'),      # Laranja escuro e laranja claro
    'SENAI': ('#D2691E', '#F4A460'),       # Ocre escuro e ocre claro
    'UDESC': ('#4B0082', '#9370DB'),       # Roxo escuro e roxo claro
    'FAEM': ('#FFD700', '#FFFACD')         # Amarelo escuro e amarelo claro
}

# Criando um gráfico com todas as IES para ingressantes e concluintes
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

for ies in df_with_sigla['sigla'].unique():
    df_ies = df_with_sigla[df_with_sigla['sigla'] == ies]
    dark_color, light_color = color_map.get(ies, ('#000000', '#808080'))  # Preto e cinza padrão se a sigla não for encontrada
    sns.lineplot(data=df_ies, x='ano', y='ingressantes', marker='o', label=f'{ies} Ingressantes', color=dark_color)
    sns.lineplot(data=df_ies, x='ano', y='concluintes', marker='o', label=f'{ies} Concluintes', color=light_color)

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução dos Totais de Ingressantes e Concluintes por IES em Chapecó (Modalidade Presencial)', color='#000000')

# Colocando a legenda no lado direito do gráfico
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')

plt.grid(True)

# Salvando o gráfico para todos os ingressantes e concluintes
arq_output = '../static/graficos/ingressantes_concluintes_todas_ies.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
