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

# Combinar os dados de ingressantes e concluintes em um único DataFrame para plotagem combinada
df_combined = df_with_sigla.melt(id_vars=['ies', 'sigla', 'ano'], value_vars=['ingressantes', 'concluintes'], var_name='tipo', value_name='quantidade')

# Criando um gráfico com todas as IES combinando ingressantes e concluintes
plt.figure(figsize=(14, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

sns.lineplot(data=df_combined, x='ano', y='quantidade', hue='sigla', style='tipo', markers=True, dashes=False)

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução dos Totais de Ingressantes e Concluintes por IES em Chapecó (Modalidade Presencial)', color='#000000')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')
plt.grid(True)

# Salvando o gráfico para todos os ingressantes e concluintes
arq_output = '../static/graficos/ingressantes_concluintes_combined_todas_ies.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
