from sqlalchemy import create_engine, MetaData, Table, select, update, insert
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm

# Conectar aos bancos de dados
engine_inep = create_engine('sqlite:///INEP.db')
engine_inep2 = create_engine('sqlite:///INEP2.db')
SessionInep = sessionmaker(bind=engine_inep)
SessionInep2 = sessionmaker(bind=engine_inep2)

# Obter metadata de ambos os bancos
metadata_inep = MetaData()
metadata_inep2 = MetaData()
metadata_inep.reflect(bind=engine_inep)
metadata_inep2.reflect(bind=engine_inep2)

# Definir a tabela alvo e as colunas para comparação
table_name = 'curso'
table_inep = Table(table_name, metadata_inep, autoload_with=engine_inep)
table_inep2 = Table(table_name, metadata_inep2, autoload_with=engine_inep2)

colunas_chave = ['codigo']  # Colunas-chave para comparação

# Iniciar as sessões
session_inep = SessionInep()
session_inep2 = SessionInep2()


# Função para verificar se o registro já existe e comparar colunas específicas
def obter_registros_unicos_e_atualizar():
    registros_inep2 = session_inep2.query(table_inep2).all()

    for registro in tqdm(registros_inep2, desc="Processando registros", unit=" registros"):
        filtro = {col: getattr(registro, col) for col in colunas_chave}

        registro_inep = session_inep.execute(select(table_inep).filter_by(**filtro)).first()

        if registro_inep:
            # Realiza o update apenas nas colunas que podem ter mudado
            novos_valores = {
                col.name: getattr(registro, col.name)
                for col in table_inep.columns if col.name not in colunas_chave
            }
            session_inep.execute(update(table_inep).filter_by(**filtro).values(**novos_valores))
        else:
            # Insere o novo registro se não existir
            novo_registro = {col.name: getattr(registro, col.name) for col in table_inep.columns}
            session_inep.execute(insert(table_inep).values(**novo_registro))


# Processar e aplicar as alterações
obter_registros_unicos_e_atualizar()

# Commit para salvar as mudanças no banco de dados
session_inep.commit()

# Fechar as sessões
session_inep.close()
session_inep2.close()
