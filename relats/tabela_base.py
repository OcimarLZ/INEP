import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html
from utilities.salvar_arq_externo import salvar_arquivos

#Monta o Sql
# Carregando dados de uma tabela para um DataFrame
sql = """
select 
m.nome,
cc.ano_censo,
sum(cc.qt_curso) cursos,
sum(cc.qt_vg_total) vagas,
sum(cc.qt_ing) ingressos,
sum(cc.qt_mat) matriculas,
sum(cc.qt_conc) concluintes
from curso_censo cc  
JOIN municipio m ON m.codigo = cc.municipio
where cc.municipio = 4204202 and cc.ano_censo > 2013
GROUP BY 
m.nome, cc.ano_censo
"""
df = carregar_dataframe(sql)
# Deletar a coluna 'Municipio'
df = df.drop(columns=['nome'])

# Redefinindo a lista de tamanhos para o formato html
column_html = ['50px', '100px', '100px', '100px', '100px', '100px']
column_names = ['Ano', 'Cursos', 'Vagas', 'Ingressos', 'Matrículas', 'Concluintes']
column_alignments = ['left', 'right', 'right', 'right', 'right', 'right']  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif;"  # Estilo do cabeçalho
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"     # Estilo das linhas de dados
arq_nome = 'dados_gerais'

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)


# Criando um gráfico de linhas utilizando Seaborn
plt.figure(figsize=(10, 6))
lineplot_cursos = sns.lineplot(data=df, x='ano_censo', y='cursos', marker='o', label='Cursos')
lineplot_vagas = sns.lineplot(data=df, x='ano_censo', y='vagas', marker='o', label='Vagas')
lineplot_ingressos = sns.lineplot(data=df, x='ano_censo', y='ingressos', marker='o', label='Ingressos')
lineplot_matriculas = sns.lineplot(data=df, x='ano_censo', y='matriculas', marker='o', label='Matrículas')
lineplot_concluintes = sns.lineplot(data=df, x='ano_censo', y='concluintes', marker='o', label='Concluintes')

# Adicionando anotações para cada ponto
for i in range(df.shape[0]):
    plt.annotate(f"{df['cursos'].iloc[i]}", (df['ano_censo'].iloc[i], df['cursos'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"{df['vagas'].iloc[i]}", (df['ano_censo'].iloc[i], df['vagas'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"{df['ingressos'].iloc[i]}", (df['ano_censo'].iloc[i], df['ingressos'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"{df['matriculas'].iloc[i]}", (df['ano_censo'].iloc[i], df['matriculas'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')
    plt.annotate(f"{df['concluintes'].iloc[i]}", (df['ano_censo'].iloc[i], df['concluintes'].iloc[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Ano Censo')
plt.ylabel('Quantidade')
plt.title('Evolução de Cursos, Vagas, Ingressos, Matrículas e Concluintes ao longo dos Anos')
plt.legend()
plt.grid(True)
plt.show()

# Faz o gráfico
# Criando um gráfico de linhas utilizando Seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(data=df, x='ano_censo', y='cursos', marker='o', label='Cursos')
sns.lineplot(data=df, x='ano_censo', y='vagas', marker='o', label='Vagas')
sns.lineplot(data=df, x='ano_censo', y='ingressos', marker='o', label='Ingressos')
sns.lineplot(data=df, x='ano_censo', y='matriculas', marker='o', label='Matrículas')
sns.lineplot(data=df, x='ano_censo', y='concluintes', marker='o', label='Concluintes')
plt.xlabel('Ano Censo')
plt.ylabel('Quantidade')
plt.title('Evolução de Cursos, Vagas, Ingressos, Matrículas e Concluintes ao longo dos Anos')
plt.legend()
plt.grid(True)
plt.show()
# Salvar os arquivos (tabela e gráficos)
salvar_arquivos(arq_nome, html_text, plt)
