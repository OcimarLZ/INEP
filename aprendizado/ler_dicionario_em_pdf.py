import pdfplumber
import pandas as pd

def extract_table_from_pdf(file_path, start_page, end_page):
    all_data = []  # Lista para armazenar DataFrames das tabelas extraídas

    with pdfplumber.open(file_path) as pdf:
        for i in range(start_page, end_page + 1):
            page = pdf.pages[i]
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    if len(table) > 1:  # Verificar se há dados além do cabeçalho
                        df = pd.DataFrame(table[1:], columns=table[0])
                        # Verifica colunas duplicadas e remove
                        if not df.columns.is_unique:
                            print(f"Colunas duplicadas detectadas na página {i}, removendo duplicatas.")
                            df = df.loc[:, ~df.columns.duplicated()]
                        all_data.append(df)
                    else:
                        print(f"Tabela na página {i} está vazia ou malformada.")
            else:
                print(f"Nenhuma tabela encontrada na página {i}")

    if all_data:  # Apenas tenta concatenar se a lista não estiver vazia
        try:
            # Usa o primeiro DataFrame para padronizar colunas
            base_columns = all_data[0].columns
            standardized_data = [df.reindex(columns=base_columns, fill_value=None) for df in all_data]
            complete_data = pd.concat(standardized_data, ignore_index=True)
        except ValueError as e:
            print("Erro ao concatenar DataFrames:", e)
            complete_data = pd.DataFrame()
    else:
        print("Nenhuma tabela válida encontrada para concatenar.")
        complete_data = pd.DataFrame()

    return complete_data

def compare_years(dfs):
    """
    Compara a presença dos códigos em diferentes anos.

    :param dfs: Lista de DataFrames para comparar.
    :return: DataFrame com a presença dos códigos por ano.
    """
    # Combine todos os DataFrames em um único com um indicador de ano
    combined_df = pd.concat(dfs, keys=range(len(dfs)), names=['Year'])
    # Verifique a presença de cada código em cada ano
    presence = combined_df.groupby('Code').apply(lambda x: x['Year'].unique())

    return presence

# Exemplo de uso
# Para cada PDF, especifique as páginas de interesse
# list_of_dfs = [
#     extract_data_from_pdf(f'caminho/para/arquivo{i}.pdf', start_page=10, end_page=20)
#     for i in range(1, 16)
# ]
# presence = compare_years(list_of_dfs)
# print(presence)
# Exemplo de uso
df = extract_table_from_pdf('D:/Trab/INEP/Pdfs/Censo_2008.pdf', 53, 54)
x = ''