from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Regiao(Base):
    __tablename__ = 'regiao'
    codigo = Column(Integer, primary_key=True)
    nome = Column(String(12), nullable=False)

class Uf(Base):
    __tablename__ = 'uf'
    sigla = Column(String(2), primary_key=True)
    nome = Column(String(40), nullable=False)
    regiao = Column(Integer, ForeignKey('regiao.codigo'), nullable=False)
    codigo = Column(Integer, nullable=False)

class Mesorregiao(Base):
    __tablename__ = 'mesorregiao'
    codigo = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False)
    estado = Column(String(2), ForeignKey('uf.sigla'), nullable=False)

class Microrregiao(Base):
    __tablename__ = 'microrregiao'
    codigo = Column(Integer, primary_key=True)
    nome = Column(String(60), nullable=False)
    mesorregiao = Column(Integer, ForeignKey('mesorregiao.codigo'), nullable=False)

class Municipio(Base):
    __tablename__ = 'municipio'
    codigo = Column(String(12), primary_key=True)
    nome = Column(String(100), nullable=False)
    capital = Column(Boolean)
    estado = Column(String(2), ForeignKey('uf.sigla'), nullable=False)
    mesoregiao = Column(Integer, ForeignKey('mesorregiao.codigo'), nullable=False)
    microregiao = Column(Integer, ForeignKey('microrregiao.codigo'), nullable=False)

# Configurar a engine e criar a sessão
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///INEP_testePK.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Exemplo de inserção de dados na tabela Municipio
uf_instance = Uf(sigla='SP', nome='São Paulo', regiao=1, codigo=35)
session.add(uf_instance)
session.commit()

mesorregiao_instance = Mesorregiao(codigo=1, nome='Mesorregião A', estado='SP')
session.add(mesorregiao_instance)
session.commit()

microrregiao_instance = Microrregiao(codigo=1, nome='Microrregião A', mesorregiao=1)
session.add(microrregiao_instance)
session.commit()

municipio_instance = Municipio(codigo='1', nome='Municipio A', capital=True, estado='SP', mesoregiao=1, microregiao=1)
session.add(municipio_instance)
session.commit()
