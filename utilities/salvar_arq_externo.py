def salvar_arquivos(arq_nome, html_text, plt):
    # Salvar a tabela em formato HTML
    arq_output = '../static/tabelas/' + arq_nome + '.html'
    with open(arq_output, 'w') as file:
        file.write(html_text)
    print('Tabela HTML criada com sucesso.')
    # Salvando o arquivo plt
    if plt:
        arq_output = '../static/graficos/' + arq_nome + '.png'
        plt.show
        plt.savefig(arq_output)
