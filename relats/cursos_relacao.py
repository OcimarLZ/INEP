import pandas as pd
from bdados.ler_bdados_to_df import carregar_dataframe

# Consulta SQL
sql = """
SELECT 
    i.nome AS instituicao,
    i.sigla,
    me.nome AS modalidade,
    ar.nome AS area,
    cu.nome AS curso,
    cc.ano_censo AS ano,
    cc.qt_vg_total AS vagas,
    cc.qt_ing AS ingres,
    cc.qt_mat AS matric,
    cc.qt_conc AS concl,
    cc.qt_sit_trancada AS tranc,
    cc.qt_sit_desvinculado AS desist
FROM 
    curso_censo cc 
JOIN 
    curso cu ON cu.codigo = cc.curso
JOIN 
    tp_modal_ensino me ON me.codigo = cc.tp_modalidade_ensino 
JOIN 
    area ar ON ar.codigo = cc.area_geral 
JOIN 
    ies i ON i.codigo = cc.ies
JOIN 
    municipio m ON m.codigo = i.municipio 
WHERE 
    cc.municipio = '4204202' and cc.ano_censo > 2013
GROUP BY 
    i.nome, i.sigla, me.nome, ar.nome, cu.nome, cc.ano_censo
ORDER BY 
    i.nome, i.sigla, me.nome, ar.nome, cu.nome, cc.ano_censo
"""
df = carregar_dataframe(sql)


def gerar_html_relatorio(df):
    # Estilos CSS com alinhamento à direita para colunas numéricas
    styles = """
    <style>
        body { font-family: Tahoma, sans-serif; color: #333; margin: 20px; }
        h2 { color: #2E7D32; }
        .report-container { width: 100%; }
        .institution-header { background-color: #4CAF50; color: white; padding: 10px; font-weight: bold; font-size: 16px; }
        .course-table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        .course-table th, .course-table td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        .course-table th { background-color: #4CAF50; color: white; }
        .course-table td { background-color: #f9f9f9; }
        .course-table tr:nth-child(even) { background-color: #f2f2f2; }
        .course-table tr:hover { background-color: #ddd; }
        .right-align { text-align: right; }  /* Classe para alinhar à direita */
    </style>
    """

    # HTML inicial com título
    html = f"<html><head>{styles}</head><body>"
    html += "<h2>Relatório de Instituições de Ensino e Cursos</h2>"

    # Variáveis de controle
    instituicao_atual = None
    last_modalidade, last_area, last_curso = None, None, None  # Armazena o último valor exibido para cada coluna

    # Loop pelas linhas do DataFrame
    for _, row in df.iterrows():
        if row['instituicao'] != instituicao_atual:
            # Fecha a tabela anterior e inicia uma nova seção para a nova instituição
            if instituicao_atual is not None:
                html += "</table><br>"

            instituicao_atual = row['instituicao']
            last_modalidade, last_area, last_curso = None, None, None  # Reset para nova instituição

            # Cabeçalho da instituição
            html += f"<div class='institution-header'>{instituicao_atual} ({row['sigla']})</div>"

            # Início da tabela para os cursos
            html += """
            <table class="course-table">
                <tr>
                    <th>Modalidade</th>
                    <th>Área</th>
                    <th>Curso</th>
                    <th>Ano</th>
                    <th style="text-align: right;">Vagas</th>
                    <th style="text-align: right;">Ingressos</th>
                    <th style="text-align: right;">Matrículas</th>
                    <th style="text-align: right;">Concluídos</th>
                    <th style="text-align: right;">Trancados</th>
                    <th style="text-align: right;">Desistentes</th>
                </tr>
            """

        # Definindo o texto a ser exibido em cada coluna
        modalidade = "" if row['modalidade'] == last_modalidade else row['modalidade']
        area = "" if row['area'] == last_area else row['area']
        curso = "" if row['curso'] == last_curso else row['curso']

        # Atualizando os últimos valores exibidos
        last_modalidade, last_area, last_curso = row['modalidade'], row['area'], row['curso']

        # Linha para os dados do curso, com alinhamento à direita nas colunas numéricas
        html += f"""
        <tr>
            <td>{modalidade}</td>
            <td>{area}</td>
            <td>{curso}</td>
            <td>{row['ano']}</td>
            <td style="text-align: right;">{row['vagas']}</td>
            <td style="text-align: right;">{row['ingres']}</td>
            <td style="text-align: right;">{row['matric']}</td>
            <td style="text-align: right;">{row['concl']}</td>
            <td style="text-align: right;">{row['tranc']}</td>
            <td style="text-align: right;">{row['desist']}</td>
        </tr>
        """

    # Finaliza o HTML
    html += "</table></body></html>"
    return html


# Gera o HTML e salva no arquivo
html_text = gerar_html_relatorio(df)
with open("relatorio_ies_cursos.html", "w", encoding="utf-8") as file:
    file.write(html_text)

print("Relatório HTML com estilo aprimorado e alinhamento à direita nas colunas numéricas gerado com sucesso.")
