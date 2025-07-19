import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_vg_total ELSE 0 END) AS vagas_presencial,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.qt_vg_total ELSE 0 END) AS vagas_distancia,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_mat ELSE 0 END) AS matriculas_presencial,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.qt_mat ELSE 0 END) AS matriculas_distancia,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_ing ELSE 0 END) AS ingressos_presencial,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.qt_ing ELSE 0 END) AS ingressos_distancia,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.qt_conc ELSE 0 END) AS concluintes_presencial,
    SUM(CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.qt_conc ELSE 0 END) AS concluintes_distancia
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

# Remover colunas onde todos os valores são zero, exceto para a coluna 'ano'
df = df.loc[:, (df != 0).any(axis=0)]

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano', 'Vagas Presencial', 'Vagas a Distância', 'Matrículas Presencial', 'Matrículas a Distância',
                'Ingressos Presencial', 'Ingressos a Distância', 'Concluintes Presencial', 'Concluintes a Distância']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'cursos_concluintes_modalidade'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução das vagas, ingressos, matrículas e concluintes em Chapecó por Modalidade de Ensino
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
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
sns.lineplot(data=df, x='ano', y='vagas_presencial', marker='o', color='#FF6347', label='Vagas Presencial')  # Tomate para linha vagas presencial
sns.lineplot(data=df, x='ano', y='vagas_distancia', marker='o', color='#FF4500', label='Vagas a Distância')  # Vermelho para linha vagas a distância
sns.lineplot(data=df, x='ano', y='matriculas_presencial', marker='o', color='#1E90FF', label='Matrículas Presencial')  # Azul dodger para linha matrículas presencial
sns.lineplot(data=df, x='ano', y='matriculas_distancia', marker='o', color='#00008B', label='Matrículas a Distância')  # Azul escuro para linha matrículas a distância
sns.lineplot(data=df, x='ano', y='ingressos_presencial', marker='o', color='#32CD32', label='Ingressos Presencial')  # Verde lima para linha ingressos presencial
sns.lineplot(data=df, x='ano', y='ingressos_distancia', marker='o', color='#006400', label='Ingressos a Distância')  # Verde escuro para linha ingressos a distância
sns.lineplot(data=df, x='ano', y='concluintes_presencial', marker='o', color='#800080', label='Concluintes Presencial')  # Roxo para linha concluintes presencial
sns.lineplot(data=df, x='ano', y='concluintes_distancia', marker='o', color='#FF00FF', label='Concluintes a Distância')  # Magenta para linha concluintes a distância

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['vagas_presencial'].iloc[i]}", (df['ano'].iloc[i], df['vagas_presencial'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    plt.annotate(f"{df['vagas_distancia'].iloc[i]}", (df['ano'].iloc[i], df['vagas_distancia'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF4500')
    plt.annotate(f"{df['matriculas_presencial'].iloc[i]}", (df['ano'].iloc[i], df['matriculas_presencial'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['matriculas_distancia'].iloc[i]}", (df['ano'].iloc[i], df['matriculas_distancia'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#00008B')
    plt.annotate(f"{df['ingressos_presencial'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_presencial'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#32CD32')
    plt.annotate(f"{df['ingressos_distancia'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_distancia'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#006400')
    plt.annotate(f"{df['concluintes_presencial'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_presencial'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#800080')
    plt.annotate(f"{df['concluintes_distancia'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_distancia'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF00FF')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Ensino Superior - Nível Graduação: Evolução das vagas, ingressos, matrículas e concluintes em Chapecó por Modalidade', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
