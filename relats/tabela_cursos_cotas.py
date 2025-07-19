import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_branca) AS ingressos_branca,
    SUM(cc.qt_conc_branca) AS concluintes_branca,
    SUM(cc.qt_ing_preta) AS ingressos_preta,
    SUM(cc.qt_conc_preta) AS concluintes_preta,
    SUM(cc.qt_ing_parda) AS ingressos_parda,
    SUM(cc.qt_conc_parda) AS concluintes_parda,
    SUM(cc.qt_ing_amarela) AS ingressos_amarela,
    SUM(cc.qt_conc_amarela) AS concluintes_amarela,
    SUM(cc.qt_ing_indigena) AS ingressos_indigena,
    SUM(cc.qt_conc_indigena) AS concluintes_indigena,
    SUM(cc.qt_ing_cornd) AS ingressos_cornd,
    SUM(cc.qt_conc_cornd) AS concluintes_cornd
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
column_names = ['Ano', 'Ingressos Branca', 'Concluintes Branca', 'Ingressos Preta', 'Concluintes Preta', 'Ingressos Parda', 'Concluintes Parda',
                'Ingressos Amarela', 'Concluintes Amarela', 'Ingressos Indígena', 'Concluintes Indígena', 'Ingressos CorND', 'Concluintes CorND']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'cursos_discentes_cotas'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes de Cotas em Chapecó
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

# Criando o primeiro gráfico de linhas com todos os dados utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
sns.lineplot(data=df, x='ano', y='ingressos_branca', marker='o', color='#FFD700', label='Ingressos Branca')  # Ouro para linha ingressos branca
sns.lineplot(data=df, x='ano', y='ingressos_preta', marker='o', color='#FF8C00', label='Ingressos Preta')  # Laranja escuro para linha ingressos preta
sns.lineplot(data=df, x='ano', y='ingressos_parda', marker='o', color='#FF4500', label='Ingressos Parda')  # Vermelho tijolo para linha ingressos parda
sns.lineplot(data=df, x='ano', y='ingressos_amarela', marker='o', color='#FFA500', label='Ingressos Amarela')  # Laranja para linha ingressos amarela
sns.lineplot(data=df, x='ano', y='ingressos_indigena', marker='o', color='#DC143C', label='Ingressos Indígena')  # Carmesim para linha ingressos indígena
sns.lineplot(data=df, x='ano', y='ingressos_cornd', marker='o', color='#B22222', label='Ingressos CorND')  # Vermelho tijolo escuro para linha ingressos cornd

sns.lineplot(data=df, x='ano', y='concluintes_branca', marker='o', color='#1E90FF', label='Concluintes Branca')  # Azul dodger para linha concluintes branca
sns.lineplot(data=df, x='ano', y='concluintes_preta', marker='o', color='#0000CD', label='Concluintes Preta')  # Azul médio para linha concluintes preta
sns.lineplot(data=df, x='ano', y='concluintes_parda', marker='o', color='#8A2BE2', label='Concluintes Parda')  # Azul violeta para linha concluintes parda
sns.lineplot(data=df, x='ano', y='concluintes_amarela', marker='o', color='#9400D3', label='Concluintes Amarela')  # Azul escuro para linha concluintes amarela
sns.lineplot(data=df, x='ano', y='concluintes_indigena', marker='o', color='#4B0082', label='Concluintes Indígena')  # Índigo para linha concluintes indígena
sns.lineplot(data=df, x='ano', y='concluintes_cornd', marker='o', color='#6A5ACD', label='Concluintes CorND')  # Azul ardósia médio para linha concluintes cornd

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingressos_branca'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_branca'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFD700')
    plt.annotate(f"{df['ingressos_preta'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_preta'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF8C00')
    plt.annotate(f"{df['ingressos_parda'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_parda'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF4500')
    plt.annotate(f"{df['ingressos_amarela'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_amarela'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFA500')
    plt.annotate(f"{df['ingressos_indigena'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_indigena'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#DC143C')
    plt.annotate(f"{df['ingressos_cornd'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_cornd'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#B22222')

    plt.annotate(f"{df['concluintes_branca'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_branca'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['concluintes_preta'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_preta'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#0000CD')
    plt.annotate(f"{df['concluintes_parda'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_parda'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#8A2BE2')
    plt.annotate(f"{df['concluintes_amarela'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_amarela'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#9400D3')
    plt.annotate(f"{df['concluintes_indigena'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_indigena'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#4B0082')
    plt.annotate(f"{df['concluintes_cornd'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_cornd'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#6A5ACD')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes de Cotas em Chapecó', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico com todos os dados
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()

# Criando o segundo gráfico de linhas excluindo "Branca" e "CorND"
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas excluindo "Branca" e "CorND"
sns.lineplot(data=df, x='ano', y='ingressos_preta', marker='o', color='#FF8C00', label='Ingressos Preta')  # Laranja escuro para linha ingressos preta
sns.lineplot(data=df, x='ano', y='ingressos_parda', marker='o', color='#FF4500', label='Ingressos Parda')  # Vermelho tijolo para linha ingressos parda
sns.lineplot(data=df, x='ano', y='ingressos_amarela', marker='o', color='#FFA500', label='Ingressos Amarela')  # Laranja para linha ingressos amarela
sns.lineplot(data=df, x='ano', y='ingressos_indigena', marker='o', color='#DC143C', label='Ingressos Indígena')  # Carmesim para linha ingressos indígena

sns.lineplot(data=df, x='ano', y='concluintes_preta', marker='o', color='#0000CD', label='Concluintes Preta')  # Azul médio para linha concluintes preta
sns.lineplot(data=df, x='ano', y='concluintes_parda', marker='o', color='#8A2BE2', label='Concluintes Parda')  # Azul violeta para linha concluintes parda
sns.lineplot(data=df, x='ano', y='concluintes_amarela', marker='o', color='#9400D3', label='Concluintes Amarela')  # Azul escuro para linha concluintes amarela
sns.lineplot(data=df, x='ano', y='concluintes_indigena', marker='o', color='#4B0082', label='Concluintes Indígena')  # Índigo para linha concluintes indígena

# Adicionando anotações para cada ponto excluindo "Branca" e "CorND"
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingressos_preta'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_preta'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF8C00')
    plt.annotate(f"{df['ingressos_parda'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_parda'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF4500')
    plt.annotate(f"{df['ingressos_amarela'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_amarela'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFA500')
    plt.annotate(f"{df['ingressos_indigena'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_indigena'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#DC143C')

    plt.annotate(f"{df['concluintes_preta'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_preta'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#0000CD')
    plt.annotate(f"{df['concluintes_parda'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_parda'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#8A2BE2')
    plt.annotate(f"{df['concluintes_amarela'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_amarela'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#9400D3')
    plt.annotate(f"{df['concluintes_indigena'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_indigena'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#4B0082')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes de Cotas em Chapecó (Sem Branca e CorND)', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o segundo gráfico excluindo "Branca" e "CorND"
arq_output = '../static/graficos/' + arq_nome + '_sem_branca_cornd.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()