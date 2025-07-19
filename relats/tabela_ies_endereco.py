import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.formatar_tabela import dataframe_to_html

# Consulta SQL para obter os dados de endereço das IES
sql = """
SELECT DISTINCT
    i.nome AS ies,
    i.sigla,
    i.endereco_logradouro || ' ' || i.endereco_numero || ' ' || i.endereco_complemento AS endereco,
    i.bairro,
    i.cep
FROM 
    curso_censo cc
JOIN 
    ies i ON i.codigo = cc.ies 
WHERE
    cc.municipio = 4204202 AND cc.ano_censo > 2013
ORDER BY 
    i.nome, i.sigla;
"""

# Carregando os dados da consulta em um DataFrame
df = carregar_dataframe(sql)

# Definindo as configurações de exibição da tabela
column_html = ['200px', '100px', '300px', '150px', '100px']  # Largura das colunas
column_names = ['IES', 'Sigla', 'Endereço', 'Bairro', 'CEP']  # Nomes das colunas para o cabeçalho
column_alignments = ['left', 'center', 'left', 'left', 'center']  # Alinhamento das colunas
header_style = "font-size: 12px; font-family: Tahoma, sans-serif; background-color: #4CAF50; color: white;"  # Estilo do cabeçalho
row_style = "font-size: 10px; font-family: Tahoma, sans-serif;"  # Estilo das linhas de dados

# HTML para o título da tabela
html_title = f"""
<table style="width: 100%; border-collapse: collapse;">
    <tr style="background-color: #2E7D32;">
        <th colspan="{len(df.columns)}" style="font-size: 14px; font-family: Tahoma, sans-serif; color: white; padding: 10px; text-align: center;">
            Tabela de Endereços das Instituições de Ensino Superior em Chapecó
        </th>
    </tr>
</table>
"""

# Convertendo o DataFrame para HTML
html_text = dataframe_to_html(df, column_html, column_names, column_alignments, header_style, row_style)

# Adicionando o título no início da tabela
html_text = html_title + html_text

# Salvando a tabela HTML
arq_nome = 'tabela_ies_endereco'
arq_output = '../static/tabelas/' + arq_nome + '.html'
with open(arq_output, 'w') as file:
    file.write(html_text)

print('Tabela HTML criada com sucesso.')
