import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from bdados.ler_bdados_to_df import carregar_dataframe
import locale

# Configurar a localização para usar o ponto como separador de milhar
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

# SQL para recuperar os dados
sql = """
SELECT 
    cc.ano_censo,
    COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.ies END) AS qtd_ies_presencial,
    COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.ies END) AS qtd_ies_distancia,
    COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 1 THEN cc.municipio END) AS qtd_municipios_presencial,
    COUNT(DISTINCT CASE WHEN cc.tp_modalidade_ensino = 2 THEN cc.municipio END) AS qtd_municipios_distancia
FROM 
    curso_censo cc
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo;
"""

# Carregar os dados
df = carregar_dataframe(sql)

# Converter para inteiros
colunas_int = ['ano_censo', 'qtd_ies_presencial', 'qtd_ies_distancia', 'qtd_municipios_presencial', 'qtd_municipios_distancia']
df[colunas_int] = df[colunas_int].astype(int)

# Função para formatar os rótulos
def formatar_numero(x, pos):
    return locale.format_string('%d', x, grouping=True)

# Função para criar e salvar gráfico
def criar_grafico(df, coluna_y1, coluna_y2, titulo, ylabel, nome_arquivo):
    plt.figure(figsize=(12, 8), facecolor='#F0F0F0')
    ax = plt.gca()
    ax.set_facecolor('#F0F0F0')

    cores = ['#FF0000', '#0000FF']

    sns.lineplot(data=df, x='ano_censo', y=coluna_y1, marker='o', label='Presencial', color=cores[0])
    sns.lineplot(data=df, x='ano_censo', y=coluna_y2, marker='o', label='EaD', color=cores[1])

    ax.set_xlabel('Ano', fontsize=12, fontweight='bold')
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', fontsize='medium')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(formatar_numero))

    for i, row in df.iterrows():
        ax.annotate(formatar_numero(row[coluna_y1], None),
                    (row['ano_censo'], row[coluna_y1]),
                    textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color=cores[0])
        ax.annotate(formatar_numero(row[coluna_y2], None),
                    (row['ano_censo'], row[coluna_y2]),
                    textcoords="offset points", xytext=(0,10), ha='center', fontsize=8, color=cores[1])

    plt.tight_layout()
    arq_output = f'../static/graficos/{nome_arquivo}.png'
    plt.savefig(arq_output, bbox_inches='tight', dpi=300)
    plt.close()
    print(f'Gráfico {nome_arquivo} criado com sucesso.')

# Criar gráfico para IES
criar_grafico(df, 'qtd_ies_presencial', 'qtd_ies_distancia',
              'Evolução da Quantidade de IES por Modalidade',
              'Quantidade de IES',
              'evolucao_ies_por_modalidade')

# Criar gráfico para Municípios
criar_grafico(df, 'qtd_municipios_presencial', 'qtd_municipios_distancia',
              'Evolução da Quantidade de Municípios por Modalidade',
              'Quantidade de Municípios',
              'evolucao_municipios_por_modalidade')

# Criar e salvar a tabela HTML
def criar_tabela_html(df):
    html = """
    <table style="width:100%; border-collapse: collapse; font-family: Arial, sans-serif;">
        <tr style="background-color: #4CAF50; color: white;">
            <th style="padding: 12px; text-align: left;">Ano</th>
            <th style="padding: 12px; text-align: right;">IES Presencial</th>
            <th style="padding: 12px; text-align: right;">IES EaD</th>
            <th style="padding: 12px; text-align: right;">Municípios Presencial</th>
            <th style="padding: 12px; text-align: right;">Municípios EaD</th>
        </tr>
    """
    for _, row in df.iterrows():
        html += f"""
        <tr style="background-color: {'#f2f2f2' if _ % 2 == 0 else 'white'};">
            <td style="padding: 12px; text-align: left;">{row['ano_censo']}</td>
            <td style="padding: 12px; text-align: right;">{formatar_numero(row['qtd_ies_presencial'], None)}</td>
            <td style="padding: 12px; text-align: right;">{formatar_numero(row['qtd_ies_distancia'], None)}</td>
            <td style="padding: 12px; text-align: right;">{formatar_numero(row['qtd_municipios_presencial'], None)}</td>
            <td style="padding: 12px; text-align: right;">{formatar_numero(row['qtd_municipios_distancia'], None)}</td>
        </tr>
        """
    html += "</table>"
    return html

tabela_html = criar_tabela_html(df)
arq_output_html = '../static/tabelas/evolucao_ies_municipios_por_modalidade.html'
with open(arq_output_html, 'w') as file:
    file.write(tabela_html)

print('Tabela HTML de evolução de IES e municípios por modalidade criada com sucesso.')