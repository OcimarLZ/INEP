import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_reserva_vaga) AS ingressos_reserva_vaga,
    SUM(cc.qt_ing_rvredepublica) AS ingressos_rede_publica,
    SUM(cc.qt_ing_rvetnico) AS ingressos_cunho_tecnico,
    SUM(cc.qt_ing_rvpdef) AS ingressos_pessoa_ne,
    SUM(cc.qt_ing_rvsocial_rf) AS ingressos_cunho_social,
    SUM(cc.qt_ing_rvoutros) AS ingressos_outros,
    SUM(cc.qt_conc_reserva_vaga) AS concluintes_reserva_vaga,
    SUM(cc.qt_conc_rvredepublica) AS concluintes_rede_publica,
    SUM(cc.qt_conc_rvetnico) AS concluintes_cunho_tecnico,
    SUM(cc.qt_conc_rvpdef) AS concluintes_pessoa_ne,
    SUM(cc.qt_conc_rvsocial_rf) AS concluintes_cunho_social,
    SUM(cc.qt_conc_rvoutros) AS concluintes_outros
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
column_names = ['Ano', 'Ingressos Reserva Vaga', 'Concluintes Reserva Vaga', 'Ingressos Rede Pública', 'Concluintes Rede Pública',
                'Ingressos Cunho Técnico', 'Concluintes Cunho Técnico', 'Ingressos Pessoa NE', 'Concluintes Pessoa NE',
                'Ingressos Cunho Social', 'Concluintes Cunho Social', 'Ingressos Outros', 'Concluintes Outros']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho com verde vivo e texto branco
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados
arq_nome = 'curso_discentes_formas_Ingresso'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes por Forma de Ingresso em Chapecó
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

# Criando o gráfico de linhas com todos os dados utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(12, 8), facecolor='#CCFFCC')  # Fundo cinza claro para a figura
ax = plt.gca()
ax.set_facecolor('#F0F0F0')  # Fundo cinza claro para os eixos

# Plotando as linhas
sns.lineplot(data=df, x='ano', y='ingressos_reserva_vaga', marker='o', color='#FFD700', label='Ingressos Reserva Vaga')
sns.lineplot(data=df, x='ano', y='concluintes_reserva_vaga', marker='o', color='#1E90FF', label='Concluintes Reserva Vaga')

sns.lineplot(data=df, x='ano', y='ingressos_rede_publica', marker='o', color='#FF8C00', label='Ingressos Rede Pública')
sns.lineplot(data=df, x='ano', y='concluintes_rede_publica', marker='o', color='#0000CD', label='Concluintes Rede Pública')

sns.lineplot(data=df, x='ano', y='ingressos_cunho_tecnico', marker='o', color='#FF4500', label='Ingressos Cunho Técnico')
sns.lineplot(data=df, x='ano', y='concluintes_cunho_tecnico', marker='o', color='#8A2BE2', label='Concluintes Cunho Técnico')

sns.lineplot(data=df, x='ano', y='ingressos_pessoa_ne', marker='o', color='#FFA500', label='Ingressos Pessoa NE')
sns.lineplot(data=df, x='ano', y='concluintes_pessoa_ne', marker='o', color='#9400D3', label='Concluintes Pessoa NE')

sns.lineplot(data=df, x='ano', y='ingressos_cunho_social', marker='o', color='#DC143C', label='Ingressos Cunho Social')
sns.lineplot(data=df, x='ano', y='concluintes_cunho_social', marker='o', color='#4B0082', label='Concluintes Cunho Social')

sns.lineplot(data=df, x='ano', y='ingressos_outros', marker='o', color='#B22222', label='Ingressos Outros')
sns.lineplot(data=df, x='ano', y='concluintes_outros', marker='o', color='#6A5ACD', label='Concluintes Outros')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['ingressos_reserva_vaga'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_reserva_vaga'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFD700')
    plt.annotate(f"{df['concluintes_reserva_vaga'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_reserva_vaga'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#1E90FF')

    plt.annotate(f"{df['ingressos_rede_publica'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_rede_publica'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF8C00')
    plt.annotate(f"{df['concluintes_rede_publica'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_rede_publica'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#0000CD')

    plt.annotate(f"{df['ingressos_cunho_tecnico'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_cunho_tecnico'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FF4500')
    plt.annotate(f"{df['concluintes_cunho_tecnico'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_cunho_tecnico'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#8A2BE2')

    plt.annotate(f"{df['ingressos_pessoa_ne'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_pessoa_ne'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#FFA500')
    plt.annotate(f"{df['concluintes_pessoa_ne'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_pessoa_ne'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#9400D3')

    plt.annotate(f"{df['ingressos_cunho_social'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_cunho_social'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#DC143C')
    plt.annotate(f"{df['concluintes_cunho_social'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_cunho_social'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#4B0082')

    plt.annotate(f"{df['ingressos_outros'].iloc[i]}", (df['ano'].iloc[i], df['ingressos_outros'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#B22222')
    plt.annotate(f"{df['concluintes_outros'].iloc[i]}", (df['ano'].iloc[i], df['concluintes_outros'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center', color='#6A5ACD')

plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.title('Ensino Superior - Nível Graduação: Evolução dos Ingressos e Concluintes por Forma de Ingresso em Chapecó', color='#000000')  # Preto para o título
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.3), ncol=2, fontsize='small')  # Mover legenda para o rodapé
plt.grid(True)

# Salvando o gráfico com todos os dados
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.tight_layout()
plt.savefig(arq_output, bbox_inches='tight')
plt.show()
plt.close()