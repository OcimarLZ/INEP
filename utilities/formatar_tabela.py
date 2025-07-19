def dataframe_to_html(df, column_widths, column_names, column_alignments, header_style, row_style):
    # Definindo o estilo CSS
    styles = f"""
        <style>
            table {{width: 100%; border-collapse: collapse;}}
            th {{ background-color: #4CAF50; color: white; {header_style}}}
            td {{{row_style}}}
            tr:nth-child(even) {{background-color: #f2f2f2;}}
            tr:hover {{background-color: #ddd;}}
            .left {{text-align: left;}}
            .center {{text-align: center;}}
            .right {{text-align: right;}}
        </style>
        """

    # Iniciando a tabela HTML
    html = "<html><head>" + styles + "</head><body>"
    html += "<table border='1'>"

    # Adicionando o cabeçalho com larguras específicas
    html += "<tr>"
    for col_name, col_align, col_width in zip(column_names, column_alignments, column_widths):
        html += f"<th class='{col_align}' style='width: {col_width};'>{col_name}</th>"
    html += "</tr>"

    # Adicionando os dados
    for _, row in df.iterrows():
        html += "<tr>"
        for i, item in enumerate(row):
            align = column_alignments[i]
            html += f"<td class='{align}'>{item}</td>"
        html += "</tr>"

    html += "</table></body></html>"
    return html