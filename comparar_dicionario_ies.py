import pandas as pd

# Caminho dos arquivos dos dicionarios das ies
file_2009 = 'd:/Trab/INEP/Microdados/dicionario/dicionário_ies_2009.xlsx'
file_2019 = 'd:/Trab/INEP/Microdados/dicionario/dicionário_ies_2019.xlsx'
file_2020 = 'd:/Trab/INEP/Microdados/dicionario/dicionário_ies_2020.xlsx'
file_2021 = 'd:/Trab/INEP/Microdados/dicionario/dicionário_ies_2021.xlsx'
file_2022 = 'd:/Trab/INEP/Microdados/dicionario/dicionário_ies_2022.xlsx'

# Carregar os arquivos em DataFrames
df_2009 = pd.read_excel(file_2009)
df_2019 = pd.read_excel(file_2019)
df_2020 = pd.read_excel(file_2020)
df_2021 = pd.read_excel(file_2021)
df_2022 = pd.read_excel(file_2022)

# Função para comparar dataframes
def compare_dataframes(df1, df2):
    comparison_df = df1.compare(df2, align_axis=0)
    return comparison_df

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