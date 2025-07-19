import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    COUNT(DISTINCT CASE WHEN tca.codigo = 1 THEN cc.ies ELSE NULL END) AS federal,
    COUNT(DISTINCT CASE WHEN tca.codigo = 2 THEN cc.ies ELSE NULL END) AS estadual,
    COUNT(DISTINCT CASE WHEN tca.codigo = 3 THEN cc.ies ELSE NULL END) AS municipal,
    COUNT(DISTINCT CASE WHEN tca.codigo = 4 THEN cc.ies ELSE NULL END) AS privada_cfl,
    COUNT(DISTINCT CASE WHEN tca.codigo = 5 THEN cc.ies ELSE NULL END) AS privada_sfl,
    COUNT(DISTINCT CASE WHEN tca.codigo = 6 THEN cc.ies ELSE NULL END) AS privada,
    COUNT(DISTINCT CASE WHEN tca.codigo = 7 THEN cc.ies ELSE NULL END) AS especial,
    COUNT(DISTINCT CASE WHEN tca.codigo = 8 THEN cc.ies ELSE NULL END) AS comunitaria,
    COUNT(DISTINCT CASE WHEN tca.codigo = 9 THEN cc.ies ELSE NULL END) AS confessional
FROM 
    curso_censo cc
JOIN 
    tp_categoria_administrativa tca ON cc.categoria = tca.codigo
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
df = df.rename(columns={'privada_sfl': 'privada sem fins lucrativos', 'privada_cfl': 'privada com fins lucrativos'})

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['50px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano'] + [col.capitalize() for col in df.columns[1:]]
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'ies_ano_categoria_administrativa_qtde'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó por Categoria Administrativa
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
plt.figure(figsize=(10, 6), facecolor='#F0F0F0')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Função para plotar uma linha, se a coluna não for zero
def plot_line(data, x, y, label, color):
    if y in data.columns:
        sns.lineplot(data=data, x=x, y=y, marker='o', label=label, color=color)

# Plotando as linhas
plot_line(df, 'ano', 'federal', 'Federal', '#FF6347')  # Tomate para linha federal
plot_line(df, 'ano', 'estadual', 'Estadual', '#1E90FF')  # Azul dodger para linha estadual
plot_line(df, 'ano', 'municipal', 'Municipal', '#FFA500')  # Laranja para linha municipal
plot_line(df, 'ano', 'privada com fins lucrativos', 'Privada com fins lucrativos', '#32CD32')  # Verde lima para linha privada cfl
plot_line(df, 'ano', 'privada sem fins lucrativos', 'Privada sem fins lucrativos', '#8A2BE2')  # Azul violeta para lima para linha privada sfl
plot_line(df, 'ano', 'privada', 'Privada', '#1E90FF')  # Azul dogdger para linha privada
plot_line(df, 'ano', 'especial', 'Especial', '#FF69B4')  # Rosa Choque para linha especial
plot_line(df, 'ano', 'comunitaria', 'Comunitaria', '#48D1CC')  # Turquesa Médio para linha comunitária
plot_line(df, 'ano', 'confessional', 'Confessional', '#FFD700')  # Ouro para linha confessional

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    if 'federal' in df.columns:
        plt.annotate(f"{df['federal'].iloc[i]}", (df['ano'].iloc[i], df['federal'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF6347')
    if 'estadual' in df.columns:
        plt.annotate(f"{df['estadual'].iloc[i]}", (df['ano'].iloc[i], df['estadual'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    if 'municipal' in df.columns:
        plt.annotate(f"{df['municipal'].iloc[i]}", (df['ano'].iloc[i], df['municipal'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFA500')
    if 'privada' in df.columns:
        plt.annotate(f"{df['privada'].iloc[i]}", (df['ano'].iloc[i], df['privada'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')
    if 'privada com fins lucrativos' in df.columns:
        plt.annotate(f"{df['privada com fins lucrativos'].iloc[i]}", (df['ano'].iloc[i], df['privada com fins lucrativos'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#32CD32')
    if 'privada sem fins lucrativos' in df.columns:
        plt.annotate(f"{df['privada sem fins lucrativos'].iloc[i]}", (df['ano'].iloc[i], df['privada sem fins lucrativos'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#8A2BE2')
    if 'especial' in df.columns:
        plt.annotate(f"{df['especial'].iloc[i]}", (df['ano'].iloc[i], df['especial'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF69B4')
    if 'comunitaria' in df.columns:
        plt.annotate(f"{df['comunitaria'].iloc[i]}", (df['ano'].iloc[i], df['comunitaria'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#48D1CC')
    if 'confessional' in df.columns:
        plt.annotate(f"{df['confessional'].iloc[i]}", (df['ano'].iloc[i], df['confessional'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFD700')

plt.xlabel('Ano')
plt.ylabel('Quantidade de instituições')
plt.title('Ensino Superior - Nível Graduação: Evolução do número de IES em Chapecó por categoria administrativa', color='#556B2F')  # Verde oliva forte para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.2), ncol=3, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()