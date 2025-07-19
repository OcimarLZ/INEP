import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Função para formatar os números em milhares (K)
def milhares(x, pos):
    return '%1.0fK' % (x * 1e-3)

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    tr.nome AS tipo_rede,
    SUM(cc.qt_ing) AS ingressantes,
    SUM(cc.qt_conc) AS concluintes,
    SUM(cc.qt_mat) AS matriculas
FROM 
    curso_censo cc
JOIN 
    tp_rede tr ON tr.codigo = cc.tp_rede
GROUP BY 
    cc.ano_censo, tr.nome
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Criando colunas para a legenda de ingressantes, concluintes e matrículas com o tipo de rede
df['ingressantes_legenda'] = df['tipo_rede'] + ' ingressantes'
df['concluintes_legenda'] = df['tipo_rede'] + ' concluintes'
df['matriculas_legenda'] = df['tipo_rede'] + ' matrículas'

# Definindo uma nova paleta de cores personalizada
novas_cores = ['#FF5733', '#33C1FF', '#FF33A6', '#FFAA33', '#33FF57', '#6A33FF', '#FFC733', '#3399FF']

# Criando um gráfico com as linhas para ingressantes, concluintes e matrículas por tipo de rede
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Ajustando os rótulos para milhares (K)
ax.yaxis.set_major_formatter(FuncFormatter(milhares))

# Plotando as linhas com a espessura ajustada
sns.lineplot(data=df, x='ano', y='ingressantes', hue='ingressantes_legenda', marker='o', palette=novas_cores[:2], linestyle='-', linewidth=2.5)
sns.lineplot(data=df, x='ano', y='concluintes', hue='concluintes_legenda', marker='o', palette=novas_cores[2:4], linestyle='--', linewidth=2.5)
sns.lineplot(data=df, x='ano', y='matriculas', hue='matriculas_legenda', marker='o', palette=novas_cores[4:6], linestyle='-.', linewidth=2.5)

# Adicionando anotações para cada ponto de ingressantes, concluintes e matrículas
for i in range(df.shape[0]):
    if i == 0 or abs(df['ingressantes'].iloc[i] - df['ingressantes'].iloc[i-1]) > 100:
        plt.annotate(f"{df['ingressantes'].iloc[i]//1000}K", (df['ano'].iloc[i], df['ingressantes'].iloc[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', color='black')
    if i == 0 or abs(df['concluintes'].iloc[i] - df['concluintes'].iloc[i-1]) > 100:
        plt.annotate(f"{df['concluintes'].iloc[i]//1000}K", (df['ano'].iloc[i], df['concluintes'].iloc[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', color='black')
    if i == 0 or abs(df['matriculas'].iloc[i] - df['matriculas'].iloc[i-1]) > 100:
        plt.annotate(f"{df['matriculas'].iloc[i]//1000}K", (df['ano'].iloc[i], df['matriculas'].iloc[i]),
                     textcoords="offset points", xytext=(0, 10), ha='center', color='black')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Evolução dos Ingressantes, Concluintes e Matrículas por Tipo de Rede', color='#000000')

# Ajustando a legenda na parte inferior em uma única linha
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize='small')  # Legenda na parte inferior em uma linha
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/evolucao_ingressantes_concluintes_matriculas_por_rede.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
