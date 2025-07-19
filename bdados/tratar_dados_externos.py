import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, relationship
from inep_models import db, Ies
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def salvar_bdados(db_df, Model, chave):
    # Obter o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Subir um nível na hierarquia de diretórios
    parent_dir = os.path.dirname(script_dir)
    # Construir o caminho absoluto para o arquivo do banco de dados
    db_path = os.path.join(parent_dir, 'INEP.db')
    # Criar a URL do banco de dados com o caminho absoluto
    db_url = f'sqlite:///{db_path}'

    logger.info(f"Conectando ao banco de dados: {db_url}")
    engine = create_engine(db_url)

    # Verificar se a tabela existe
    inspector = inspect(engine)
    if not inspector.has_table(Model.__tablename__):
        logger.info(f"Criando a tabela {Model.__tablename__}")
        Model.__table__.create(engine)
    else:
        logger.info(f"A tabela {Model.__tablename__} já existe")

    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # Iterar sobre cada registro do DataFrame e fazer upsert
        for record in db_df.to_dict(orient="records"):
            instance = session.query(Model).filter_by(**{chave: record[chave]}).first()
            if instance:
                # Atualizar o registro existente
                for key, value in record.items():
                    setattr(instance, key, value)
            else:
                # Adicionar um novo registro
                instance = Model(**record)
                session.add(instance)

        session.commit()
        logger.info(f"Dados salvos com sucesso na tabela {Model.__tablename__}")
    except Exception as e:
        session.rollback()
        logger.error(f"Erro ao salvar dados: {str(e)}")
        raise e
    finally:
        session.close()

def ler_ies():
    # Configure your SQLite database connection
    DATABASE_URI = 'sqlite:///INEP.db'
    # Create the SQLAlchemy engine
    engine = create_engine(DATABASE_URI)
    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)
    # Create a Session
    session = Session()
    # Query the Ies table
    ies_data = session.query(Ies).all()
    # Convert the query result to a pandas DataFrame
    # Assuming Ies is a SQLAlchemy declarative base model with columns matching your table
    ies_df = pd.DataFrame([s.__dict__ for s in ies_data])
    # Drop the SQLAlchemy internal columns like _sa_instance_state
    ies_df = ies_df.drop('_sa_instance_state', axis=1, errors='ignore')
    # Close the session
    session.close()
    return ies_df

def ultimo_id(Model):
    # Obter o diretório do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Subir um nível na hierarquia de diretórios
    parent_dir = os.path.dirname(script_dir)
    # Construir o caminho absoluto para o arquivo do banco de dados
    db_path = os.path.join(parent_dir, 'INEP.db')
    # Criar a URL do banco de dados com o caminho absoluto
    db_url = f'sqlite:///{db_path}'

    logger.info(f"Conectando ao banco de dados: {db_url}")
    engine = create_engine(db_url)
    # Verificar se a tabela existe
    inspector = inspect(engine)

    if not inspector.has_table(Model.__tablename__):
        logger.info(f"Criando a tabela {Model.__tablename__}")
        Model.__table__.create(engine)
    else:
        logger.info(f"A tabela {Model.__tablename__} já existe")

    Session = sessionmaker(bind=engine)
    session = Session()

    max_id = session.query(Model.id).order_by(Model.id.desc()).first()
    return max_id
