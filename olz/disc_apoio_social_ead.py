import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe

# Carrega os dados do SQL
sql = """
SELECT 
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
WHERE 
    tp_modalidade_ensino = 2
GROUP BY 
    ano_censo;
"""
df = carregar_dataframe(sql)

# Configuração do gráfico
plt.figure(figsize=(14, 8))
sns.set(style="whitegrid")

# Definindo cores para cada linha
colors = {
    'Ingressantes com Apoio Social': '#ff7f0e',
    'Matriculados com Apoio Social': '#d62728',
    'Concluintes com Apoio Social': '#8c564b',
    'Algum Tipo de Apoio': '#7f7f7f'
}

# Criação das linhas para cada categoria
sns.lineplot(data=df, x='ano_censo', y='perc_ing_apoio', label='Ingressantes com Apoio Social', marker='o', color=colors['Ingressantes com Apoio Social'], linewidth=2.5)
sns.lineplot(data=df, x='ano_censo', y='perc_mat_apoio', label='Matriculados com Apoio Social', marker='o', color=colors['Matriculados com Apoio Social'], linewidth=2.5, linestyle='--')
sns.lineplot(data=df, x='ano_censo', y='perc_conc_apoio', label='Concluintes com Apoio Social', marker='o', color=colors['Concluintes com Apoio Social'], linewidth=2.5, linestyle='-.')
sns.lineplot(data=df, x='ano_censo', y='perc_algum_apoio', label='Algum Tipo de Apoio', marker='o', color=colors['Algum Tipo de Apoio'], linewidth=2.5, linestyle=':')

# Adicionando rótulos para cada ponto
for i in range(df.shape[0]):
    plt.text(df['ano_censo'].iloc[i], df['perc_ing_apoio'].iloc[i], f"{df['perc_ing_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=colors['Ingressantes com Apoio Social'])
    plt.text(df['ano_censo'].iloc[i], df['perc_mat_apoio'].iloc[i], f"{df['perc_mat_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=colors['Matriculados com Apoio Social'])
    plt.text(df['ano_censo'].iloc[i], df['perc_conc_apoio'].iloc[i], f"{df['perc_conc_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=colors['Concluintes com Apoio Social'])
    plt.text(df['ano_censo'].iloc[i], df['perc_algum_apoio'].iloc[i], f"{df['perc_algum_apoio'].iloc[i]:.2f}%", ha="center", va="bottom", fontsize=8, color=colors['Algum Tipo de Apoio'])

# Configurando rótulos e título
plt.xlabel('Ano', fontweight='bold')
plt.ylabel('Percentual (%)', fontweight='bold')
plt.title('Evolução dos Percentuais de Apoio Social Modalidade EAD', fontweight='bold')

# Ajustando a legenda
plt.legend(title='Categoria', loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')
plt.grid(True)

# Salvando e mostrando o gráfico
arq_output = '../static/graficos/evolucao_apoio_social_ead.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
