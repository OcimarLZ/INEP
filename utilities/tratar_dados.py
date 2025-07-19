import numpy as np
import pandas as pd

def recria_e_reindexa_dataframe(df, ultimo_id):
    """
    Recria e reindexa o DataFrame a partir do último ID fornecido.

    :param df: DataFrame original que será reindexado
    :param ultimo_id: Último ID existente no banco de dados
    :return: DataFrame recriado com IDs reindexados
    """
    # Certifique-se de que ultimo_id é um inteiro
    if isinstance(ultimo_id, (tuple, list, pd.Series)):
        # Se for um Row ou similar, extraia o primeiro valor
        ultimo_id = ultimo_id[0]

    # Criar uma cópia do DataFrame para evitar alterações no original
    df_reindexed = df.copy()

    # Gerar novos IDs começando de 'ultimo_id + 1'
    novo_id = range(int(ultimo_id) + 1, int(ultimo_id) + 1 + len(df_reindexed))

    # Atribuir os novos IDs à coluna 'id'
    df_reindexed['id'] = novo_id

    return df_reindexed


def soma_intervalo(colunas_serie, col_inicio, col_fim, paridade='ambas'):
    """
    Soma os valores das colunas dentro de um intervalo definido, com base na paridade:
    - 'par': soma apenas colunas de índice par
    - 'impar': soma apenas colunas de índice ímpar
    - 'ambas': soma todas as colunas no intervalo

    Parameters:
    - colunas_serie: Serie de colunas de um dataframe
    - col_inicio: Nome da primeira coluna no intervalo
    - col_fim: Nome da última coluna no intervalo
    - paridade: 'par', 'impar' ou 'ambas'. Default é 'ambas'.

    Returns:
    - Uma série com a soma ao longo das linhas das colunas selecionadas.
    """
    # Selecionar o intervalo de colunas
    colunas_intervalo = colunas_serie.loc[col_inicio:col_fim]

    # Selecionar os valores com base na paridade
    if paridade == 'par':
        colunas_selecionadas = colunas_intervalo.iloc[::2]  # Índices pares
    elif paridade == 'impar':
        colunas_selecionadas = colunas_intervalo.iloc[1::2]  # Índices ímpares
    elif paridade == 'ambas':
        colunas_selecionadas = colunas_intervalo  # Todos os valores
    elif paridade == 'de2em2':
        colunas_selecionadas = pd.concat([colunas_intervalo.iloc[i:i + 2] for i in range(0, len(colunas_intervalo), 4)])
    else:
        raise ValueError("Paridade deve ser 'par', 'impar', 'ambas' ou 'de2em2'.")

    if len(colunas_selecionadas) > 0:
        return colunas_selecionadas.sum()
    else:
        return 0

def trata_intervalo(colunas_serie, col_inicio, col_fim, operacao):
    """
    Verifica se um intervalo de um DataFrame contém pelo menos um 'S'.

    :param df: O DataFrame a ser analisado.
    :param lin_inicio: Índice da linha inicial do intervalo.
    :param lin_fim: Índice da linha final do intervalo (incluído).
    :param col_inicio: Índice da coluna inicial do intervalo.
    :param col_fim: Índice da coluna final do intervalo (incluído).
    :return: 'S' se qualquer célula no intervalo contiver 'S', caso contrário 'N'.
    """
    # Seleciona o intervalo do DataFrame
    colunas = colunas_serie.loc[col_inicio:col_fim]
    # Verifica a operação
    if operacao == 'S':
        # Verifica se existe pelo menos um 'S' no intervalo
        if (colunas == 'S').any().any():
            return True
        else:
            return False
    elif operacao == '+':
        # Retornar a soma ao longo do eixo 1 (ao longo das linhas)
        return colunas.sum()
    else:
        return 0


def trata_lista(colunas_serie, lista_cols, operacao):
    """
    Seleciona um conjunto de colunas especificadas em `lista_colunas` do DataFrame `df`
    e verifica se pelo menos um valor é igual a 'S'.

    Parameters:
    - df: DataFrame do Pandas
    - lista_colunas: Lista de colunas específicas para análise
    - operacao

    Returns:
    - se operacao = "S"
          - 'S' se pelo menos um valor for 'S' no subconjunto das colunas
          - 'N' caso contrário
    - se operacao = '+'
        - SOMA Das colunaas
    """
    # Seleciona o intervalo do DataFrame
    colunas = colunas_serie[lista_cols]
    # Verifica a operação
    if operacao == 'S':
        # Verifica se existe pelo menos um 'S' no intervalo
        if (colunas == 'S').any().any():
            return True
        else:
            return False
    elif operacao == '+':
        # Retornar a soma ao longo do eixo 1 (ao longo das linhas)
        return colunas.sum()
    else:
        return 0

def seta_zero_colunas_com_nan(df):
    # Itera sobre todas as colunas do DataFrame
    for column in df.columns:
        # Verifica se a coluna é do tipo float, integer ou boolean
        if np.issubdtype(df[column].dtype, np.number) or df[column].dtype == bool:
            # Substitui NaN por 0 na coluna
            df[column] = df[column].fillna(0)
    return df

def trata_localizacao_nula(nul_df, coluna, ies_df, coluna_ies, metodo):
    # Criar um dicionário para armazenar os índices gerados para cada 'NO_CINE_ROTULO' único
    cine_rotulo_map = {}
    # Atribuir o índice do DataFrame à coluna 'codigo' onde o valor original é nulo
    print(f'Tratando os Dados...Refazendo da coluna {coluna } com valores em branco')
    # Iterar sobre o DataFrame e preencher 'CO_CINE_ROTULO' com índices gerados onde o valor original é nulo
    for idx, row in nul_df.iterrows():
        if pd.isnull(row[coluna]):
            ies = row['CO_IES']
            # Recupera os valores da ies associada
            matching_rows = ies_df[(ies_df['codigo'] == ies)]
            if not matching_rows.empty:
                valor = matching_rows.iloc[0][coluna_ies]
                # Atribuir o mesmo código encontrado
                if metodo == 'S':
                    nul_df.at[idx, coluna] = valor
                elif metodo == 'C':
                    if coluna == 'TP_REDE':
                        if valor < 4:
                            nul_df.at[idx, coluna] = 1
                        else:
                            nul_df.at[idx, coluna] = 2
                    if coluna == 'IN_GRATUITO':
                        if valor < 4:
                            nul_df.at[idx, coluna] = 0
                        else:
                            nul_df.at[idx, coluna] = 1
                    if coluna == 'TP_GRAU_ACADEMICO':
                        nul_df.at[idx, coluna] = 0
    return nul_df
