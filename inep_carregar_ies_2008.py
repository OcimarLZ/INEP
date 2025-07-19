import pandas as pd
from inep_models import Ies, Ies_censo
from bdados.tratar_dados_externos import salvar_bdados, ler_ies, ultimo_id
from bdados.ler_bdados_to_df import carregar_dataframe
from utilities.tratar_dados import recria_e_reindexa_dataframe, soma_intervalo, trata_intervalo, trata_lista

# Indicação de quais tabelas devem ser salvas no banco de dados (para tempo de desenvolvimento, nos testes)
tab_ies = 'N'
tab_censo = 'N'

org_acad = {
     4:3,
     6:4
}

de_para_cadies = {'ANO': 'ano_censo',
     'REGIAO': 'regiao',
     'SIGLA_UF': 'estado',
     'CODMUNIC': 'municipio',
     'CO_ORG': 'org_academica',
     'CO_DEP': 'categoria',
     'CO_REDE': 'tp_rede',
     'NOMEORG':'nome',
     'IES': 'codigo'
     }

encode = 'ISO-8859-1'
delimitador = '|'
# Definir o caminho da pasta
ano = 2008
file_patch = f'd:/Trab/INEP/Microdados/ies/IES_2008.csv'
# Carregar o arquivo CSV em um DataFrame, especificando o delimitador correto
df = pd.read_csv(file_patch, delimiter=delimitador, encoding=encode)

# Resetar o índice do DataFrame completo, concatenado com os df dos diversos anaos
df = df.reset_index(drop=True)
# Verificar se precisa cadastrar alguma IES
df_ies_atu = df[['IES']].drop_duplicates()
# lER E carregar o dataframe das IES para calcular o valores a serem trocados
df_ies = ler_ies()
#  Identificar quais registros de ies_nov_df['ies'] não estão em ies_df['codigo']
df_ies_nao_exist = df_ies_atu[~df_ies_atu['IES'].isin(df_ies['codigo'])]
# Filtrando as colunas ANO, IES, NOME, CIDADE, UF onde IES coincide entre A e B
# Pegar os dados do dataframe que precisam ser salvas na tabela IES
df_ies_dados = pd.merge(df_ies_nao_exist, df, on='IES', how='inner')[['IES', 'CO_ORG', 'NOMEORG', 'CO_REDE', 'CO_DEP', 'CATEGADM', 'CATADMPARTSE', 'CATADMCOMUN', 'CATADMCONFESS', 'CATADMFILANT', 'CODMUNIC', 'SIGLA_UF', 'NOMEDEP']]
# Renomear as colunas do DataFrame de acordo com o dicionário
df_ies_dados = df_ies_dados.rename(columns=de_para_cadies)
# Extraindo os 2 primeiros e os 5 últimos dígitos
df_ies_dados['municipio'] = df_ies_dados['municipio'].astype(str).apply(lambda x: x[:2] + x[-5:])
# Tratar o tipo de organização acadêmica
# Substituindo os valores com base no dicionário
df_ies_dados['org_academica'] = df_ies_dados['org_academica'].replace(org_acad)
# Atualizar a coluna 'org_academica' onde o valor na coluna 'nome' for igual a 'Centro de Educação Tecnológica'
df_ies_dados.loc[df_ies_dados['nome'] == 'Centro de Educação Tecnológica', 'org_academica'] = 5
df_ies_dados['categoria'] = 4
df_ies_dados.loc[df_ies_dados['NOMEDEP'] == 'Federal', 'categoria'] = 1
df_ies_dados.loc[df_ies_dados['NOMEDEP'] == 'Estadual', 'categoria'] = 2
df_ies_dados.loc[df_ies_dados['NOMEDEP'] == 'Municipal', 'categoria'] = 3
df_ies_dados.loc[df_ies_dados['NOMEDEP'] == 'Comun.Confes.Filant.', 'categoria'] = 5
df_ies_dados['nome'] = df_ies_dados['nome'] + ' codigo: ' + df_ies_dados['codigo'].astype(str)
df_ies_dados['sigla'] = '-'
df_ies_dados['endereco_logradouro'] = 'a definir'
df_ies_dados['endereco_numero'] = 's/n'
df_ies_dados['endereco_complemento'] = 'a definir'
df_ies_dados['bairro'] = 'a definir'
df_ies_dados['cep'] = 0
df_ies_dados['mantenedora'] = 0
# recupera a localização da IES
sql = "select m.codigo as municipio_codigo, u.regiao, m.mesorregiao, m.microrregiao from municipio m join uf u on u.sigla = m.estado"
df_aux = carregar_dataframe(sql)
# Unir os dados dos municípios ao dataframe original
df_ies_dados = df_ies_dados.merge(df_aux, how='left', left_on='municipio', right_on='municipio_codigo')
# Remover os campos não desejados
df_ies_dados.drop(columns={'CATEGADM','NOMEDEP', 'CATADMPARTSE', 'CATADMCOMUN', 'CATADMCONFESS', 'CATADMFILANT', 'municipio_codigo'}, inplace=True)
# Salva os dados da IES
if tab_ies == 'S':
     salvar_bdados(df_ies_dados, Ies, 'codigo')

# Substituir todos os valores NaN por zero
df.fillna(0, inplace=True)
ies_censo = []
# Iterar sobre cada linha do DataFrame
for _, row in df.iterrows():
   # Criar um dicionário para mapear campos do modelo para valores do DataFrame
   dados_ies = {
        'ano_censo': row['ANO'],  # Mapeamento direto para o ano do censo
        'regiao': row['REGIAO'],  # Mapeamento direto para a região
        'mesorregiao': 0,
        'microrregiao': 0,
        'estado': row['SIGLA_UF'],  # Mapeamento direto para o estado
        'municipio': str(row['CODMUNIC']),
        'org_academica': row['CO_ORG'],  # Mapeamento direto para a organização acadêmica
        'categoria': row['CATEGADM'],  # Mapeamento direto para a categoria administrativa
        'mantenedora': 0,
        'tp_rede': row['CO_REDE'],  # Mapeamento direto para o tipo de rede
        'ies': row['IES'],  # Mapeamento direto para a IES
        'qt_tec_total': soma_intervalo(row, 'I0311', 'I0376', 'ambas'),
        'qt_tec_fundamental_incomp_fem': row['I0311'] + row['I0313'] + row['I0315'],
        'qt_tec_fundamental_incomp_masc': row['I0312'] + row['I0314'] + row['I0316'],
        'qt_tec_fundamental_comp_fem': row['I0321'] + row['I0323'] + row['I0325'],  # Mapeamento direto
        'qt_tec_fundamental_comp_masc': row['I0322'] + row['I0324'] + row['I0326'],  # Mapeamento direto
        'qt_tec_medio_fem': row['I0331'] + row['I0333'] + row['I0335'],  # Mapeamento direto
        'qt_tec_medio_masc': row['I0332'] + row['I0334'] + row['I0336'],  # Mapeamento direto
        'qt_tec_superior_fem': row['I0341'] + row['I0343'] + row['I0345'],
        'qt_tec_superior_masc': row['I0342'] + row['I0344'] + row['I0346'],
        'qt_tec_especializacao_fem': row['I0351'] + row['I0353'] + row['I0355'],
        'qt_tec_especializacao_masc': row['I0352'] + row['I0354'] + row['I0356'],
        'qt_tec_mestrado_fem': row['I0361'] + row['I0363'] + row['I0365'],
        'qt_tec_mestrado_masc': row['I0362'] + row['I0364'] + row['I0366'],
        'qt_tec_doutorado_fem': row['I0371'] + row['I0373'] + row['I0375'],
        'qt_tec_doutorado_masc': row['I0372'] + row['I0374'] + row['I0376'],
        'qt_tec_titulacao_ndef': 0,
        'in_acesso_portal_capes': trata_lista(row, lista_cols=['I15251'], operacao='S'),
        'in_acesso_outras_bases': trata_lista(row, lista_cols=['I1551', 'I1581', 'I1591'], operacao='S'),
        'in_assina_outra_base': trata_lista(row, lista_cols=['I1581', 'I1591'], operacao='S'),
        'in_repositorio_institucional': trata_lista(row, lista_cols=['I15161'], operacao='S'),
        'in_busca_integrada': trata_lista(row, lista_cols=['I1581', 'I15201'], operacao='S'),
        'in_servico_internet': trata_lista(row, lista_cols=['I1551', 'I15211'], operacao='S'),
        'in_participa_rede_social': trata_lista(row, lista_cols=['I1581'], operacao='S'),
        'in_catalogo_online': trata_lista(row, lista_cols=['I1551', 'I15171', 'I15211'], operacao='S'),
        'qt_periodico_eletronico': soma_intervalo(row, 'I59011', 'I59095', 'ambas') - trata_lista(row, lista_cols=['I59011', 'I59021', 'I59031', 'I59041', 'I59051', 'I59061', 'I59071', 'I59081', 'I59091'], operacao='+'),
        'qt_livro_eletronico': trata_lista(row, lista_cols=['I59011', 'I59021', 'I59031', 'I59041', 'I59051', 'I59061', 'I59071', 'I59081', 'I59091'], operacao='+'),
        'qt_doc_total': row['I0812'] + row['I0912'],  # Mapeamento direto
        'qt_doc_exe': row['I0811'] + row['I0911'],  # Mapeamento direto
        'qt_doc_ex_femi': soma_intervalo(row, 'I07109', 'I07514', 'impar') + soma_intervalo(row, 'I64011', 'I64056', 'impar'),
        'qt_doc_ex_masc': soma_intervalo(row, 'I07109', 'I07514', 'par') + soma_intervalo(row, 'I64011', 'I64056', 'par'),
        'qt_doc_ex_genero_ndef': 0,  # Mapeamento direto
        'qt_doc_ex_sem_grad': soma_intervalo(row, 'I07109', 'I07114', 'ambas') + soma_intervalo(row, 'I64011', 'I64016', 'ambas'),
        'qt_doc_ex_grad': soma_intervalo(row, 'I07209', 'I07214', 'ambas') + soma_intervalo(row, 'I64021', 'I64026', 'ambas'),
        'qt_doc_ex_esp': soma_intervalo(row, 'I07309', 'I07314', 'ambas') + soma_intervalo(row, 'I64031', 'I64036', 'ambas'),
        'qt_doc_ex_mest': soma_intervalo(row, 'I07409', 'I07414', 'ambas') + soma_intervalo(row, 'I64041', 'I64046', 'ambas'),
        'qt_doc_ex_dout': soma_intervalo(row, 'I07509', 'I07514', 'ambas') + soma_intervalo(row, 'I64051', 'I64056', 'ambas'),
        'qt_doc_ex_titulacao_ndef': 0,
        'qt_doc_ex_int': trata_lista(row, lista_cols=['I07109', 'I07110', 'I07209', 'I07210', 'I07309', 'I07310', 'I07409', 'I07410', 'I07509', 'I07510'], operacao='+'),
        'qt_doc_ex_int_de': trata_lista(row, lista_cols=['I07109', 'I07110', 'I07209', 'I07210', 'I07309', 'I07310', 'I07409', 'I07410', 'I07509', 'I07510'], operacao='+'),
        'qt_doc_ex_int_sem_de': 0,
        'qt_doc_ex_parc': trata_lista(row, lista_cols=['I07111', 'I07112', 'I07211', 'I07212', 'I07311', 'I07312', 'I07411', 'I07412', 'I07511', 'I07512'], operacao='+'),
        'qt_doc_ex_hor': trata_lista(row, lista_cols=['I07113', 'I07114', 'I07213', 'I07214', 'I07313', 'I07314', 'I07413', 'I07414', 'I07513', 'I07514'], operacao='+'),
        'qt_doc_ex_dedicacao_ndef': 0,
        'qt_doc_ex_0_29': row['I10011'] + row['I10012'] + row['I10021'] + row['I10022'],
        'qt_doc_ex_30_34': row['I10031'] + row['I10032'],
        'qt_doc_ex_35_39': row['I10041'] + row['I10042'],
        'qt_doc_ex_40_44': row['I10051'] + row['I10052'],
        'qt_doc_ex_45_49': row['I10061'] + row['I10062'],
        'qt_doc_ex_50_54': row['I10071'] + row['I10072'],
        'qt_doc_ex_55_59': row['I10081'] + row['I10082'],
        'qt_doc_ex_60_mais': row['I10091'] + row['I10092'],
        'qt_doc_ex_idade_ndef': 0, 
        'qt_doc_ex_branca': 0,
        'qt_doc_ex_preta': 0,
        'qt_doc_ex_parda': 0,
        'qt_doc_ex_amarela': 0,
        'qt_doc_ex_indigena': 0,
        'qt_doc_ex_cor_nd': 0,
        'qt_doc_ex_raca_ndef':  row['I0812'] + row['I0912'],
        'qt_doc_ex_bra':  row['I0812'] + row['I0912'] - row['I0852'],
        'qt_doc_ex_est': row['I0852'],
        'qt_doc_ex_nacional_ndef': 0,  # Mapeamento direto
        'qt_doc_ex_com_deficiencia': soma_intervalo(row, 'I72011', 'I72105', 'ambas')
   }
   # Criar uma nova instância de Ies_censo com os dados mapeados
   ies_censo.append(dados_ies)

# Transformar o resultado em dataframe
ies_censo_df = pd.DataFrame(ies_censo)
# Tratar os campos de qt para inteiro
# Selecionar todas as colunas que começam com "qt_"
qt_columns = [col for col in ies_censo_df.columns if col.startswith('qt_')]
# Converter essas colunas para o tipo inteiro
ies_censo_df[qt_columns] = ies_censo_df[qt_columns].astype(int)
# Tratar municipio
ies_censo_df['municipio'] = ies_censo_df['municipio'].astype(str).apply(lambda x: x[:2] + x[-5:])
# Tratar a região
sql = "select m.codigo as municipio_codigo, u.regiao, m.mesorregiao, m.microrregiao from municipio m join uf u on u.sigla = m.estado"
df_aux = carregar_dataframe(sql)
# Remove as colunas que serão atualizadas
ies_censo_df.drop(columns={'regiao', 'mesorregiao', 'microrregiao'}, inplace=True)
# Unir os dados dos municípios ao dataframe original
ies_censo_df = ies_censo_df.merge(df_aux, how='left', left_on='municipio', right_on='municipio_codigo')
# Remover a coluna gerada para unificar
ies_censo_df.drop(columns={'municipio_codigo'}, inplace=True)
# tratagar org acad e a categoria
sql = "select i.codigo as codies, i.categoria, i.org_academica, mantenedora from ies i"
df_aux = carregar_dataframe(sql)
# Remove as colunas que serão atualizadas
ies_censo_df.drop(columns={'categoria', 'org_academica', 'mantenedora'}, inplace=True)
# Unir os dados dos municípios ao dataframe original
ies_censo_df = ies_censo_df.merge(df_aux, how='left', left_on='ies', right_on='codies')
# Remover a coluna gerada para unificar
ies_censo_df.drop(columns={'codies'}, inplace=True)
# descobre o nro do ultimo id
ultimo_id = ultimo_id(Ies_censo)
ultimo_id = ultimo_id[0]
# Resetando o índice para transformar o índice na primeira coluna
bd_df = recria_e_reindexa_dataframe(ies_censo_df, ultimo_id)
# Troca o nome da primeira coluna
# Salvar os dados da ies_censo
if tab_censo == 'S':
     salvar_bdados(bd_df, Ies_censo, 'id')
