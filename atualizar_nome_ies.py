from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from inep_models import Ies, Municipio  # Certifique-se de ajustar o nome do módulo

# Configurando a conexão com o banco de dados
database_url = 'sqlite:///INEP.db'  # Substitua pela URL correta do seu banco de dados
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Atualizando os registros
try:
    # Obtenha os registros que precisam ser atualizados
    registros_para_atualizar = (
        session.query(Ies)
        .join(Municipio, Ies.municipio == Municipio.codigo)
        .filter(Ies.nome.like('%codigo:%'))
        .all()
    )

    for registro in registros_para_atualizar:
        municipio_nome = (
            session.query(Municipio.nome)
            .filter(Municipio.codigo == registro.municipio)
            .scalar()
        )
        if municipio_nome:
            novo_nome = f"Instituição inativa da cidade de {municipio_nome}"
            registro.nome = novo_nome

    # Commit das mudanças
    session.commit()
    print("Atualização concluída com sucesso!")

except Exception as e:
    print(f"Erro durante a atualização: {e}")
    session.rollback()
finally:
    session.close()