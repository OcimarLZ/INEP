import pandas as pd
import os
from utilities.log import logger

def create_summary_spreadsheet(input_file, output_file, formato, separador, encode):
    # Ler a planilha de entrada
    if formato == 'CSV':
        df = pd.read_csv(input_file, nrows=1, delimiter= separador, encoding=encode)
    else:
        df = pd.read_excel(input_file, nrows=1)  # Ajuste 'skiprows' conforme necessário

    # Inicializar listas para armazenar os nomes das colunas e os tipos de dados
    nome_atributos = []
    tipo_dados = []
    # Iterar sobre as colunas da planilha de entrada
    for col in df.columns:
        nome_atributos.append(col)
        tipo_dado = type(df.at[0, col]).__name__
        tipo_dados.append(tipo_dado)

    # Criar um novo DataFrame com os nomes das colunas e os tipos de dados
    summary_df = pd.DataFrame({
        'Column Name': nome_atributos,
        'Data Type': tipo_dados
    })

    # Salvar o DataFrame resumido em uma nova planilha
    summary_df.to_excel(output_file, index=False)

# Alinhar 2 dataframes
def align_dataframes(a_df, b_df):
    """
    Alinha dois DataFrames com base nos índices e preenche valores ausentes com NaN.

    Args:
    a_df (pd.DataFrame): Primeiro DataFrame
    b_df (pd.DataFrame): Segundo DataFrame

    Returns:
    tuple: Dois DataFrames alinhados
    """
    a_df_aligned, b_df_aligned = a_df.align(b_df, join='outer', axis=0, fill_value=pd.NA)
    return a_df_aligned, b_df_aligned

# Comparar 2 dataframes
def compare_dataframes(a_df, b_df):
    """
    Compara dois DataFrames e retorna um DataFrame com as diferenças.

    Args:
    a_df (pd.DataFrame): Primeiro DataFrame
    b_df (pd.DataFrame): Segundo DataFrame

    Returns:
    pd.DataFrame: DataFrame com as diferenças
    """
    a_df_aligned, b_df_aligned = align_dataframes(a_df, b_df)
    difs_df = a_df_aligned.compare(b_df_aligned, align_axis=1)
    return difs_df

# Tratar as planilhas das IES e do Censo
paths = ['d:/Trab/INEP/Microdados/Ies/', 'd:/Trab/INEP/Microdados/Censo/']
tp_arqs = ['ies', 'censo']
fm_arqs = ['CSV', 'CSV']
dicionario = 'd:/Trab/INEP/Microdados/Dicionario/'
idx = 0
# Pegar cada tipo de arquivo e gerar o dicionário de dados de cada arquivo
for path in paths:
    tp_arq = tp_arqs[idx]
    # Definir o caminho da pasta
    folder_path = path
    formato = fm_arqs[idx]
    # Listar todos os arquivos na pasta
    files_in_directory = os.listdir(folder_path)
    # Filtrar apenas os arquivos com extensão .xlsx
    csv_files = [file for file in files_in_directory if file.endswith(formato)]
    # Lê todos os arquivos do formato
    for file in csv_files:
        compl = ''
        if tp_arq == 'ies':
            ano = file[4:8]
        else:
            ano = file[6:10]
            tam = len(file)
            if tam > 14:
                compl = file[10:]
                compl = compl.rsplit('.', 1)[0]
                x = ''
        if int(ano) < 2009:
            separador = '|'
        else:
            separador = ';'
        # Caminho do arquivo de entrada e saída
        input_file = folder_path + file
        output_file = dicionario +  'dic_' + tp_arq + '_' + ano + compl +'.xlsx'
        encode = 'ISO-8859-1'
       # Chamar a função para criar a planilha resumida
        create_summary_spreadsheet(input_file, output_file, formato, separador, encode)
    idx = idx + 1
# Tratar os censos de 2000 a 2008 que estão em arquivos separados. Juntar para posterior comparação
anos = range(2000, 2008 + 1)
arqs = ['_FORME_DISTANCIA', '_FORME_PRESENCIAL', '_GRADUACAO_DISTANCIA', '_GRADUACAO_PRESENCIAL', '_SECOMPLE_DISTANCIA', '_SECOMPLE_PRESENCIAL']
# Percorre os 9 anos
for ano in anos:
    # Monta o nome do arquivo destino
    arq_destino = dicionario + 'dic_censo_' + str(ano) + '.xlsx'
    # Inicializar um dataframe para o resultado
    trab_df = []
    # Percorre cada um dos arquivos do ano
    for arq in arqs:
        # Monta o nome do arquivo origem
        arq_origem = dicionario + 'dic_censo_' + str(ano) + arq + '.xlsx'
        # Le os arquivos
        # testar se o arquivo existe
        if os.path.exists(arq_origem):
            df = pd.read_excel(arq_origem)
            # Adiciona os dados nas listas
            trab_df.append(df)
    # Concatenar os dataframes
    soma_df = pd.concat(trab_df)
    # Remove linhas duplicadas
    novo_df = soma_df.drop_duplicates()
    # Salvar o resultado no arquivo destino
    novo_df.to_excel(arq_destino)
#
# Tratar as diferenças de ano para ano
# Tratar a diferença dos dicionários de IES
anos = range(1995, 2021 + 1)
tp_dics = ['dic_ies', 'dic_censo']
dicionario = 'd:/Trab/INEP/Microdados/Dicionario/'
# Faz um loop para cada tipo de dicionário
for tp_dic in tp_dics:
    arq_destino = dicionario + tp_dic + '.xlsx'
    dif_global = []
    # Percorre os anos que tem dicionário
    for ano in anos:
        # Seta o arquivo a
        ano_a = str(ano)
        arq_a = dicionario + tp_dic + '_' + ano_a + '.xlsx'
        # recupera o dataframe a
        a_df = pd.read_excel(arq_a)
        # Seta o arquivo b
        ano_b = str(ano + 1)
        arq_b = dicionario + tp_dic + '_' + ano_b + '.xlsx'
        # recupera o dataframe b
        b_df = pd.read_excel(arq_b)
        # Compara os 2 dataframes e calcula o que mudou
        dif_df = compare_dataframes(a_df, b_df)
        # Marcar quais foram os anos comparados no dataframe de diferenças
        refer = f'Dif_{ano_a}-{ano_b}'
        dif_df.insert(0, 'referencia', refer)
        # Adiciona os diferenças no dataframe global das diferenças
        dif_global.append(dif_df)
        msg = f'Conferido a diferença dos arquivos de {tp_dic} de {refer}'
        logger('I', msg)
    # Salvar o resultado das diferenças na planilha
    dif_global_df = pd.concat(dif_global, ignore_index=True)
    dif_global_df.to_excel(arq_destino)

# Recuperar o que é cada uma das variáveis dos pdfs

# montar um banco de dados de IES

# Montar um banco de dados dos cursos