from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd

# Supondo que você já tenha seu engine configurado
# engine = create_engine('sua_string_de_conexao')
Session = sessionmaker(bind=engine)
session = Session()

# Exemplo de DataFrame
data = {
    'pop_19a24anos': [1702.0, 424.0, 1515.0],
    'municipio': [5200050, 3100104, 5200100],
    'ano_censo': [2022, 2022, 2022]
}

df = pd.DataFrame(data)

# Iterar sobre o DataFrame e atualizar os registros
for index, row in df.iterrows():
    # Filtrar o objeto MunicipioCenso correspondente
    municipio_censo = session.query(MunicipioCenso).filter_by(
        municipio=row['municipio'],
        ano_censo=row['ano_censo']
    ).first()

    # Se o registro existir, atualize a coluna pop_19a24anos
    if municipio_censo:
        municipio_censo.pop_19a24anos = row['pop_19a24anos']

# Commit as alterações no banco de dados
session.commit()

# Fechar a sessão
session.close()