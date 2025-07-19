from observa_models import db
from sqlalchemy import create_engine

# Cria a engine do SQLite
engine = create_engine('postgresql+psycopg2://postgres:Sem2Senha@localhost:5433/observa_edubr')
db.metadata.create_all(engine)



