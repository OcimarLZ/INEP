from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Monta o SQL
sql = """
SELECT 
    cc.ano_censo AS ano,
    SUM(cc.qt_ing_branca) AS ingressantes_branca,
    SUM(cc.qt_ing_parda) AS ingressantes_parda,
    SUM(cc.qt_ing_preta) AS ingressantes_preta,
    SUM(cc.qt_ing_indigena) AS ingressantes_indigena,
    SUM(cc.qt_ing_amarela) AS ingressantes_amarela,
    SUM(cc.qt_ing_cornd) AS ingressantes_cornd,
    SUM(cc.qt_conc_branca) AS concluintes_branca,
    SUM(cc.qt_conc_parda) AS concluintes_parda,
    SUM(cc.qt_conc_preta) AS concluintes_preta,
    SUM(cc.qt_conc_indigena) AS concluintes_indigena,
    SUM(cc.qt_conc_amarela) AS concluintes_amarela,
    SUM(cc.qt_conc_cornd) AS concluintes_cornd
FROM 
    curso_censo cc
WHERE 
    cc.municipio = 4204202 AND cc.ano_censo > 2013
GROUP BY 
    cc.ano_censo
ORDER BY 
    cc.ano_censo
"""
df = carregar_dataframe(sql)

# Substituindo NaN por 0 e convertendo para inteiros
df = df.fillna(0).astype(int)

# Definindo colunas e estilo para o HTML
years = sorted(df['ano'].unique())
column_html = ['150px'] + ['100px'] * (len(df.columns) - 1)
column_alignments = ['left'] + ['right'] * (len(df.columns) - 1)
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"
arq_nome = 'discentes_raca_ingressantes_concluintes'

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Ensino Superior - Nível Graduação: Evolução de Ingressantes e Concluintes por Raça em Chapecó
        </th>
    </tr>
"""

# Adicionando os cabeçalhos das colunas para cada ano
header = '<tr style="background-color: #4CAF50;">'
header += '<th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white;">Ano</th>'
for col in df.columns[1:]:
    header += f'<th style="font-size: 12px; font-family: Tahoma, sans-serif; color: white; text-align: center;">{col.replace("_", " ").capitalize()}</th>'
header += '</tr>'

# Convertendo o DataFrame para texto HTML
html_text = dataframe_to_html(df, column_html, [], column_alignments, header_style, row_style)

# Adicionando o título e cabeçalho no início da tabela
html_text = html_title + header + html_text

# Salvando a tabela HTML
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)
print('Tabela HTML criada com sucesso.')
