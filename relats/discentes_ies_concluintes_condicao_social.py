import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_conc_reserva_vaga) AS total_reserva_vaga,
    SUM(cc.qt_conc_rvredepublica) AS total_rvredepublica,
    SUM(cc.qt_conc_rvetnico) AS total_rvetnico,
    SUM(cc.qt_conc_rvpdef) AS total_rvpdef,
    SUM(cc.qt_conc_rvsocial_rf) AS total_rvsocial_rf,
    SUM(cc.qt_conc_rvoutros) AS total_rvoutros,
    SUM(cc.qt_conc_procescpublica) AS total_procescpublica,
    SUM(cc.qt_conc_procescprivada) AS total_procescprivada,
    SUM(cc.qt_conc_procnaoinformada) AS total_procnaoinformada,
    SUM(cc.qt_conc_parfor) AS total_parfor,
    SUM(cc.qt_conc_apoio_social) AS total_apoio_social,
    SUM(cc.qt_conc_ativ_extracurricular) AS total_ativ_extracurricular,
    SUM(cc.qt_conc_mob_academica) AS total_mob_academica
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

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype(int)

# Pivotando o DataFrame para que os anos estejam nas colunas e as condições sociais nas linhas
df_pivot = df.melt(id_vars=['ano'], var_name='Condição Social', value_name='Quantidade')
df_pivot = df_pivot.pivot(index='Condição Social', columns='ano', values='Quantidade').fillna(0).astype(int)

# Redefinindo a lista de tamanhos para o formato HTML
column_html = ['300px'] + ['100px'] * len(df_pivot.columns)
column_names = ['Condição Social'] + [str(year) for year in df_pivot.columns]
column_alignments = ['left'] + ['right'] * len(df_pivot.columns)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'concluintes_condicao_social_qtde_pivot'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df_pivot.columns) + 1}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Concluintes por Condição Social em Chapecó
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df_pivot.reset_index(), column_html, column_names, column_alignments, header_style, row_style)

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
plt.figure(figsize=(10, 6), facecolor='#CCFFCC')  # Fundo cinza claro para a figura, largura ajustada
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
sns.lineplot(data=df, x='ano', y='total_reserva_vaga', marker='o', label='Reserva de Vaga', color='#006400')
sns.lineplot(data=df, x='ano', y='total_rvredepublica', marker='o', label='Rede Pública', color='#FF6347')
sns.lineplot(data=df, x='ano', y='total_rvetnico', marker='o', label='Cunho Étnico', color='#1E90FF')
sns.lineplot(data=df, x='ano', y='total_rvpdef', marker='o', label='Pessoas com Deficiência', color='#FFA500')
sns.lineplot(data=df, x='ano', y='total_rvsocial_rf', marker='o', label='Cunho Social RF', color='#9400D3')
sns.lineplot(data=df, x='ano', y='total_rvoutros', marker='o', label='Outras Reservas', color='#8A2BE2')
sns.lineplot(data=df, x='ano', y='total_procescpublica', marker='o', label='Proc. Escola Pública', color='#FF1493')
sns.lineplot(data=df, x='ano', y='total_procescprivada', marker='o', label='Proc. Escola Privada', color='#8B4513')
sns.lineplot(data=df, x='ano', y='total_procnaoinformada', marker='o', label='Proc. Não Informada', color='#2E8B57')
sns.lineplot(data=df, x='ano', y='total_parfor', marker='o', label='Parfor', color='#4682B4')
sns.lineplot(data=df, x='ano', y='total_apoio_social', marker='o', label='Apoio Social', color='#D2691E')
sns.lineplot(data=df, x='ano', y='total_ativ_extracurricular', marker='o', label='Ativ. Extracurricular', color='#DA70D6')
sns.lineplot(data=df, x='ano', y='total_mob_academica', marker='o', label='Mobilidade Acadêmica', color='#32CD32')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['total_reserva_vaga'].iloc[i]}", (df['ano'].iloc[i], df['total_reserva_vaga'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#006400')
    plt.annotate(f"{df['total_rvredepublica'].iloc[i]}", (df['ano'].iloc[i], df['total_rvredepublica'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF6347')
    plt.annotate(f"{df['total_rvetnico'].iloc[i]}", (df['ano'].iloc[i], df['total_rvetnico'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#1E90FF')
    plt.annotate(f"{df['total_rvpdef'].iloc[i]}", (df['ano'].iloc[i], df['total_rvpdef'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FFA500')
    plt.annotate(f"{df['total_rvsocial_rf'].iloc[i]}", (df['ano'].iloc[i], df['total_rvsocial_rf'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#9400D3')
    plt.annotate(f"{df['total_rvoutros'].iloc[i]}", (df['ano'].iloc[i], df['total_rvoutros'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8A2BE2')
    plt.annotate(f"{df['total_procescpublica'].iloc[i]}", (df['ano'].iloc[i], df['total_procescpublica'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#FF1493')
    plt.annotate(f"{df['total_procescprivada'].iloc[i]}", (df['ano'].iloc[i], df['total_procescprivada'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#8B4513')
    plt.annotate(f"{df['total_procnaoinformada'].iloc[i]}", (df['ano'].iloc[i], df['total_procnaoinformada'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#2E8B57')
    plt.annotate(f"{df['total_parfor'].iloc[i]}", (df['ano'].iloc[i], df['total_parfor'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#4682B4')
    plt.annotate(f"{df['total_apoio_social'].iloc[i]}", (df['ano'].iloc[i], df['total_apoio_social'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#D2691E')
    plt.annotate(f"{df['total_ativ_extracurricular'].iloc[i]}", (df['ano'].iloc[i], df['total_ativ_extracurricular'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#DA70D6')
    plt.annotate(f"{df['total_mob_academica'].iloc[i]}", (df['ano'].iloc[i], df['total_mob_academica'].iloc[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='#32CD32')

plt.xlabel('Ano')
plt.ylabel('Quantidade de Concluintes')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Concluintes por Condição Social em Chapecó', color='#000000')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='small')  # Ajustando a posição da legenda
plt.grid(True)

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()

print('Gráfico criado com sucesso.')
