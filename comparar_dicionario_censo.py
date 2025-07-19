import pandas as pd

def remove_ultimas_colunas(df):
    """
    Remove todas as colunas do DataFrame, exceto as quatro primeiras.
    Args:
    df (pd.DataFrame): DataFrame original
    Returns:
    pd.DataFrame: DataFrame com apenas as quatro primeiras colunas
    """
    return df.iloc[:, :4]
def align_dataframes(df1, df2):
    """
    Alinha dois DataFrames com base nos índices e preenche valores ausentes com NaN.

    Args:
    df1 (pd.DataFrame): Primeiro DataFrame
    df2 (pd.DataFrame): Segundo DataFrame

    Returns:
    tuple: Dois DataFrames alinhados
    """
    df1_aligned, df2_aligned = df1.align(df2, join='outer', axis=0, fill_value=pd.NA)
    return df1_aligned, df2_aligned

# Função para comparar dataframes
def compare_dataframes(df1, df2):
    """
    Compara dois DataFrames e retorna um DataFrame com as diferenças.

    Args:
    df1 (pd.DataFrame): Primeiro DataFrame
    df2 (pd.DataFrame): Segundo DataFrame

    Returns:
    pd.DataFrame: DataFrame com as diferenças
    """
    df1_aligned, df2_aligned = align_dataframes(df1, df2)
    comparison_df = df1_aligned.compare(df2_aligned, align_axis=0)
    return comparison_df

# Caminho dos arquivos dos dicionarios das ies
file_2009 = 'd:/Trab/INEP/Microdados/Dicionario/dicionário_2009.xlsx'
file_2019 = 'd:/Trab/INEP/Microdados/Dicionario/dicionário_2019.xlsx'
file_2020 = 'd:/Trab/INEP/Microdados/Dicionario/dicionário_2020.xlsx'
file_2021 = 'd:/Trab/INEP/Microdados/Dicionario/dicionário_2021.xlsx'
file_2022 = 'd:/Trab/INEP/Microdados/Dicionario/dicionário_2022.xlsx'

# Carregar os arquivos em DataFrames
df_2009 = pd.read_excel(file_2009, sheet_name='cadastro_cursos', skiprows=8)
df_2019 = pd.read_excel(file_2019, sheet_name='cadastro_cursos', skiprows=8)
df_2020 = pd.read_excel(file_2020, sheet_name='cadastro_cursos', skiprows=8)
df_2021 = pd.read_excel(file_2021, sheet_name='cadastro_cursos', skiprows=8)
df_2022 = pd.read_excel(file_2022, sheet_name='cadastro_cursos', skiprows=8)

# remove todas as colunas, exceto as 4 primeiras em cada dataframe
# Aplicar a função para manter apenas as quatro primeiras colunas
df_2009 = remove_ultimas_colunas(df_2009)
df_2019 = remove_ultimas_colunas(df_2019)
df_2020 = remove_ultimas_colunas(df_2020)
df_2021 = remove_ultimas_colunas(df_2021)
df_2022 = remove_ultimas_colunas(df_2022)

# Comparar os dataframes
diff_2009_2019 = compare_dataframes(df_2009, df_2019)
diff_2019_2020 = compare_dataframes(df_2019, df_2020)
diff_2020_2021 = compare_dataframes(df_2020, df_2021)
diff_2021_2022 = compare_dataframes(df_2021, df_2022)

# Exibir as diferenças
print("Diferenças entre 2009 e 2019")
print(diff_2009_2019)
print("\nDiferenças entre 2019 e 2020")
print(diff_2019_2020)
print("\nDiferenças entre 2020 e 2021")
print(diff_2020_2021)
print("\nDiferenças entre 2021 e 2022")
print(diff_2021_2022)
x = ''