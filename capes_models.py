from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Uf(db.Model):
    __tablename__ = 'uf'
    sigla = db.Column(db.String(2), primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    regiao = db.Column(db.Integer, db.ForeignKey('regiao.codigo'), nullable=False)
    codigo = db.Column(db.Integer(), nullable=False)

class Regiao(db.Model):
    __tablename__ = 'regiao'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(12), nullable=False)

class Municipio(db.Model):
    __tablename__ = 'municipio'
    codigo = db.Column(db.String(12), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capital = db.Boolean()

class GrandeArea(db.Model):
    __tablename__ = 'area'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class AreaConhecimento(db.Model):
    __tablename__ = 'area_conhecimento'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    area = db.Column(db.Integer, db.ForeignKey('area.codigo'), nullable=False)

class AreaAvaliacao(db.Model):
    __tablename__ = 'area_avaliacao'
    codigo = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

class Programa(db.Model):
    __tablename__ = 'programa'
    codigo = db.Column(db.String(15), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class ProgramaFomento(db.Model):
    __tablename__ = 'programa_fomento'
    codigo = db.Column(db.String(15), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class TpNivelAcademico(db.Model):
    __tablename__ = 'tp_nivel_academico'
    codigo = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

class TpStatusJuridico(db.Model):
    __tablename__ = 'tp_status_juridico'
    codigo = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

class Ies(db.Model):
    __tablename__ = 'ies'
    codigo = db.Column(db.Integer(), primary_key=True)
    sigla = db.Column(db.String(15), nullable=False)
    nome = db.Column(db.String(100), nullable=False)

class BolsaNacional(db.Model):
    __tablename__ = 'bolsa_nacional'
    id = db.Column(db.Integer, primary_key=True)
    ano_censo = db.Column(db.Integer, nullable=False)
    regiao = db.Column(db.String(13), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    municipio = db.Column(db.String(50), nullable=False)
    ies_codigo = db.Column(db.Integer, db.ForeignKey('ies.codigo'), nullable=True)
    programa_codigo = db.Column(db.String(15), db.ForeignKey('programa.codigo'), nullable=True)
    programa_fomento = db.Column(db.String(15), nullable=False)
    status_juridico = db.Column(db.Integer, db.ForeignKey('tp_status_juridico.codigo'), nullable=True)
    grande_area = db.Column(db.Integer, db.ForeignKey('area.codigo'), nullable=True)
    area_avaliacao = db.Column(db.Integer, db.ForeignKey('area_avaliacao.codigo'), nullable=True)
    area_conhecimento = db.Column(db.Integer, db.ForeignKey('area_conhecimento.codigo'), nullable=True)
    qt_coord_geral_isf = db.Column(db.Integer, nullable=True)
    qt_coord_pedag_isf = db.Column(db.Integer, nullable=True)
    qt_coord_centro_isf = db.Column(db.Integer, nullable=True)
    qt_doutorado_pleno = db.Column(db.Integer, nullable=True)
    qt_iniciacao_cientifica = db.Column(db.Integer, nullable=True)
    qt_mestrado = db.Column(db.Integer, nullable=True)
    qt_mestrado_prof = db.Column(db.Integer, nullable=True)
    qt_prof_visit_mestrado_senior = db.Column(db.Integer, nullable=True)
    qt_prof_isf = db.Column(db.Integer, nullable=True)
    qt_pos_doutorado = db.Column(db.Integer, nullable=True)
    qt_supervisao = db.Column(db.Integer, nullable=True)
    qt_total_linha = db.Column(db.Integer, nullable=True)

class BolsaNacionalPorPrograma(db.Model):
    __tablename__ = 'bolsa_nacional_por_programa'
    id = db.Column(db.Integer, primary_key=True)
    ano_censo = db.Column(db.Integer, nullable=False)
    regiao = db.Column(db.String(13), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    municipio = db.Column(db.String(50), nullable=False)
    ies_codigo = db.Column(db.Integer, db.ForeignKey('ies.codigo'), nullable=True)
    programa_codigo = db.Column(db.String(15), db.ForeignKey('programa.codigo'), nullable=True)
    programa_fomento = db.Column(db.String(15), nullable=False)
    status_juridico = db.Column(db.Integer, db.ForeignKey('tp_status_juridico.codigo'), nullable=True)
    grande_area = db.Column(db.Integer, db.ForeignKey('area.codigo'), nullable=True)
    area_avaliacao = db.Column(db.Integer, db.ForeignKey('area_avaliacao.codigo'), nullable=True)
    area_conhecimento = db.Column(db.Integer, db.ForeignKey('area_conhecimento.codigo'), nullable=True)
    qt_doutorado_pleno = db.Column(db.Integer, nullable=True)
    qt_mestrado = db.Column(db.Integer, nullable=True)
    qt_prof_visitante = db.Column(db.Integer, nullable=True)
    qt_pos_doutorado = db.Column(db.Integer, nullable=True)
    qt_total_linha = db.Column(db.Integer, nullable=True)

