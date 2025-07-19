import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    m.nome,
    cc.ano_censo,
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
    m.nome, cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Município', 'Ano', 'Ingresso Jovens', 'Ingresso Adultos', 'Ingresso Segunda Idade', 'Ingresso Terceira Idade',
                'Concluintes Jovens', 'Concluintes Adultos', 'Concluintes Segunda Idade', 'Concluintes Terceira Idade']
column_alignments = ['left', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right', 'right']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'cursos_concluintes_faixa_etaria'

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
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn com fundo verde muito claro
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo verde muito claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo verde muito claro para os eixos

# Função para plotar uma linha, se a coluna não for zero
def plot_line(data, x, y, label, color):
    if y in data.columns:
        sns.lineplot(data=data, x=x, y=y, marker='o', label=label, color=color)

# Plotando as linhas para ingressos
plot_line(df, 'ano_censo', 'ingresso_jovens', 'Ingresso Jovens', '#FF6347')  # Tomate para linha ingresso jovens
plot_line(df, 'ano_censo', 'ingresso_adultos', 'Ingresso Adultos', '#1E90FF')  # Azul dodger para linha ingresso adultos
plot_line(df, 'ano_censo', 'ingresso_segunda_idade', 'Ingresso Segunda Idade', '#32CD32')  # Verde lima para linha ingresso segunda idade
plot_line(df, 'ano_censo', 'ingresso_terceira_idade', 'Ingresso Terceira Idade', '#FFD700')  # Ouro para linha ingresso terceira idade

# Plotando as linhas para concluintes
plot_line(df, 'ano_censo', 'concluintes_jovens', 'Concluintes Jovens', '#FF8C00')  # Laranja escuro para linha concluintes jovens
plot_line(df, 'ano_censo', 'concluintes_adultos', 'Concluintes Adultos', '#6A5ACD')  # Azul ardósia para linha concluintes adultos
plot_line(df, 'ano_censo', 'concluintes_segunda_idade', 'Concluintes Segunda Idade', '#008080')  # Verde água para linha concluintes segunda idade
plot_line(df, 'ano_censo', 'concluintes_terceira_idade', 'Concluintes Terceira Idade', '#DA70D6')  # Orquídea para linha concluintes terceira idade

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingresso_jovens'].iloc[i]}", (df['ano_censo'].iloc[i], df['ingresso_jovens'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    plt.annotate(f"{df['ingresso_adultos'].iloc[i]}", (df['ano_censo'].iloc[i], df['ingresso_adultos'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['ingresso_segunda_idade'].iloc[i]}", (df['ano_censo'].iloc[i], df['ingresso_segunda_idade'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#32CD32')
    plt.annotate(f"{df['ingresso_terceira_idade'].iloc[i]}", (df['ano_censo'].iloc[i], df['ingresso_terceira_idade'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFD700')
    plt.annotate(f"{df['concluintes_jovens'].iloc[i]}", (df['ano_censo'].iloc[i], df['concluintes_jovens'].iloc[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#FF8C00')
    plt.annotate(f"{df['concluintes_adultos'].iloc[i]}", (df['ano_censo'].iloc[i], df['concluintes_adultos'].iloc[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#6A5ACD')
    plt.annotate(f"{df['concluintes_segunda_idade'].iloc[i]}", (df['ano_censo'].iloc[i], df['concluintes_segunda_idade'].iloc[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#008080')
    plt.annotate(f"{df['concluintes_terceira_idade'].iloc[i]}", (df['ano_censo'].iloc[i], df['concluintes_terceira_idade'].iloc[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='#DA70D6')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes em Chapecó por Faixa Etária', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()
