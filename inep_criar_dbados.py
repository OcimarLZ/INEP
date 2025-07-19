from inep_models import db
from sqlalchemy import create_engine

# Cria a engine do SQLite
engine = create_engine('sqlite:///INEP.db')
db.metadata.create_all(engine)

