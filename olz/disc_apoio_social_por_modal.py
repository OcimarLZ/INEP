import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe

# Carrega os dados do SQL
sql = """
SELECT 
    tp_modalidade_ensino, 
    ano_censo,
    CASE 
        WHEN SUM(qt_ing) > 0 THEN ROUND((SUM(qt_ing_apoio_social) * 100.0 / SUM(qt_ing)),2) 
        ELSE 0 
    END AS perc_ing_apoio,
    CASE 
        WHEN SUM(qt_mat) > 0 THEN ROUND((SUM(qt_mat_apoio_social) * 100.0 / SUM(qt_mat)),2)
        ELSE 0 
    END AS perc_mat_apoio,
    CASE 
        WHEN SUM(qt_conc) > 0 THEN ROUND((SUM(qt_conc_apoio_social) * 100.0 / SUM(qt_conc)),2)
        ELSE 0 
    END AS perc_conc_apoio,
    CASE 
        WHEN SUM(qt_mat) > 0 THEN ROUND((SUM(qt_apoio_social) * 100.0 / SUM(qt_mat)),2)
        ELSE 0 
    END AS perc_algum_apoio
FROM 
    curso_censo
GROUP BY 
    tp_modalidade_ensino, ano_censo;
"""
df = carregar_dataframe(sql)

# Converte a modalidade de ensino para uma coluna categórica mais legível
df['tp_modalidade_ensino'] = df['tp_modalidade_ensino'].map({1: 'Presencial', 2: 'EAD'})

# Configura o gráfico
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

# Definindo uma paleta de cores específica para cada combinação de modalidade e dado
color_map = {
    'Presencial - Ingressantes com Apoio Social': '#1f77b4',
    'EAD - Ingressantes com Apoio Social': '#ff7f0e',
    'Presencial - Matriculados com Apoio Social': '#2ca02c',
    'EAD - Matriculados com Apoio Social': '#d62728',
    'Presencial - Concluintes com Apoio Social': '#9467bd',
    'EAD - Concluintes com Apoio Social': '#8c564b',
    'Presencial - Algum Tipo de Apoio': '#e377c2',
    'EAD - Algum Tipo de Apoio': '#7f7f7f'
}

# Criando linhas para cada categoria com cores específicas
sns.lineplot(data=df, x='ano_censo', y='perc_ing_apoio', hue=df['tp_modalidade_ensino'].apply(lambda x: f'{x} - Ingressantes com Apoio Social'), marker='o', palette=color_map, linewidth=2.5)
sns.lineplot(data=df, x='ano_censo', y='perc_mat_apoio', hue=df['tp_modalidade_ensino'].apply(lambda x: f'{x} - Matriculados com Apoio Social'), marker='o', palette=color_map, linewidth=2.5, linestyle='--')
sns.lineplot(data=df, x='ano_censo', y='perc_conc_apoio', hue=df['tp_modalidade_ensino'].apply(lambda x: f'{x} - Concluintes com Apoio Social'), marker='o', palette=color_map, linewidth=2.5, linestyle='-.')
sns.lineplot(data=df, x='ano_censo', y='perc_algum_apoio', hue=df['tp_modalidade_ensino'].apply(lambda x: f'{x} - Algum Tipo de Apoio'), marker='o', palette=color_map, linewidth=2.5, linestyle=':')

# Adicionando rótulos para cada ponto
for i in range(df.shape[0]):
    plt.text(df['ano_censo'].iloc[i], df['perc_ing_apoio'].iloc[i], f"{df['perc_ing_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=color_map[f"{df['tp_modalidade_ensino'].iloc[i]} - Ingressantes com Apoio Social"])
    plt.text(df['ano_censo'].iloc[i], df['perc_mat_apoio'].iloc[i], f"{df['perc_mat_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=color_map[f"{df['tp_modalidade_ensino'].iloc[i]} - Matriculados com Apoio Social"])
    plt.text(df['ano_censo'].iloc[i], df['perc_conc_apoio'].iloc[i], f"{df['perc_conc_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=color_map[f"{df['tp_modalidade_ensino'].iloc[i]} - Concluintes com Apoio Social"])
    plt.text(df['ano_censo'].iloc[i], df['perc_algum_apoio'].iloc[i], f"{df['perc_algum_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=color_map[f"{df['tp_modalidade_ensino'].iloc[i]} - Algum Tipo de Apoio"])

# Configurando rótulos e título
plt.xlabel('Ano', fontweight='bold')
plt.ylabel('Percentual (%)', fontweight='bold')
plt.title('Evolução dos Percentuais de Apoio Social por Modalidade de Ensino e Ano', fontweight='bold')

# Ajustando a legenda
plt.legend(title='Categoria', loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize='small')
plt.grid(True)

# Salvando e mostrando o gráfico
arq_output = '../static/graficos/evolucao_apoio_social_por_modalidade.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
