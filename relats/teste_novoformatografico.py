import pandas as pd
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe

# Monta o SQL para obter os dados
sql = """
SELECT 
    cc.ies,
    i.sigla,
    i.nome,
    CASE WHEN cc.tp_modalidade_ensino = 2 THEN c.nome || '-ead' ELSE c.nome END AS curso,
    cc.ano_censo AS ano,
    SUM(cc.qt_mat) AS matriculas
FROM curso_censo cc
JOIN curso c ON c.codigo = cc.curso 
JOIN ies i ON i.codigo = cc.ies
WHERE cc.municipio = 4204202 AND cc.ano_censo >= 2014
GROUP BY 
    cc.ies, i.sigla, i.nome, c.nome, cc.ano_censo, cc.tp_modalidade_ensino
ORDER BY 
    cc.ies, i.sigla, i.nome, c.nome, cc.ano_censo, cc.tp_modalidade_ensino;
"""

# Carrega o DataFrame a partir do SQL
df = carregar_dataframe(sql)

# Removendo a primeira coluna ('ies'), pois ela só serviu para classificar
df = df.drop(columns=['ies'])

# Tratando a coluna 'sigla' para substituir valores nulos
df['sigla'] = df.apply(lambda row: ' '.join(row['nome'].split()[1:3]) if pd.isnull(row['sigla']) else row['sigla'], axis=1)

# Removendo a coluna 'nome'
df = df.drop(columns=['nome'])

# Concatenando a sigla da instituição com o nome do curso
df['curso_completo'] = df['sigla'] + " - " + df['curso']

# Selecionando as colunas necessárias para o relatório
df_final = df[['curso_completo', 'ano', 'matriculas']]

# Pivotando a tabela para ter os anos como colunas e os cursos como linhas
df_pivot = df_final.pivot(index='curso_completo', columns='ano', values='matriculas')

# Substituindo valores nulos por 0 e convertendo para inteiros
df_pivot = df_pivot.fillna(0).astype(int)

# Salvando a tabela em um arquivo Excel
arq_output = '../static/tabelas/matriculas_por_curso_por_ano.xlsx'
df_pivot.to_excel(arq_output)

# Criando um gráfico para os dados
plt.figure(figsize=(12, 8), facecolor='#F0F0F0')  # Fundo cinza claro
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
for curso in df_pivot.index:
    plt.plot(df_pivot.columns, df_pivot.loc[curso], linestyle='--', linewidth=2, label=curso)  # Linhas tracejadas com espessura aumentada

# Ajustando a legenda
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize='medium')  # Legenda com 2 colunas

# Ajustando os rótulos e título
plt.xlabel('Ano', fontweight='bold')
plt.ylabel('Matrículas', fontweight='bold')
plt.title('Evolução de Matrículas por Curso e Ano', color='#000000', fontweight='bold')

# Ajustando o estilo dos rótulos do eixo X e Y
ax.xaxis.label.set_size(12)
ax.yaxis.label.set_size(12)
ax.xaxis.label.set_weight('bold')
ax.yaxis.label.set_weight('bold')

# Salvando o gráfico
arq_output_grafico = '../static/graficos/matriculas_por_curso_por_ano.png'
plt.tight_layout()
plt.savefig(arq_output_grafico, bbox_inches='tight')
plt.show()

print('Planilha Excel e gráfico criados com sucesso.')
