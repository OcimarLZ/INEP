from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from tqdm import tqdm  # Biblioteca para a barra de progresso

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

# Definir a tabela alvo (ajuste conforme necessário)
table_name = 'curso_censo'
table_inep = Table(table_name, metadata_inep, autoload_with=engine_inep)
table_inep2 = Table(table_name, metadata_inep2, autoload_with=engine_inep2)

# Iniciar as sessões
session_inep = SessionInep()
session_inep2 = SessionInep2()


# Identificar registros exclusivos
def obter_registros_unicos():
    registros_inep = session_inep.query(table_inep).all()
    registros_inep_data = {tuple(row[1:]) for row in registros_inep}  # Ignora o campo ID

    registros_inep2 = session_inep2.query(table_inep2).all()

    registros_unicos = []
    for row in tqdm(registros_inep2, desc="Verificando registros exclusivos", unit=" registros"):
        if tuple(row[1:]) not in registros_inep_data:
            registros_unicos.append(row)
    return registros_unicos


# Obter registros exclusivos com progresso
registros_unicos = obter_registros_unicos()

# Inserir registros exclusivos no INEP.db com uma barra de progresso
for registro in tqdm(registros_unicos, desc="Inserindo registros exclusivos", unit=" registros"):
    novo_registro = {col.name: getattr(registro, col.name) for col in table_inep2.columns if col.name != 'id'}
    session_inep.execute(table_inep.insert().values(**novo_registro))

# Commit para salvar as inserções
session_inep.commit()

# Fechar as sessões
session_inep.close()
session_inep2.close()
