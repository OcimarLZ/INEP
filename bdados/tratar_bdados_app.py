import shutil
import pandas as pd
import configparser
from sqlalchemy import create_engine


# função que recupera onde deve ser gravado os dados para carga no BI e cria a conexão (recebe qual módulo será utilizado)
def criar_conexao(modulo):
    # Recuperar config de acesso ao banco do arquivo .ini
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    # Recupera onde fica o destino dos dados do datamart
    sgdb = cfg.get(modulo, "SGDB")
    pasta_local = cfg.get(modulo,"PASTA_LOCAL")
    dbase = cfg.get(modulo,"DW")
    ecoar = cfg.get(modulo,"ECHO")
    salvarxls = cfg.get(modulo,"PLANILHA")
    if ecoar == 'S':
        ecoar = True
    else:
        ecoar = False
    engine = create_engine(sgdb + ':' + pasta_local + dbase, echo=ecoar)
    bd_bi_cnx = engine.connect()
    return bd_bi_cnx, salvarxls, dbase


# recebe os dados para salvar no datamart
def salvar_datamart(db_bi_cnx, dados_df, modulo, salvarxls, nome_table, d_type):
    if salvarxls == 'C':  # salvar os dados em CSV
        status = salvar_em_csv(dados_df, nome_table)
    elif salvarxls == 'X':  # salvar os dados em XLS
        status = salvar_em_xls(modulo, dados_df, nome_table)
    else:
        status = salvar_no_bi(dados_df, nome_table, db_bi_cnx, d_type)
    return status

# recebe o dataframe e salva na base de dados do BI
def salvar_no_bi(dados_df, nome_table, db_bi_cnx, d_type):
    # colocar as colunas do dataframe em lowercasa
    dados_df.columns = [col.lower() for col in dados_df.columns]
    # salvar o dataframe no banco de dados
    status = dados_df.to_sql(nome_table, db_bi_cnx, if_exists='replace', index=False, dtype=d_type)
    return status


# salvar em CSV
def salvar_em_csv(dados_df, nome_table):
    nomecsv = nome_table + '.csv'
    status = dados_df.to_csv(nomecsv, index=False)
    return status

# Salvar em XLS
def salvar_em_xls(modulo, dados_df, nome_table):
    nomexls = modulo[:-3] + '.xlsx'
    if nome_table == 'versaodb':
        with pd.ExcelWriter(nomexls, mode='w') as writer:
            status = dados_df.to_excel(writer, sheet_name=nome_table, index=False)
    else:
        with pd.ExcelWriter(nomexls, mode='a', if_sheet_exists="replace") as writer:
            status = dados_df.to_excel(writer, sheet_name=nome_table, index=False)
    return status

# copia a base do BI para o repositório
def copiar_para_repositorio(modulo):
    # Recuperar config de acesso ao banco do arquivo .ini
    cfg = configparser.ConfigParser()
    cfg.read('../config.ini')
    pasta_repositorio = cfg.get(modulo, "PASTA_REPOSITORIO")
    dbase = cfg.get(modulo,"DW")
    # arquivo = pasta_local + dbase
    arqlocal = '.\\' + dbase
    # move para a pasta destinho
    status = shutil.copy(arqlocal, pasta_repositorio)
    print(f'Movendo arquivo: {arqlocal} p/ {pasta_repositorio}')
    return status
