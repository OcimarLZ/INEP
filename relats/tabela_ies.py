import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
# Carregando dados de uma tabela para um DataFrame
sql = """
SELECT 
    cc.ano_censo as ano,
    COUNT(DISTINCT cc.ies) AS total_ies
FROM 
    curso_censo cc
WHERE 
    cc.municipio = 4204202 and cc.ano_censo > 2000
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""
df = carregar_dataframe(sql)

# Redefinindo a lista de tamanhos para o formato html
column_html = ['50px', '100px']
column_names = ['Ano', 'Instituições']
column_alignments = ['left', 'right']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"     # Estilo das linhas de dados
arq_nome = 'ies_ano_qtde_geral'

# HTML para o título da tabela
html_title = """
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="2" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó
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

arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(10, 6), facecolor='#F0F0F0')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

lineplot_cursos = sns.lineplot(data=df, x='ano', y='total_ies', marker='o', label='Instituições', color='#98FB98')  # Verde claro para a linha

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['total_ies'].iloc[i]}", (df['ano'].iloc[i], df['total_ies'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Ano')
plt.ylabel('Qtde de instituições')
plt.title('Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó', color='#556B2F')  # Verde oliva forte para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()