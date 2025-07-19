from sqlalchemy import create_engine
import pandas as pd

# Configurações de conexão
sqlite_url = 'sqlite:///INEP.db'  # Caminho do banco de dados SQLite
postgres_url = 'postgresql://postgres:Sem2Senha@localhost:5433/observa_edubr'  # Altere com os dados do seu PostgreSQL

# Conexões
engine_sqlite = create_engine(sqlite_url)
engine_postgres = create_engine(postgres_url)

# Lista das tabelas em ordem de dependência para a migração
tablesx = [
    ("comum.regiao", "regiao"),
    ("comum.uf", "uf"),
    ("comum.mesorregiao", "mesorregiao"),
    ("comum.microrregiao", "microrregiao"),
    ("comum.municipio", "municipio"),
    ("graduacao.area", "area"),
    ("graduacao.area_especifica", "area_especifica"),
    ("graduacao.area_detalhada", "area_detalhada"),
    ("graduacao.curso", "curso"),
    ("graduacao.cine_rotulo", "cine_rotulo"),
    ("graduacao.tp_dimensao", "tp_dimensao"),
    ("graduacao.tp_nivel_academico", "tp_nivel_academico"),
    ("graduacao.tp_modal_ensino", "tp_modal_ensino"),
    ("graduacao.tp_organizacao_academica", "tp_organizacao_academica"),
    ("graduacao.tp_categoria_administrativa", "tp_categoria_administrativa"),
    ("graduacao.tp_rede", "tp_rede"),
    ("graduacao.tp_grau_academico", "tp_grau_academico"),
    ("graduacao.tp_modalidade_ensino", "tp_modalidade_ensino"),
    ("graduacao.mantenedora", "mantenedora"),
    ("graduacao.ies", "ies"),
    ("graduacao.ies_censo", "ies_censo"),
    ("graduacao.curso_censo", "curso_censo"),
    ("graduacao.censo_es", "censo_es")
]
tables = [
    ("graduacao.ies_censo", "ies_censo"),
    ("graduacao.curso_censo", "curso_censo"),
    ("graduacao.censo_es", "censo_es")
]

def decode_bytes(value):
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            # Tenta com latin1 caso utf-8 falhe
            return value.decode('latin1')
    return value

# Função para migrar dados de cada tabela
def migrate_table(schema_table, table):
    # Conectando ao banco SQLite
    query = f"SELECT * FROM {table}  limit 10"
    df = pd.read_sql(query, engine_sqlite)

    if df.empty:
        print(f"Não há dados na tabela {table} para migrar.")
        return

        # Decodificar colunas de bytes para string
    for column in df.columns:
        if isinstance(df[column].iloc[0], bytes):  # Checa o primeiro valor da coluna
            df[column] = df[column].apply(decode_bytes)

    # Conversão de 0 e 1 para False e True
    if 'in_acesso_portal_capes' in df.columns:
        df['in_acesso_portal_capes'] = df['in_acesso_portal_capes'].apply(lambda x: True if x == 1 else False)
    if 'in_acesso_outras_bases' in df.columns:
        df['in_acesso_outras_bases'] = df['in_acesso_outras_bases'].apply(lambda x: True if x == 1 else False)
    if 'in_assina_outra_base' in df.columns:
        df['in_assina_outra_base'] = df['in_assina_outra_base'].apply(lambda x: True if x == 1 else False)
    if 'in_repositorio_institucional' in df.columns:
        df['in_repositorio_institucional'] = df['in_repositorio_institucional'].apply(lambda x: True if x == 1 else False)
    if 'in_busca_integrada' in df.columns:
        df['in_busca_integrada'] = df['in_busca_integrada'].apply(lambda x: True if x == 1 else False)
    if 'in_servico_internet' in df.columns:
        df['in_servico_internet'] = df['in_servico_internet'].apply(lambda x: True if x == 1 else False)
    if 'in_participa_rede_social' in df.columns:
        df['in_participa_rede_social'] = df['in_participa_rede_social'].apply(lambda x: True if x == 1 else False)
    if 'in_catalogo_online' in df.columns:
        df['in_catalogo_online'] = df['in_catalogo_online'].apply(lambda x: True if x == 1 else False)
    # Remover o índice do DataFrame para evitar duplicações no PostgreSQL
    df.reset_index(drop=True, inplace=True)

    # Migração para PostgreSQL
    # Tenta gravar no PostgreSQL
    schema, tabela = schema_table.split('.')
    df.to_sql(tabela, engine_postgres, schema=schema, if_exists='append', index=False, method="multi", chunksize=1000)
    print(f"Dados migrados para a tabela {schema_table}")

# Migrar todas as tabelas
for schema_table, table in tables:
    print(f"Migrando {schema_table}...")
    schema, table = schema_table.split(".")
    migrate_table(schema_table, table)
    print(f"Conclusão da migração de {schema_table}.")
