from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inep_models import Ies_censo as IesCensoSQLite  # Importe com um nome diferente
from observa_models import Ies_censo as IesCensoPostgres
from sqlalchemy.exc import IntegrityError

# Configurações de conexão
sqlite_url = 'sqlite:///INEP.db'
postgres_url = 'postgresql://postgres:Sem2Senha@localhost:5433/observa_edubr'

def migrar_ies_censo():
    """
    Migra dados da tabela ies_censo do SQLite para o PostgreSQL.
    """
    try:
        # Cria os mecanismos de conexão
        sqlite_engine = create_engine(sqlite_url)
        postgres_engine = create_engine(postgres_url)

        # Cria as sessões
        SQLite_Session = sessionmaker(bind=sqlite_engine)
        Postgres_Session = sessionmaker(bind=postgres_engine)

        sqlite_session = SQLite_Session()
        postgres_session = Postgres_Session()

        # Consulta todos os registros da tabela ies_censo no SQLite
        ies_censo_sqlite = sqlite_session.query(IesCensoSQLite).all()

        for registro_sqlite in ies_censo_sqlite:
            # Filtra os atributos para remover _sa_instance_state
            dados_registro = {coluna.name: getattr(registro_sqlite, coluna.name) for coluna in
                              registro_sqlite.__table__.columns}

            # Cria um novo registro para o PostgreSQL com os dados filtrados
            registro_postgres = IesCensoPostgres(**dados_registro)

            # Adiciona o novo registro à sessão do PostgreSQL
            postgres_session.add(registro_postgres)

        # Faz o commit dos dados no PostgreSQL
        postgres_session.commit()
        print("Migração concluída com sucesso!")

    except IntegrityError as e:
        print(f"Erro de integridade: {e}")
        postgres_session.rollback()  # Desfaz as alterações em caso de erro
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        postgres_session.rollback()  # Desfaz as alterações em caso de erro
    finally:
        # Fecha as sessões
        sqlite_session.close()
        postgres_session.close()


# Chama a função para iniciar a migração
migrar_ies_censo()
