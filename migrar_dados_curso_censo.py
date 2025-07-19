from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inep_models import Curso_censo as CursoCensoSQLite  # Importe com um nome diferente
from observa_models import Curso_censo as CursoCensoPostgres
from sqlalchemy.exc import IntegrityError

# Configurações de conexão
sqlite_url = 'sqlite:///INEP.db'
postgres_url = 'postgresql://postgres:Sem2Senha@localhost:5433/observa_edubr'


def migrar_curso_censo_em_lotes(tamanho_lote=5000):
    """
    Migra dados da tabela ies_censo do SQLite para o PostgreSQL em lotes.

    :param tamanho_lote: Número de registros para processar por vez.
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

        # Consulta em lotes
        offset = 0
        while True:
            # Consulta um lote de registros
            registros_lote = sqlite_session.query(CursoCensoSQLite).offset(offset).limit(tamanho_lote).all()

            if not registros_lote:
                break  # Sai do loop quando não houver mais registros

            for registro_sqlite in registros_lote:
                # Filtra os atributos para remover _sa_instance_state
                dados_registro = {coluna.name: getattr(registro_sqlite, coluna.name) for coluna in
                                  registro_sqlite.__table__.columns}

                # Cria um novo registro para o PostgreSQL com os dados filtrados
                registro_postgres = CursoCensoPostgres(**dados_registro)

                # Adiciona o novo registro à sessão do PostgreSQL
                postgres_session.add(registro_postgres)

            # Faz o commit dos dados no PostgreSQL para cada lote
            try:
                postgres_session.commit()
                print(f"Lote migrado com sucesso a partir do offset {offset}!")
            except IntegrityError as e:
                print(f"Erro de integridade no lote a partir do offset {offset}: {e}")
                postgres_session.rollback()

            # Atualiza o offset
            offset += tamanho_lote

    except Exception as e:
        print(f"Erro durante a migração: {e}")
        postgres_session.rollback()
    finally:
        # Fecha as sessões
        sqlite_session.close()
        postgres_session.close()


# Chama a função para iniciar a migração
migrar_curso_censo_em_lotes()