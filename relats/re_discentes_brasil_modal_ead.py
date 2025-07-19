import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html
import locale

# Configurar a localização para usar o ponto como separador de milhar
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# Monta o SQL para dados dos discentes
sql = """
select 
cc.ano_censo as ano,
sum(cc.qt_vg_total) vagas,
sum(cc.qt_inscrito_total) inscritos,
sum(cc.qt_ing) ingressantes,
sum(cc.qt_mat) matriculas
from curso_censo cc 
where cc.tp_modalidade_ensino = 2
group by 1
order by 1
"""
df = carregar_dataframe(sql)

# Preenchendo valores NaN com 0 e convertendo para inteiros
df = df.fillna(0).astype(int)

# Função para formatar números com separador de milhar
def formatar_numero(valor):
    return locale.format_string('%d', valor, grouping=True)

# Aplicar a formatação nas colunas numéricas
colunas_numericas = ['vagas', 'inscritos', 'ingressantes', 'matriculas']
for coluna in colunas_numericas:
    df[coluna] = df[coluna].apply(formatar_numero)

# Convertendo o DataFrame para o formato HTML
column_html = ['150px'] + ['100px'] * (len(df.columns) - 1)
column_names = ['Ano', 'Vagas', 'Inscritos', 'Ingressantes', 'Matrículas']
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)  # Alinhamentos para cada coluna do cabeçalho
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 're_evolucao_discentes_brasil_ead'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Evolução de Vagas, Inscritos, Ingressantes e Matrículas por Ano - EAD
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML de evolução dos discentes criada com sucesso.')

# Restaurar o DataFrame para valores numéricos para o gráfico
df[colunas_numericas] = df[colunas_numericas].apply(lambda x: x.str.replace('.', '').astype(int))

# Criando um gráfico de linhas utilizando Seaborn com fundo cinza claro
plt.figure(figsize=(12, 8), facecolor='#F0F0F0')  # Aumentei a altura para acomodar a legenda
ax = plt.gca()
ax.set_facecolor('#F0F0F0')

# Novas cores
cores = ['#FF0000', '#FFA500', '#008000', '#0000FF']

# Plotando as linhas para cada métrica
sns.lineplot(data=df, x='ano', y='vagas', marker='o', label='Vagas', color=cores[0])
sns.lineplot(data=df, x='ano', y='inscritos', marker='o', label='Inscritos', color=cores[1])
sns.lineplot(data=df, x='ano', y='ingressantes', marker='o', label='Ingressantes', color=cores[2])
sns.lineplot(data=df, x='ano', y='matriculas', marker='o', label='Matrículas', color=cores[3])

# Função para formatar os rótulos em milhões
def milhoes(x, pos):
    return f'{x/1e6:.1f}M'

# Adicionando anotações para cada ponto
for i, coluna in enumerate(['vagas', 'inscritos', 'ingressantes', 'matriculas']):
    for j in range(df.shape[0]):
        valor = df[coluna].iloc[j]
        plt.annotate(f'{valor/1e6:.1f}M', (df['ano'].iloc[j], valor),
                     textcoords="offset points", xytext=(0, 10),
                     ha='center', color=cores[i], fontweight='bold')

plt.xlabel('Ano', fontsize=12, fontweight='bold')
plt.ylabel('Quantidade (em milhões)', fontsize=12, fontweight='bold')
plt.title('Evolução de Vagas, Inscritos, Ingressantes e Matrículas por Ano no Brasil - EAD',
          color='#000000', fontsize=14, fontweight='bold')

# Ajustando a posição da legenda para a parte inferior
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=4, fontsize='medium')

plt.grid(True, linestyle='--', alpha=0.7)

# Formatando o eixo Y para mostrar valores em milhões
ax.yaxis.set_major_formatter(plt.FuncFormatter(milhoes))

# Ajustando os limites do eixo Y para dar um pouco mais de espaço acima do valor máximo
max_value = df[['vagas', 'inscritos', 'ingressantes', 'matriculas']].max().max()
plt.ylim(0, max_value * 1.1)

# Ajustando o layout para acomodar a legenda
plt.tight_layout()
plt.subplots_adjust(bottom=0.2)  # Aumenta o espaço na parte inferior para a legenda

# Salvando o gráfico
arq_output = '../static/graficos/' + arq_nome + '.png'
plt.savefig(arq_output, bbox_inches='tight', dpi=300)
plt.show()
plt.close()

print('Gráfico de evolução dos discentes criado com sucesso.')