import pandas as pd
import numpy as np
import gc
from bdados.tratar_dados_externos import salvar_bdados, ler_ies, ultimo_id
from bdados.ler_bdados_to_df import carregar_dataframe
from inep_models import Area_especifica, Area_detalhada, Cine_rotulo, Curso, Curso_censo
from utilities.tratar_dados import recria_e_reindexa_dataframe, soma_intervalo, trata_intervalo, trata_lista, seta_zero_colunas_com_nan, trata_localizacao_nula

# Função para substituir o prefixo com base no dicionário
def substituir_prefixo(valor):
    for prefixo, novo_prefixo in de_para_detalhada.items():
        if valor.startswith(prefixo):
            return valor.replace(prefixo, novo_prefixo, 1)
    return valor  # Retorna o valor original se nenhum prefixo corresponder

def preencher_ies(df):
    # Iterar sobre o DataFrame e preencher valores nulos
    for i in range(1, len(df)):
        if pd.isnull(df.loc[i, 'IES']) and df.loc[i, 'MASCARA'] == df.loc[i-1, 'MASCARA']:
            df.loc[i, 'IES'] = df.loc[i-1, 'IES']
    return df


tab_aread = 'S'
tab_areae = 'S'
tab_curso = 'S'
tab_rotulo = 'S'
tab_censo =  'S'
tab_ies = 'N'
soma = '+'
sim_nao = 'S'
col_todas = 'ambas'
col_par = 'par'
col_impar = 'impar'
col_2em2 = 'de2em2'

tp_rede = {
     1: 'Pública',
     2: 'Privada'}

tp_dimensao = {
    1: 'Cursos presenciais ofertados no Brasil',
    2: 'Cursos a distância ofertados no Brasil',
    3: 'Cursos a distância com dimensão de dados somente a nível Brasil',
    4: 'Cursos a distância ofertados por instituições brasileiras no exterior'}

tp_grau_acad = {
    0: 'Não Aplicável',
    1: 'Bacharelado',
    2: 'Licenciatura',
    3: 'Tecnológico',
    4: 'Bacharelado e Licenciatura'}

tp_nivel_acad = {
    1: 'Graduação',
    2: 'Sequencial de Formação Específica'}

tp_modal = {
    1: 'Presencial',
    2: 'Curso a distância'}

# Remover logo no inicia do processo
remover_cols = ['NO_REGIAO', 'NO_UF', 'NO_MUNICIPIO', 'IN_CAPITAL', 'CO_UF']
# Remover antes de salvar a tabela de censo dos cursos
remover_cols2 = ['NO_CURSO', 'NO_CINE_ROTULO', 'NO_CINE_AREA_GERAL', 'NO_CINE_AREA_ESPECIFICA', 'NO_CINE_AREA_DETALHADA', 'IN_COMUNITARIA', 'IN_CONFESSIONAL']

# Para renomear o nome das colunas
de_para_censo = {
    'nome':'ver'
}

de_para_uf = {
    11: 'RO',
    12: 'AC',
    13: 'AM',
    14: 'RR',
    15: 'PA',
    16: 'AP',
    17: 'TO',
    21: 'MA',
    22: 'PI',
    23: 'CE',
    24: 'RN',
    25: 'PB',
    26: 'PE',
    27: 'AL',
    28: 'SE',
    29: 'BA',
    31: 'MG',
    32: 'ES',
    33: 'RJ',
    35: 'SP',
    41: 'PR',
    42: 'SC',
    43: 'RS',
    50: 'MS',
    51: 'MT',
    52: 'GO',
    53: 'DF'
}

# As areas em 2008 eram apenas 8. Em 2009 foram incluidas as áreas 4-Negócios, administração e direito e 6-Computação e Tecnologias da Informação e Comunicação (TIC)
de_para_org = {
    4:3,
    6:4
}

# As areas em 2008 eram apenas 8. Em 2009 foram incluidas as áreas 4-Negócios, administração e direito e 6-Computação e Tecnologias da Informação e Comunicação (TIC)
de_para_area = {
    '4':'5',
    '5':'7',
    '6':'8',
    '7':'9',
    '8':'10'}

# Nos anos iniciais, as áreas eram diferentes do adotado a partir de 2009, portanto, há um de-para
de_para_area_especifica = {
'62':'81',
'58':'73',
'42':'51',
'44':'53',
'34':'41',
'48':'61',
'38':'42',
'52':'71',
'14':'11',
'56':'54',
'54':'72',
'85':'52',
'72':'91',
'64':'84',
'76':'92',
'86':'103',
'84':'104',
'81':'101'
}

# Nos anos iniciais, as áreas eram diferentes do adotado a partir de 2009, portanto, há um de-para
de_para_detalhada = {
'581':'0731',
'210':'0213',
'215':'0214',
'10':'0011',
'211':'0213',
'421':'0511',
'481':'0614',
'313':'0312',
'420':'0114',
'422':'0521',
'142':'0111',
'443':'0532',
'814':'1011',
'440':'0533',
'310':'0312',
'340':'0413',
'344':'0411',
'214':'0212',
'380':'0421',
'314':'0311',
'522':'0713',
'523':'0714',
'723':'0913',
'582':'0732',
'520':'0710',
'623':'0821',
'521':'0715',
'813':'1014',
'462':'0542',
'727':'0916',
'226':'0223',
'441':'0533',
'144':'0112',
'146':'0114',
'143':'0112',
'145':'0114',
'345':'0413',
'225':'0222',
'622':'0816',
'816':'0812',
'811':'1015',
'220':'0115',
'223':'0115',
'222':'0115',
'342':'0414',
'461':'0541',
'543':'0722',
'721':'0912',
'544':'0724',
'212':'0215',
'724':'0911',
'483':'0615',
'541':'0721',
'621':'0811',
'850':'0712',
'861':'1032',
'311':'0313',
'442':'0531',
'524':'0711',
'624':'0831',
'720':'0918',
'862':'1022',
'346':'0415',
'762':'0923',
'815':'1012',
'863':'1031',
'213':'0322',
'725':'0914',
'726':'0915',
'542':'0723',
'840':'1041',
'482':'0615',
'525':'0716',
'341':'0416',
'641':'0841',
'812':'1015'
}

encode = 'ISO-8859-1'
delimitador = ('|')
df = pd.DataFrame()
ano = 2007
# Definir o caminho da pasta
arqs = [f'd:/Trab/INEP/Microdados/censo/Censo_{ano}_GRADUACAO_PRESENCIAL.CSV', f'd:/Trab/INEP/Microdados/censo/Censo_{ano}_GRADUACAO_DISTANCIA.CSV']
for arq in arqs:
    file_patch = arq
    # Carregar o arquivo CSV em um DataFrame, especificando o delimitador correto
    df_parc = pd.read_csv(file_patch, delimiter=delimitador, encoding=encode)
    # deletar registros onde o curso é zero
    df_parc = df_parc[df_parc['CURSO'] != 0]
    df = pd.concat([df, df_parc])
    print(f'Leitura finalizada do censo do ano {ano} com {len(df_parc)} registros')
# remove o dataframe não mais utilizado
del df_parc
print(f'Total de registros carregados {len(df)}')
# Resetar o índice do DataFrame completo, concatenado com os df dos diversos anaos
print('Tratando os Dados... Reindexando DF')
df = df.reset_index(drop=True)
# Trata valores nulos
df = seta_zero_colunas_com_nan(df)
# A o nome da coluna AREACURSO por CO_CINE_ROTULO
df.rename(columns={'AREACURSO': 'CO_CINE_ROTULO'}, inplace=True)
# Criar dataframes de resumo para comparar se haverá a atroca dos códigos
# Resumo da quantidade de registros por CODAREAGERAL
antes_codareageral = df.groupby('CODAREAGERAL').size().reset_index(name='qtde_registros')
# Resumo da quantidade de registros por CODAREAESPECIFICA
antes_codareaespecifica = df.groupby('CODAREAESPECIFICA').size().reset_index(name='qtde_registros')
# Resumo da quantidade de registros por CODAREADETALHADA
antes_codareadetalhada = df.groupby('CODAREADETALHADA').size().reset_index(name='qtde_registros')
# Substitui prefixos dos códigos do rótulo
df['CO_CINE_ROTULO'] = df['CO_CINE_ROTULO'].apply(substituir_prefixo)
# Substituir o código da área detalhada
de_para_detalhada = {int(k): int(v) for k, v in de_para_detalhada.items()}
df['CODAREADETALHADA'] = df['CODAREADETALHADA'].replace(de_para_detalhada)
# Substituir o código da área específica
de_para_area_especifica = {int(k): int(v) for k, v in de_para_area_especifica.items()}
df['CODAREAESPECIFICA'] = df['CODAREAESPECIFICA'].replace(de_para_area_especifica)
# Substituir o código da área geral
de_para_area = {int(k): int(v) for k, v in de_para_area.items()}
df['CODAREAGERAL'] = df['CODAREAGERAL'].replace(de_para_area)
# Resumo da quantidade de registros por CODAREAGERAL
depois_codareageral = df.groupby('CODAREAGERAL').size().reset_index(name='qtde_registros')
# Resumo da quantidade de registros por CODAREAESPECIFICA
depois_codareaespecifica = df.groupby('CODAREAESPECIFICA').size().reset_index(name='qtde_registros')
# Resumo da quantidade de registros por CODAREADETALHADA
depois_codareadetalhada = df.groupby('CODAREADETALHADA').size().reset_index(name='qtde_registros')
# Validar se há novas áreas detalhadas
area_det_df = df[['CODAREADETALHADA', 'NOMEAREADETALHADA', 'CODAREAESPECIFICA']].drop_duplicates()
aread_df = area_det_df[['CODAREADETALHADA']].drop_duplicates()
# Recuperar as areas detalhadas dos dados do curso
sql = 'select a.codigo as area_detalhada from area_detalhada a order by 1'
df_aux = carregar_dataframe(sql)
#  Identificar quais registros de aread_df não estão em df_aux
aread_nao_exist = aread_df[~aread_df['CODAREADETALHADA'].isin(df_aux['area_detalhada'])]
# Unir os dados das áreas ao dataframe original
aread_nao_exist = aread_nao_exist.merge(area_det_df, how='left', left_on='CODAREADETALHADA', right_on='CODAREADETALHADA')
# renomear para o nome das colunas da tabela no banco
aread_nao_exist = aread_nao_exist.rename(columns={'CODAREADETALHADA': 'codigo', 'NOMEAREADETALHADA': 'nome', 'CODAREAESPECIFICA': 'area_especifica'})
if tab_aread == 'S':
    salvar_bdados(aread_nao_exist, Area_detalhada, 'codigo')
# remove o dataframe não mais utilizado
del aread_nao_exist, aread_df, area_det_df

# Tratar áreas específicas
area_esp_df = df[['CODAREAESPECIFICA', 'NOMEAREAESPECIFICA', 'CODAREAGERAL']].drop_duplicates()
areae_df = area_esp_df[['CODAREAESPECIFICA']].drop_duplicates()
# Recuperar as areas detalhadas dos dados do curso
sql = 'select a.codigo as area_especifica from area_especifica a order by 1'
df_aux = carregar_dataframe(sql)
#  Identificar quais registros de areae_df não estão em df_aux
areae_nao_exist = areae_df[~areae_df['CODAREAESPECIFICA'].isin(df_aux['area_especifica'])]
# Unir os dados das áreas ao dataframe original
areae_nao_exist = areae_nao_exist.merge(area_esp_df, how='left', left_on='CODAREAESPECIFICA', right_on='CODAREAESPECIFICA')
# renomear para o nome das colunas da tabela no banco
areae_nao_exist = areae_nao_exist.rename(columns={'CODAREAESPECIFICA': 'codigo', 'NOMEAREAESPECIFICA': 'nome', 'CODAREAGERAL': 'area'})
if tab_areae == 'S':
    salvar_bdados(areae_nao_exist, Area_especifica, 'codigo')
del areae_nao_exist, areae_df, area_esp_df

# Tratar os cursos
curso_df = df[['CURSO', 'NOME_CURSO', 'CODAREADETALHADA']].drop_duplicates()
cursoe_df = curso_df[['CURSO']].drop_duplicates()
# Recuperar as areas detalhadas dos dados do curso
sql = 'select * from curso order by 1'
df_aux = carregar_dataframe(sql)
#  Identificar quais registros de cursoe_df não estão em df_aux
curso_nao_exist = cursoe_df[~cursoe_df['CURSO'].isin(df_aux['codigo'])]
# Unir os dados das áreas ao dataframe original
curso_nao_exist = curso_nao_exist.merge(curso_df, how='left', left_on='CURSO', right_on='CURSO')
# renomear para o nome das colunas da tabela no banco
curso_nao_exist = curso_nao_exist.rename(columns={'CURSO': 'codigo', 'NOME_CURSO': 'nome', 'CODAREADETALHADA': 'area_detalhada'})
curso_nao_exist['nome'] = curso_nao_exist['nome'].fillna('Indefinido')
if tab_curso == 'S':
    salvar_bdados(curso_nao_exist, Curso, 'codigo')
del cursoe_df, curso_nao_exist, curso_df

# Tratar os rótulos
rotulo_df = df[['CO_CINE_ROTULO', 'NOMEAREACURSO']].drop_duplicates()
rotuloe_df = rotulo_df[['CO_CINE_ROTULO']].drop_duplicates()
# Recuperar as areas detalhadas dos dados do curso
sql = 'select * from cine_rotulo order by 1'
df_aux = carregar_dataframe(sql)
#  Identificar quais registros de cursoe_df não estão em df_aux
rotulo_nao_exist = rotuloe_df[~rotuloe_df['CO_CINE_ROTULO'].isin(df_aux['codigo'])]
# Unir os dados das áreas ao dataframe original
rotulo_nao_exist = rotulo_nao_exist.merge(rotulo_df, how='left', left_on='CO_CINE_ROTULO', right_on='CO_CINE_ROTULO')
# renomear para o nome das colunas da tabela no banco
rotulo_nao_exist = rotulo_nao_exist.rename(columns={'CO_CINE_ROTULO': 'codigo', 'NOMEAREACURSO': 'nome'})
rotulo_nao_exist['nome'] = rotulo_nao_exist['nome'].fillna('Indefinido')
if tab_rotulo == 'S':
    salvar_bdados(rotulo_nao_exist, Cine_rotulo, 'codigo')
del rotulo_nao_exist, rotuloe_df, rotulo_df

# Utilizando map() para atribuir as siglas com base nos códigos
df['SIGLA_UF'] = df['COD_UF'].map(de_para_uf)

# Recuperar a IES do cadastro de cursos
sql = 'Select distinct curso as CURSO, ies as IES from curso_censo where ies < 120070001 order by 2'
df_curso_ies = carregar_dataframe(sql)
# Fazer a junção dos DataFrames com base na coluna 'curso'
df = pd.merge(df, df_curso_ies, on='CURSO', how='left')
# preencher IES qdo a mascara for igual
df = preencher_ies(df)
# Selecionar apenas as máscaras que não possuem IES
df_ies_nulos = df[df['IES'].isnull()]
df_mascaras_sem_ies = df_ies_nulos[['MASCARA']].drop_duplicates()
# Salvar em uma planilha excel
file = f'df_mascaras_sem_ies_{ano}.xlsx'
df_mascaras_sem_ies.to_excel(file, index=False)
# Selecionar as máscaras que possuem IES
df_aux = df[['MASCARA', 'IES']].drop_duplicates()
# Garantindo que a coluna IES tenha o maior valor para cada MASCARA
df_aux2 = df_aux.groupby('MASCARA', as_index=False)['IES'].agg('max')
df_mascaras_com_ies = df_aux2[['MASCARA', 'IES']].drop_duplicates()
# Salvar em uma planilha excel
file = f'df_mascaras_com_ies_{ano}.xlsx'
df_mascaras_com_ies.to_excel(file, index=False)
# Setar um ID para uso futuro a coluna IES, para que não sejam iguais aos códigos já existente de IFES
df_ies_nulos['IES'] = df_ies_nulos['MASCARA'].apply(lambda x: int('1' + str(ano) + str(x).zfill(4)))
# Atualiza o a coluna de IES no dataframe principal
df.update(df_ies_nulos)
# forçar o tipo de dado integer
df['IES'] = df['IES'].astype(int)
# Tratar as IES
ies_atu_df = df[['IES']].drop_duplicates()
# lER E carregar o dataframe das IES para calcular o valores a serem trocados
ies_df = ler_ies()
#valiar se há novas ies
#  Identificar quais registros de ies_nov_df['ies'] não estão em ies_df['codigo']
ies_nao_existem = ies_atu_df[~ies_atu_df['IES'].isin(ies_df['codigo'])]
# Tratar o codigo do municipio
df.rename(columns={'CODMUNIC_CURSO': 'municipio'}, inplace=True)
# Extraindo os 2 primeiros e os 5 últimos dígitos
df['municipio'] = df['municipio'].astype(str).apply(lambda x: x[:2] + x[-5:])
df.rename(columns={'SIGLA_UF': 'estado'}, inplace=True)
# Filtra as linhas onde a coluna 'regioes' possui valores nulos
nul_df = df[df['estado'].isnull()]
if len(nul_df) > 0:
    nul_df = trata_localizacao_nula(nul_df, 'estado', ies_df, 'estado', 'S')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'municipios' possui valores nulos
nul_df = df[df['municipio'].isnull()]
if len(nul_df) > 0:
    nul_df = trata_localizacao_nula(nul_df, 'municipio', ies_df, 'municipio', 'S')
    # Atualizar o df principal
    # Atualizando o DataFrame principal com os valores do DataFrame parcial
    df.update(nul_df)
# Filtra as linhas onde a coluna 'TP_REDE' possui valores nulos
df.rename(columns={'CO_REDE': 'tp_rede'}, inplace=True)
# Criando a coluna IN_GRATUITA com base na condição de TP_REDE
df['in_gratuito'] = df['tp_rede'].apply(lambda x: True if x == 1 else False)

# Tipo de Grau Acadêmico
df['tp_grau_academico'] = 0# Definindo a coluna TP_GRADU_ACADEMICO para 1 onde EH_BRACHARELADO é "S"
df.loc[df['EH_BACHARELADO'] == 'S', 'tp_grau_academico'] = 1
df.loc[df['EH_LICENCPLENA'] == 'S', 'tp_grau_academico'] = 2
df.loc[df['EH_LICCURTA'] == 'S', 'tp_grau_academico'] = 2
df.loc[df['EH_TECNO'] == 'S', 'tp_grau_academico'] = 3

# Categoria
df['categoria'] = 5
df.loc[df['CATEGADM'] == 'FEDERAL', 'categoria'] = 1
df.loc[df['CATEGADM'] == 'ESTADUAL', 'categoria'] = 2
df.loc[df['CATEGADM'] == 'MUNICIPAL', 'categoria'] = 3
df.loc[(df['CATEGADM'] == 'PRIVADA') & (df['CATADMPARTSE'] == 'S'), 'categoria'] = 4
df.loc[(df['CATEGADM'] == 'PRIVADA') & (df['CATADMCONFESS'] == 'S'), 'categoria'] = 9
df.loc[(df['CATEGADM'] == 'PRIVADA') & (df['CATADMCOMUN'] == 'S'), 'categoria'] = 9
df.loc[(df['CATEGADM'] == 'PRIVADA') & (df['CATADMFILANT'] == 'S'), 'categoria'] = 8
depois_cat = df.groupby('categoria').size().reset_index(name='qtde_registros')

df['dimensao'] = 1
df.loc[df['MOD_DISTANCIA'] == 'S', 'dimensao'] = 2

# Modalidade de ensino
df['tp_modalidade_ensino'] = 1
df.loc[df['MOD_DISTANCIA'] == 'S', 'tp_modalidade_ensino'] = 2
# Nivel academico
df['tp_nivel_academico'] = 2
df.loc[df['NIVELCURSO'] == 'GRADUACAO', 'tp_nivel_academico'] = 2

# Organicação acad
antes_org = df.groupby('CO_ORG').size().reset_index(name='qtde_registros')
df['CO_ORG'] = df['CO_ORG'].replace(de_para_org)
df.rename(columns={'CO_ORG': 'org_academica'}, inplace=True)
depois_org = df.groupby('org_academica').size().reset_index(name='qtde_registros')

# Tratar a região
df.loc[df['REGIAO'] == 'Sul', 'regiao'] = 4
df.loc[df['REGIAO'] == 'Sudeste', 'regiao'] = 3
df.loc[df['REGIAO'] == 'Nordeste', 'regiao'] = 2
df.loc[df['REGIAO'] == 'Norte', 'regiao'] = 1
df.loc[df['REGIAO'] == 'Centro-Oeste', 'regiao'] = 5

# Trocar o nome de algumas colunas
#[, 'CO_CINE_ROTULO', 'NOMEAREACURSO', 'CODAREAGERAL', 'NOMEAREAGERAL', 'CODAREAESPECIFICA', 'NOMEAREAESPECIFICA', 'CODAREADETALHADA', 'NOMEAREADETALHADA', 'CODMUNIC', 'NOME_MUNICIPIO', 'EH_CAPITAL', 'COD_UF', 'NOME_UF', 'estado', 'REGIAO', 'org_academica', 'NOMEORG', 'TP_REDE', 'REDE', 'CATEGADM', 'CO_DEP', 'NOMEDEP', 'CATADMPARTSE', 'CATADMCOMUN', 'CATADMCONFESS', 'CATADMFILANT', 'NUMERODECURSOS', 'C62011', 'C62012', 'C62021', 'C62022', 'C62031', 'C62032', 'C62041', 'C62042', 'C62051', 'C62052', 'C62061', 'C62062', 'C62071', 'C62072', 'C62081', 'C62082', 'C62091', 'C62092', 'C62101', 'C62102', 'C63011', 'C63012', 'C63021', 'C63022', 'C63031', 'C63032', 'C63041', 'C63042', 'C63051', 'C63052', 'C63061', 'C63062', 'C63071', 'C63072', 'C63081', 'C63082', 'C63091', 'C63092', 'C63101', 'C63102', 'C6401', 'C6402', 'C6403', 'C6404', 'C6405', 'C6406', 'C6407', 'C6408', 'C6409', 'C6410', 'C6411', 'C6412', 'C6413', 'C6414', 'C6415', 'C6416', 'C6417', 'C6418', 'C6419', 'C6420', 'C6501', 'C6502', 'C6503', 'C6504', 'C6505', 'C6506', 'C6507', 'C6508', 'C6509', 'C6510', 'C6511', 'C6512', 'C6513', 'C6514', 'C6515', 'C6516', 'C6517', 'C6518', 'C6519', 'C6520', 'C6601', 'C6602', 'C6603', 'C6604', 'C6605', 'C6606', 'C6607', 'C6608', 'C6609', 'C6610', 'C6611', 'C6612', 'C6613', 'C6614', 'C6615', 'C6616', 'C6617', 'C6618', 'C6619', 'C6620', 'C67011', 'C67012', 'C67013', 'C67014', 'C67015', 'C67016', 'C67021', 'C67022', 'C67023', 'C67024', 'C67025', 'C67026', 'C67031', 'C67032', 'C67033', 'C67034', 'C67035', 'C67036', 'C67041', 'C67042', 'C67043', 'C67044', 'C67045', 'C67046', 'C67051', 'C67052', 'C67053', 'C67054', 'C67055', 'C67056', 'C67061', 'C67062', 'C67063', 'C67064', 'C67065', 'C67066', 'C67071', 'C67072', 'C67073', 'C67074', 'C67075', 'C67076', 'C67081', 'C67082', 'C67083', 'C67084', 'C67085', 'C67086', 'C67091', 'C67092', 'C67093', 'C67094', 'C67095', 'C67096', 'C67101', 'C67102', 'C67103', 'C67104', 'C67105', 'C67106', 'C68011', 'C68012', 'C68013', 'C68014', 'C68015', 'C68016', 'C68021', 'C68022', 'C68023', 'C68024', 'C68025', 'C68026', 'C68031', 'C68032', 'C68033', 'C68034', 'C68035', 'C68036', 'C68041', 'C68042', 'C68043', 'C68044', 'C68045', 'C68046', 'C68051', 'C68052', 'C68053', 'C68054', 'C68055', 'C68056', 'C68061', 'C68062', 'C68063', 'C68064', 'C68065', 'C68066', 'C68071', 'C68072', 'C68073', 'C68074', 'C68075', 'C68076', 'C68081', 'C68082', 'C68083', 'C68084', 'C68085', 'C68086', 'C68091', 'C68092', 'C68093', 'C68094', 'C68095', 'C68096', 'C68101', 'C68102', 'C68103', 'C68104', 'C68105', 'C68106', 'C6901', 'C6902', 'C6903', 'C6904', 'C6905', 'C6906', 'C6907', 'C6908', 'C6909', 'C6910', 'C6911', 'C6912', 'C6913', 'C6914', 'C6915', 'C6916', 'C6917', 'C6918', 'C6919', 'C6920', 'C6921', 'C6922', 'C6923', 'C6924', 'C6925', 'C6926', 'C6927', 'C6928', 'C6929', 'C6930', 'C6931', 'C6932', 'C6933', 'C6934', 'C6935', 'C6936', 'C6937', 'C6938', 'C6939', 'C6940', 'C6941', 'C6942', 'C6943', 'C6944', 'C6945', 'C6946', 'C6947', 'C6948', 'C6949', 'C6950', 'C6951', 'C6952', 'C6953', 'C6954', 'C6955', 'C6956', 'C6957', 'C6958', 'C6959', 'C6960', 'C7001', 'C7002', 'C7003', 'C7004', 'C7005', 'C7006', 'C7007', 'C7008', 'C7009', 'C7010', 'C7011', 'C7012', 'C7013', 'C7014', 'C7015', 'C7016', 'C7017', 'C7018', 'C7019', 'C7020', 'C7021', 'C7022', 'C7023', 'C7024', 'C7025', 'C7026', 'C7027', 'C7028', 'C7029', 'C7030', 'C7031', 'C7032', 'C7033', 'C7034', 'C7035', 'C7036', 'C7037', 'C7038', 'C7039', 'C7040', 'C7041', 'C7042', 'C7043', 'C7044', 'C7045', 'C7046', 'C7047', 'C7048', 'C7049', 'C7050', 'C7051', 'C7052', 'C7053', 'C7054', 'C7055', 'C7056', 'C7057', 'C7058', 'C7059', 'C7060', 'C7101', 'C7102', 'C7103', 'C7104', 'C7105', 'C7106', 'C7107', 'C7108', 'C7109', 'C7110', 'C7111', 'C7112', 'C7113', 'C7114', 'C7115', 'C7116', 'C7117', 'C7118', 'C7119', 'C7120', 'C7121', 'C7122', 'C7123', 'C7124', 'C7125', 'C7126', 'C7127', 'C7128', 'C7129', 'C7130', 'C7131', 'C7132', 'C7133', 'C7134', 'C7135', 'C7136', 'C7137', 'C7138', 'C7139', 'C7140', 'C7141', 'C7142', 'C7143', 'C7144', 'C7145', 'C7146', 'C7147', 'C7148', 'C7149', 'C7150', 'C7151', 'C7152', 'C7153', 'C7154', 'C7155', 'C7156', 'C7157', 'C7158', 'C7159', 'C7160', 'C72011', 'C72012', 'C72013', 'C72014', 'C72021', 'C72022', 'C72023', 'C72024', 'C72031', 'C72032', 'C72033', 'C72034', 'C72041', 'C72042', 'C72043', 'C72044', 'C72051', 'C72052', 'C72053', 'C72054', 'C72061', 'C72062', 'C72063', 'C72064', 'C72071', 'C72072', 'C72073', 'C72074', 'C72081', 'C72082', 'C72083', 'C72084', 'C72091', 'C72092', 'C72093', 'C72094', 'C72101', 'C72102', 'C72103', 'C72104', 'C73011', 'C73012', 'C73013', 'C73014', 'C73021', 'C73022', 'C73023', 'C73024', 'C73031', 'C73032', 'C73033', 'C73034', 'C73041', 'C73042', 'C73043', 'C73044', 'C73051', 'C73052', 'C73053', 'C73054', 'C73061', 'C73062', 'C73063', 'C73064', 'C73071', 'C73072', 'C73073', 'C73074', 'C73081', 'C73082', 'C73083', 'C73084', 'C73091', 'C73092', 'C73093', 'C73094', 'C73101', 'C73102', 'C73103', 'C73104', 'C7401', 'C7402', 'C7403', 'C7404', 'C7405', 'C7406', 'C7407', 'C7408', 'C7409', 'C7410', 'C7411', 'C7412', 'C7413', 'C7414', 'C7415', 'C7416', 'C7417', 'C7418', 'C7419', 'C7420', 'C7421', 'C7422', 'C7423', 'C7424', 'C7425', 'C7426', 'C7427', 'C7428', 'C7429', 'C7430', 'C7431', 'C7432', 'C7433', 'C7434', 'C7435', 'C7436', 'C7437', 'C7438', 'C7439', 'C7440', 'C7501', 'C7502', 'C7503', 'C7504', 'C7505', 'C7506', 'C7507', 'C7508', 'C7509', 'C7510', 'C7511', 'C7512', 'C7513', 'C7514', 'C7515', 'C7516', 'C7517', 'C7518', 'C7519', 'C7520', 'C7521', 'C7522', 'C7523', 'C7524', 'C7525', 'C7526', 'C7527', 'C7528', 'C7529', 'C7530', 'C7531', 'C7532', 'C7533', 'C7534', 'C7535', 'C7536', 'C7537', 'C7538', 'C7539', 'C7540', 'C7601', 'C7602', 'C7603', 'C7604', 'C7605', 'C7606', 'C7607', 'C7608', 'C7609', 'C7610', 'C7611', 'C7612', 'C7613', 'C7614', 'C7615', 'C7616', 'C7617', 'C7618', 'C7619', 'C7620', 'C7621', 'C7622', 'C7623', 'C7624', 'C7625', 'C7626', 'C7627', 'C7628', 'C7629', 'C7630', 'C7631', 'C7632', 'C7633', 'C7634', 'C7635', 'C7636', 'C7637', 'C7638', 'C7639', 'C7640', 'C03011', 'C03012', 'C03013', 'C03014', 'C03031', 'C03032', 'C03033', 'C03034', 'C03051', 'C03052', 'C03053', 'C03054', 'C03071', 'C03072', 'C03073', 'C03074', 'C03091', 'C03092', 'C03093', 'C03094', 'C03131', 'C03132', 'C03133', 'C03134', 'C03151', 'C03152', 'C03153', 'C03154', 'C03021', 'C03022', 'C03023', 'C03024', 'C03041', 'C03042', 'C03043', 'C03044', 'C03061', 'C03062', 'C03063', 'C03064', 'C03081', 'C03082', 'C03083', 'C03084', 'C03101', 'C03102', 'C03103', 'C03104', 'C03141', 'C03142', 'C03143', 'C03144', 'C03161', 'C03162', 'C03163', 'C03164', 'C03185', 'C03186', 'C03187', 'C03188', 'C03189', 'C03190', 'C03191', 'C03192', 'C03193', 'C03194', 'C03195', 'C03196', 'C03197', 'C03198', 'C03199', 'C03200', 'C7701', 'C7702', 'C7703', 'C7704', 'C7705', 'C7706', 'C7707', 'C7708', 'C7709', 'C7710', 'C7711', 'C7712', 'C7713', 'C7714', 'C7715', 'C7716', 'C7717', 'C7718', 'C7719', 'C7720', 'C7721', 'C7722', 'C7723', 'C7724', 'C7725', 'C7726', 'C7727', 'C7728', 'C7729', 'C7730', 'C7731', 'C7732', 'C7733', 'C7734', 'C7735', 'C7736', 'C7737', 'C7738', 'C7739', 'C7740', 'C7741', 'C7742', 'C7743', 'C7744', 'C7745', 'C7746', 'C7747', 'C7748', 'C7749', 'C7750', 'C7751', 'C7752', 'C7753', 'C7754', 'C7755', 'C7756', 'C7757', 'C7758', 'C7759', 'C7760', 'C7761', 'C7762', 'C7763', 'C7764', 'C7765', 'C7766', 'C7767', 'C7768', 'C7769', 'C7770', 'C7771', 'C7772', 'C09011', 'C09012', 'C09021', 'C09022', 'C09031', 'C09032', 'C09041', 'C09042', 'C09051', 'C09052', 'C09061', 'C09062', 'C09071', 'C09072', 'C09081', 'C09082', 'C09091', 'C09092', 'C09101', 'C09102', 'C09111', 'C09112', 'C09121', 'C09122', 'C09131', 'C09132', 'C09141', 'C09142', 'C09151', 'C09152', 'C09161', 'C09162', 'C09171', 'C09172', 'C09181', 'C09182', 'C09191', 'C09192', 'C09201', 'C09202', 'C09211', 'C09212', 'C09221', 'C09222', 'C14111', 'C14112', 'C14113', 'C14114', 'C14121', 'C14122', 'C14123', 'C14124', 'C0621', 'C0622', 'C0623', 'C0624', 'C0631', 'C0632', 'C0633', 'C0634', 'C14211', 'C14212', 'C14213', 'C14214', 'C14221', 'C14222', 'C14223', 'C14224', 'C1011', 'C1012', 'C1013', 'C1014', 'C1021', 'C1022', 'C1023', 'C1024', 'C1031', 'C1032', 'C1033', 'C1034', 'C1015', 'C1016', 'C1017', 'C1018', 'C1025', 'C1026', 'C1027', 'C1028', 'C1035', 'C1036', 'C1037', 'C1038', 'C145011', 'C145012', 'C145021', 'C145022', 'C145031', 'C145032', 'C145041', 'C145042', 'C8111', 'C8112', 'C8113', 'C8114', 'C8121', 'C8122', 'C8123', 'C8124', 'C8211', 'C8212', 'C8213', 'C8214', 'C8221', 'C8222', 'C8223', 'C8224', 'C8231', 'C8232', 'C8233', 'C8234', 'C8241', 'C8242', 'C8243', 'C8244', 'C8251', 'C8252', 'C8253', 'C8254', 'C8271', 'C8272', 'C8273', 'C8274', 'C8281', 'C8282', 'C8283', 'C8284', 'C82101', 'C82102', 'C82103', 'C82104', 'C82111', 'C82112', 'C82113', 'C82114', 'C82121', 'C82122', 'C82123', 'C82124', 'C831', 'C832', 'C833', 'C834', 'C835', 'C836', 'C837', 'C838', 'C7811', 'C7812', 'C7813', 'C7814', 'C7821', 'C7822', 'C7823', 'C7824', 'C0421', 'C0422', 'C0423', 'C0424', 'C0431', 'C0432', 'C0433', 'C0434', 'C111', 'C112', 'C113', 'C114', 'C115', 'C116', 'C117', 'C118', 'C79011', 'C79012', 'C79013', 'C79014', 'C79021', 'C79022', 'C79023', 'C79024', 'C79041', 'C79042', 'C79043', 'C79044', 'C79051', 'C79052', 'C79053', 'C79054', 'C79061', 'C79062', 'C79063', 'C79064', 'C79071', 'C79072', 'C79073', 'C79074', 'C79081', 'C79082', 'C79083', 'C79084', 'C79091', 'C79092', 'C79093', 'C79094', 'C79111', 'C79112', 'C79113', 'C79114', 'C79121', 'C79122', 'C79123', 'C79124', 'C79131', 'C79132', 'C79133', 'C79134', 'C79141', 'C79142', 'C79143', 'C79144', 'C801', 'C802', 'C803', 'C804', 'C805', 'C806', 'C807', 'C808', 'C1511', 'C1521', 'C1531', 'C1541', 'C1551', 'C1571', 'C1581', 'C1591', 'C15101', 'C15111', 'C15121', 'C1611', 'C1612', 'C1613', 'C1614', 'C1615', 'C1616', 'C1617', 'C1621', 'C1622', 'C1623', 'C1624', 'C1625', 'C1626', 'C1627', 'C1631', 'C1632', 'C1633', 'C1634', 'C1635', 'C1636', 'C1637', 'C1641', 'C1642', 'C1643', 'C1644', 'C1645', 'C1646', 'C1647', 'C1651', 'C1652', 'C1653', 'C1654', 'C1655', 'C1656', 'C1657', 'C1661', 'C1662', 'C1663', 'C1664', 'C1665', 'C1666', 'C1667', 'C1671', 'C1672', 'C1673', 'C1674', 'C1675', 'C1676', 'C1677', 'C1681', 'C1682', 'C1683', 'C1684', 'C1685', 'C1686', 'C1687', 'C1691', 'C1692', 'C1693', 'C1694', 'C1695', 'C1696', 'C1697', 'C16101', 'C16102', 'C16103', 'C16104', 'C16105', 'C16106', 'C16107', 'C16111', 'C16112', 'C16113', 'C16114', 'C16115', 'C16116', 'C16117', 'C16121', 'C16122', 'C16123', 'C16124', 'C16125', 'C16126', 'C16127', 'C16131', 'C16132', 'C16133', 'C16134', 'C16135', 'C16136', 'C16137', 'C16141', 'C16142', 'C16143', 'C16144', 'C16145', 'C16146', 'C16147', 'C16151', 'C16152', 'C16153', 'C16154', 'C16155', 'C16156', 'C16157', 'C16161', 'C16162', 'C16163', 'C16164', 'C16165', 'C16166', 'C16167', 'C16171', 'C16172', 'C16173', 'C16174', 'C16175', 'C16176', 'C16177', 'C16181', 'C16182', 'C16183', 'C16184', 'C16185', 'C16186', 'C16187', 'C138011', 'C138012', 'C138013', 'C138014', 'C138015', 'C138016', 'C138017', 'C138018', 'C138019', 'C138021', 'C138022', 'C138023', 'C138024', 'C138025', 'C138026', 'C138027', 'C138028', 'C138029', 'C138031', 'C138032', 'C138033', 'C138034', 'C138035', 'C138036', 'C138037', 'C138038', 'C138039', 'C138041', 'C138042', 'C138043', 'C138044', 'C138045', 'C138046', 'C138047', 'C138048', 'C138049', 'C138051', 'C138052', 'C138053', 'C138054', 'C138055', 'C138056', 'C138058', 'C138059', 'C138057', 'C138061', 'C138062', 'C138063', 'C138064', 'C138065', 'C138066', 'C138067', 'C138068', 'C138069', 'C138071', 'C138078', 'C138079', 'C138072', 'C138073', 'C138074', 'C138075', 'C138076', 'C138077', 'C138081', 'C138082', 'C138083', 'C138084', 'C138085', 'C138086', 'C138087', 'C138088', 'C138089', 'C138091', 'C138092', 'C138093', 'C138094', 'C138095', 'C138098', 'C138099', 'C138096', 'C138097', 'C138101', 'C138102', 'C138103', 'C138104', 'C138105', 'C138106', 'C138107', 'C138108', 'C138109', 'C138118', 'C138119', 'C138111', 'C138112', 'C138113', 'C138114', 'C138115', 'C138116', 'C138117', 'C138121', 'C138122', 'C138123', 'C138124', 'C138125', 'C138126', 'C138127', 'C138128', 'C138129', 'C138131', 'C138132', 'C138133', 'C138134', 'C138138', 'C138139', 'C138148', 'C138149', 'C138135', 'C138136', 'C138137', 'C138141', 'C138142', 'C138143', 'C138144', 'C138145', 'C138146', 'C138147', 'C0711', 'C0713', 'C0714', 'C0715', 'C0717', 'C0731', 'C0732', 'C0733', 'C0734', 'C0735', 'C0736', 'C0737', 'C0721', 'C0741', 'C0742', 'C0723', 'C0724', 'C0725', 'C0727', 'C0743', 'C92011', 'C92021', 'C92031', 'C92041', 'C92051', 'C92061', 'C92071', 'C92081', 'C92091', 'SIGLA_UF_CURSO', 'C94011', 'C94021', 'C94031', 'C94041', 'C94051', 'C94061', 'C94071', 'C94081', 'C94091', 'C94101', 'C95011', 'C95021', 'C95031', 'C95041', 'C95051', 'C95061', 'C95071', 'C95081', 'C95091', 'C95101', 'C96011', 'C96021', 'C96031', 'C96041', 'C96051', 'C96061', 'C96071', 'C96081', 'C96091', 'C96101', 'C97011', 'C97021', 'C97031', 'C97041', 'C97051', 'C97061', 'C97071', 'C97081', 'C97091', 'C97101', 'C98011', 'C98012', 'C98021', 'C98022', 'C98031', 'C98032', 'C98041', 'C98042', 'C98051', 'C98052', 'C98061', 'C98062', 'C98071', 'C98072', 'C98081', 'C98082', 'C98091', 'C98092', 'C98101', 'C98102', 'C152011', 'C152012', 'C152021', 'C152022', 'C152031', 'C152032', 'C152041', 'C152042', 'C152051', 'C152052', 'C152061', 'C152062', 'C152071', 'C152072', 'C152081', 'C152082', 'C152091', 'C152092', 'C152101', 'C152102', 'C153011', 'C153012', 'C153021', 'C153022', 'C153031', 'C153032', 'C153041', 'C153042', 'C153051', 'C153052', 'C153061', 'C153062', 'C153071', 'C153072', 'C153081', 'C153082', 'C153091', 'C153092', 'C153101', 'C153102', 'C154011', 'C154012', 'C154021', 'C154022', 'C154031', 'C154032', 'C154041', 'C154042', 'C154051', 'C154052', 'C154061', 'C154062', 'C154071', 'C154072', 'C154081', 'C154082', 'C154091', 'C154092', 'C154101', 'C154102', 'C155011', 'C155012', 'C155021', 'C155022', 'C155031', 'C155032', 'C155041', 'C155042', 'C155051', 'C155052', 'C155061', 'C155062', 'C155071', 'C155072', 'C155081', 'C155082', 'C155091', 'C155092', 'C155101', 'C155102', 'C156011', 'C156012', 'C156021', 'C156022', 'C156031', 'C156032', 'C156041', 'C156042', 'C156051', 'C156052', 'C156061', 'C156062', 'C156071', 'C156072', 'C156081', 'C156082', 'C156091', 'C156092', 'C156101', 'C156102', 'C157011', 'C157012', 'C157021', 'C157022', 'C157031', 'C157032', 'C157041', 'C157042', 'C157051', 'C157052', 'C157061', 'C157062', 'C157071', 'C157072', 'C157081', 'C157082', 'C157091', 'C157092', 'C157101', 'C157102', 'C158011', 'C158012', 'C158021', 'C158022', 'C158031', 'C158032', 'C158041', 'C158042', 'C158051', 'C158052', 'C158061', 'C158062', 'C158071', 'C158072', 'C158081', 'C158082', 'C158091', 'C158092', 'C158101', 'C158102', 'C159011', 'C159012', 'C159021', 'C159022', 'C159031', 'C159032', 'C159041', 'C159042', 'C159051', 'C159052', 'C159061', 'C159062', 'C159071', 'C159072', 'C159081', 'C159082', 'C159091', 'C159092', 'C159101', 'C159102', 'C159111', 'C159112', 'C159121', 'C159122', 'C159131', 'C159132', 'C159141', 'C159142', 'C159151', 'C159152', 'C159161', 'C159162', 'C159171', 'C159172', 'C159181', 'C159182', 'C159191', 'C159192', 'C159201', 'C159202', 'C159211', 'C159212', 'C159221', 'C159222', 'C159231', 'C159232', 'C159241', 'C159242', 'C160011', 'C160012', 'C160021', 'C160022', 'C160031', 'C160032', 'C160041', 'C160042', 'C160051', 'C160052', 'C160061', 'C160062', 'C160071', 'C160072', 'C160081', 'C160082', 'C160091', 'C160092', 'C160101', 'C160102', 'C160111', 'C160112', 'C160121', 'C160122', 'C160131', 'C160132', 'C160141', 'C160142', 'C160151', 'C160152', 'C160161', 'C160162', 'C160171', 'C160172', 'C160181', 'C160182', 'C160191', 'C160192', 'C160201', 'C160202', 'C160211', 'C160212', 'C160221', 'C160222', 'C160231', 'C160232', 'C160241', 'C160242', 'C161011', 'C161012', 'C161021', 'C161022', 'C161031', 'C161032', 'C161041', 'C161042', 'C161051', 'C161052', 'C161061', 'C161062', 'C161071', 'C161072', 'C161081', 'C161082', 'C161091', 'C161092', 'C161101', 'C161102', 'C161111', 'C161112', 'C161121', 'C161122', 'C161131', 'C161132', 'C161141', 'C161142', 'C161151', 'C161152', 'C161161', 'C161162', 'C161171', 'C161172', 'C161181', 'C161182', 'C161191', 'C161192', 'C161201', 'C161202', 'C161211', 'C161212', 'C161221', 'C161222', 'C162011', 'C162012', 'C162021', 'C162022', 'C163011', 'C163012', 'C163021', 'C163022', 'C163031', 'C163032', 'C163041', 'C163042', 'C163051', 'C163052', 'C163013', 'C163014', 'C163023', 'C163024', 'C163033', 'C163034', 'C163043', 'C163044', 'C163053', 'C163054', 'C164011', 'C164012', 'C164021', 'C164022', 'C165011', 'C165012', 'C165021', 'C165022', 'C166011', 'C166012', 'C166021', 'C166022', 'C167011', 'C167012', 'C167021', 'C167022', 'C168011', 'C168012', 'C168021', 'C168022', 'C169011', 'C169012', 'C169021', 'C169022', 'C170011', 'C170012', 'C170021', 'C170022', 'C174011', 'C174012', 'C174013', 'C174014', 'C174015', 'C174016', 'C174021', 'C174022', 'C174023', 'C174024', 'C174025', 'C174026', 'C174031', 'C174032', 'C174033', 'C174034', 'C174035', 'C174036', 'C174041', 'C174042', 'C174043', 'C174044', 'C174045', 'C174046', 'C174051', 'C174052', 'C174053', 'C174054', 'C174055', 'C174056', 'C175011', 'C175012', 'C175013', 'C175014', 'C175015', 'C175016', 'C175021', 'C175022', 'C175023', 'C175024', 'C175025', 'C175026', 'C175031', 'C175032', 'C175033', 'C175034', 'C175035', 'C175036', 'C175041', 'C175042', 'C175043', 'C175044', 'C175045', 'C175046', 'C175051', 'C175052', 'C175053', 'C175054', 'C175055', 'C175056', 'C179011', 'C179012', 'C179021', 'C179022', 'C179031', 'C179032', 'C179041', 'C179042', 'C179051', 'C179052', 'C179061', 'C179062', 'C179071', 'C179081', 'C179091', 'C179101', 'C179111', 'C179121', 'C180011', 'C180021', 'C180031', 'C180041', 'C180051', 'C180061', 'C180071', 'C180081', 'C180091', 'C180101', 'C180111', 'C180121', 'C180131', 'C180141', 'C180151', 'C180161', 'C180171', 'C180181', 'C180191', 'C180201', 'C181011', 'C181021', 'C181031', 'C181041', 'C181051', 'C181061', 'C181071', 'C181081', 'C181091', 'IN_GRATUITO', 'TP_GRAU_ACADEMICO', 'categoria', 'dimensao', 'tp_modalidade_ensino', 'tp_nivel_academico'] [0  2008  1784  48129  ...        1                    1                   2] []
df.rename(columns={'ANO': 'ano_censo'}, inplace=True)
df.rename(columns={'IES': 'ies'}, inplace=True)
df.rename(columns={'CURSO': 'curso'}, inplace=True)
df.rename(columns={'CO_CINE_ROTULO': 'cine_rotulo'}, inplace=True)
df.rename(columns={'CODAREAGERAL': 'area_geral'}, inplace=True)
df.rename(columns={'CODAREAESPECIFICA': 'area_especifica'}, inplace=True)
df.rename(columns={'CODAREADETALHADA': 'area_detalhada'}, inplace=True)
# deletar algumas colunas que não são mais necessárias
df.drop(columns=['CODMUNIC', 'NOME_MUNICIPIO', 'EH_CAPITAL', 'COD_UF', 'NOME_UF', 'NOMEORG'], inplace=True)
df.drop(columns=['NOME_CURSO', 'REGIAO', 'DTINIFUNCCURSO', 'NIVELCURSO', 'SUBNIVEL', 'MOD_PRESENC', 'MOD_DISTANCIA'], inplace=True)
df.drop(columns=['EH_BACHARELADO', 'EH_LICENCPLENA', 'EH_LICCURTA', 'EH_TECNO', 'EH_ESPECPROF'], inplace=True)
df.drop(columns=['NOMEAREACURSO', 'NOMEAREAGERAL', 'NOMEAREAESPECIFICA', 'NOMEAREADETALHADA', 'REDE', 'CATEGADM', 'CO_DEP', 'NOMEDEP'],  inplace=True)
df.drop(columns=['CATADMPARTSE', 'CATADMCOMUN', 'CATADMCONFESS', 'CATADMFILANT', 'NUMERODECURSOS'], inplace=True)
# Substituir todos os valores NaN por zero
df.fillna(0, inplace=True)
df['regiao'] = df['regiao'].astype(int)
# remove dataframes não mais necessários
del ies_nao_existem, ies_df, ies_atu_df
# Começa a tratar o censo em si
curso_censo = []
# Iterar sobre cada linha do DataFrame
for _, row in df.iterrows():
   # Criar um dicionário para mapear campos do modelo para valores do DataFrame
   dados_curso = {
       'id': 0,
       'ano_censo': row['ano_censo'],
       'regiao': row['regiao'],
       'estado': row['estado'],
       'municipio': row['municipio'],
       'dimensao': row['dimensao'],
       'org_academica': row['org_academica'],
       'categoria': row['categoria'],
       'tp_rede': row['tp_rede'],
       'ies': row['ies'],
       'curso': row['curso'],
       'cine_rotulo': row['cine_rotulo'],
       'area_geral': row['area_geral'],
       'area_especifica': row['area_especifica'],
       'area_detalhada': row['area_detalhada'],
       'tp_grau_academico': row['tp_grau_academico'],
       'in_gratuito': row['in_gratuito'],
       'tp_modalidade_ensino': row['tp_modalidade_ensino'],
       'tp_nivel_academico': row['tp_nivel_academico'],
       'qt_curso': 1, #(Tratar cursos = zero)
       'qt_vg_total': soma_intervalo(row, 'C62011', 'C6620', col_todas) + soma_intervalo(row, 'C94011', 'C97101', col_todas),
       'qt_vg_total_diurno': soma_intervalo(row, 'C62011', 'C6620', col_impar),
       'qt_vg_total_noturno': soma_intervalo(row, 'C62011', 'C6620', col_par),
       'qt_vg_total_ead': soma_intervalo(row, 'C94011', 'C97101', col_todas),
       'qt_vg_nova': 0,
       'qt_vg_proc_seletivo': trata_lista(row, lista_cols = ['C62011', 'C62012', 'C62041', 'C62042', 'C62061', 'C62062', 'C62091', 'C62092', 'C63011', 'C63012',
                                                             'C63041', 'C63042',  'C63061', 'C63062', 'C63091', 'C63092', 'C6401', 'C6402', 'C6407', 'C6408',
                                                             'C6411', 'C6412', 'C6417', 'C6418', 'C6501', 'C6502', 'C6507', 'C6508',  'C6511', 'C6512', 'C6517',
                                                             'C6518', 'C6601', 'C6602', 'C6607', 'C6608',  'C6611', 'C6612', 'C6617', 'C6618'], operacao=soma),
       'qt_vg_remanesc': 0,
       'qt_vg_prog_especial': row['C138101'] + row['C138111'] + row['C138121'] + row['C138131'] + row['C138141'],
       'qt_inscrito_total': soma_intervalo(row, 'C67011', 'C7160', col_todas) + soma_intervalo(row, 'C98011', 'C154102', col_todas),
       'qt_inscrito_total_diurno': row['C67011'] + row['C67012'] + row['C67021'] + row['C67022'] + row['C67031'] + row['C67032'] + row['C67041'] +
                                   row['C67042'] + row['C67051'] + row['C67052'] + row['C67061'] + row['C67062'] + row['C67071'] + row['C67072'] +
                                   row['C67081'] + row['C67082'] + row['C67091'] + row['C67092'] + row['C67101'] + row['C67101'] + row['C68011'] +
                                   row['C68012'] + row['C68021'] + row['C68022'] + row['C68031'] + row['C68032'] + row['C68041'] + row['C68042'] +
                                   row['C68051'] + row['C68052'] + row['C68061'] + row['C68062'] + row['C68071'] + row['C68072'] + row['C68081'] +
                                   row['C68082'] + row['C68091'] + row['C68092'] + row['C68101'] + row['C68101'] + row['C6901'] + row['C6902'] +
                                   row['C6905'] + row['C6906'] + row['C6909'] + row['C6910'] + row['C6913'] + row['C6914'] + row['C6917'] +
                                   row['C6918'] + row['C6921'] + row['C6922'] + row['C6925'] + row['C6926'] + row['C6929'] + row['C6930'] +
                                   row['C6933'] + row['C6934'] + row['C6937'] + row['C6938'],
       'qt_inscrito_total_noturno': row['C67013'] + row['C67014'] + row['C67023'] + row['C67024'] + row['C67033'] + row['C67034'] + row['C67043'] +
                                    row['C67044'] + row['C67053'] + row['C67054'] + row['C67063'] + row['C67064'] + row['C67073'] + row['C67074'] +
                                    row['C67083'] + row['C67084'] + row['C67093'] + row['C67094'] + row['C67103'] + row['C67104'] + row['C68013'] +
                                    row['C68014'] + row['C68023'] + row['C68024'] + row['C68033'] + row['C68034'] + row['C68043'] + row['C68044'] +
                                    row['C68053'] + row['C68054'] + row['C68063'] + row['C68064'] + row['C68073'] + row['C68074'] + row['C68083'] +
                                    row['C68084'] + row['C68093'] + row['C68094'] + row['C68102'] + row['C68104'] + row['C6903'] + row['C6904'] +
                                    row['C6907'] + row['C6908'] + row['C6911'] + row['C6912'] + row['C6915'] + row['C6916'] + row['C6919'] +
                                    row['C6920'] + row['C6923'] + row['C6924'] + row['C6927'] + row['C6928'] + row['C6931'] + row['C6932'] +
                                    row['C6935'] + row['C6936'] + row['C6939'] + row['C6940'],
       'qt_inscrito_total_ead': soma_intervalo(row, 'C98011', 'C154102', col_todas),
       'qt_insc_vg_nova': 0,
       'qt_insc_proc_seletivo': soma_intervalo(row, 'C67011', 'C67016', col_todas) +
                                soma_intervalo(row, 'C67041', 'C67046', col_todas) +
                                soma_intervalo(row, 'C67061', 'C67066', col_todas) +
                                soma_intervalo(row, 'C67091', 'C67096', col_todas) +
                                soma_intervalo(row, 'C68011', 'C68016', col_todas) +
                                soma_intervalo(row, 'C68041', 'C68046', col_todas) +
                                soma_intervalo(row, 'C68061', 'C68066', col_todas) +
                                soma_intervalo(row, 'C68091', 'C68096', col_todas),
       'qt_insc_vg_remanesc': 0,
       'qt_insc_vg_prog_especial': 0,
       'qt_ing': soma_intervalo(row, 'C72011', 'C7640', col_todas) +
                 soma_intervalo(row, 'C155011', 'C158102', col_todas),
       'qt_ing_fem': soma_intervalo(row, 'C72011', 'C7640', col_impar) +
                     soma_intervalo(row, 'C155011', 'C158102', col_impar),
       'qt_ing_masc': soma_intervalo(row, 'C72011', 'C7640', col_par) +
                     soma_intervalo(row, 'C155011', 'C158102', col_par),
       'qt_ing_diurno': soma_intervalo(row, 'C72011', 'C7640', col_2em2),
       'qt_ing_noturno': soma_intervalo(row, 'C72013', 'C7640', col_2em2),
       'qt_ing_vg_nova': 0,
       'qt_ing_vestibular': soma_intervalo(row, 'C72011', 'C72014', col_todas) +
                            soma_intervalo(row, 'C72041', 'C72044', col_todas) +
                            soma_intervalo(row, 'C72061', 'C72064', col_todas) +
                            soma_intervalo(row, 'C72091', 'C72094', col_todas) +
                            soma_intervalo(row, 'C73011', 'C73014', col_todas) +
                            soma_intervalo(row, 'C73041', 'C73044', col_todas) +
                            soma_intervalo(row, 'C73061', 'C73064', col_todas) +
                            soma_intervalo(row, 'C73091', 'C73094', col_todas) +
                            soma_intervalo(row, 'C7401', 'C7404', col_todas) +
                            soma_intervalo(row, 'C7413', 'C7416', col_todas) +
                            soma_intervalo(row, 'C7421', 'C7424', col_todas) +
                            soma_intervalo(row, 'C7433', 'C7436', col_todas) +
                            soma_intervalo(row, 'C7501', 'C7504', col_todas) +
                            soma_intervalo(row, 'C7513', 'C7516', col_todas) +
                            soma_intervalo(row, 'C7521', 'C7524', col_todas) +
                            soma_intervalo(row, 'C7533', 'C7536', col_todas) +
                            soma_intervalo(row, 'C7601', 'C7604', col_todas) +
                            soma_intervalo(row, 'C7613', 'C7616', col_todas) +
                            soma_intervalo(row, 'C7621', 'C7624', col_todas) +
                            soma_intervalo(row, 'C7633', 'C7636', col_todas) +
                            soma_intervalo(row, 'C155011', 'C155011', col_todas) +
                            trata_lista(row, lista_cols= ['C155041', 'C155042', 'C155061', 'C155062', 'C155091', 'C155092'], operacao=soma) +
                            trata_lista(row, lista_cols= ['C156011', 'C156041', 'C156042', 'C156061', 'C156062', 'C156091', 'C156092'], operacao=soma) +
                            trata_lista(row, lista_cols= ['C157011', 'C157041', 'C157042', 'C157061', 'C157062', 'C157091', 'C157092'], operacao=soma) +
                            trata_lista(row, lista_cols= ['C158011', 'C158041', 'C158042', 'C158061', 'C158062', 'C158091', 'C158092'], operacao=soma),
       'qt_ing_enem': soma_intervalo(row, 'C72021', 'C72024', col_todas) +
                      soma_intervalo(row, 'C72041', 'C72044', col_todas) +
                      soma_intervalo(row, 'C72071', 'C72074', col_todas) +
                      soma_intervalo(row, 'C72091', 'C72094', col_todas) +
                      soma_intervalo(row, 'C73021', 'C73024', col_todas) +
                      soma_intervalo(row, 'C73041', 'C73044', col_todas) +
                      soma_intervalo(row, 'C73071', 'C73074', col_todas) +
                      soma_intervalo(row, 'C73091', 'C73094', col_todas) +
                      soma_intervalo(row, 'C7405', 'C7408', col_todas) +
                      soma_intervalo(row, 'C7413', 'C7416', col_todas) +
                      soma_intervalo(row, 'C7425', 'C7428', col_todas) +
                      soma_intervalo(row, 'C7433', 'C7436', col_todas) +
                      soma_intervalo(row, 'C7505', 'C7508', col_todas) +
                      soma_intervalo(row, 'C7513', 'C7516', col_todas) +
                      soma_intervalo(row, 'C7525', 'C7528', col_todas) +
                      soma_intervalo(row, 'C7533', 'C7536', col_todas) +
                      soma_intervalo(row, 'C7605', 'C7608', col_todas) +
                      soma_intervalo(row, 'C7613', 'C7616', col_todas) +
                      soma_intervalo(row, 'C7625', 'C7628', col_todas) +
                      soma_intervalo(row, 'C7633', 'C7636', col_todas) +
                      trata_lista(row, lista_cols= ['C155012', 'C155021', 'C155041', 'C155042', 'C155071', 'C155072', 'C155091', 'C155091'], operacao=soma) +
                      trata_lista(row, lista_cols= ['C156012', 'C156021', 'C156041', 'C156042', 'C156071', 'C156072', 'C156091', 'C156091'], operacao=soma) +
                      trata_lista(row, lista_cols= ['C157012', 'C157021', 'C157041', 'C157042', 'C157071', 'C157072', 'C157091', 'C157091'], operacao=soma) +
                      trata_lista(row, lista_cols= ['C158012', 'C158021', 'C158041', 'C158042', 'C158071', 'C158072', 'C158091', 'C158091'], operacao=soma),
       'qt_ing_avaliacao_seriada':  soma_intervalo(row, 'C72031', 'C72034', col_todas) +
                                    soma_intervalo(row, 'C72081', 'C72084', col_todas) +
                                    soma_intervalo(row, 'C73031', 'C73034', col_todas) +
                                    soma_intervalo(row, 'C73081', 'C73084', col_todas) +
                                    soma_intervalo(row, 'C7409', 'C7412', col_todas) +
                                    soma_intervalo(row, 'C7429', 'C7432', col_todas) +
                                    soma_intervalo(row, 'C7509', 'C7512', col_todas) +
                                    soma_intervalo(row, 'C7529', 'C7532', col_todas) +
                                    soma_intervalo(row, 'C7609', 'C7612', col_todas) +
                                    soma_intervalo(row, 'C7629', 'C7632', col_todas) +
                                    trata_lista(row, lista_cols= ['C155022', 'C155031', 'C155032', 'C155081', 'C155082'], operacao=soma) +
                                    trata_lista(row, lista_cols= ['C156022', 'C156031', 'C156032', 'C156081', 'C156082'], operacao=soma) +
                                    trata_lista(row, lista_cols= ['C157022', 'C157031', 'C157032', 'C157081', 'C157082'], operacao=soma) +
                                    trata_lista(row, lista_cols= ['C158022', 'C158031', 'C158032', 'C158081', 'C158082'], operacao=soma),
       'qt_ing_selecao_simplifica':  0,
       'qt_ing_egr': soma_intervalo(row, 'C03021', 'C03024', col_todas) +
                     soma_intervalo(row, 'C03193', 'C03196', col_todas) +
                     soma_intervalo(row, 'C7729', 'C7732', col_todas) +
                     soma_intervalo(row, 'C7765', 'C7768', col_todas) +
                     soma_intervalo(row, 'C159101', 'C159102', col_todas) +
                     soma_intervalo(row, 'C159221', 'C159222', col_todas) +
                     soma_intervalo(row, 'C160101', 'C160102', col_todas) +
                     soma_intervalo(row, 'C160221', 'C160222', col_todas),
       'qt_ing_outro_tipo_selecao': soma_intervalo(row, 'C72051', 'C72054', col_todas) +
                                    soma_intervalo(row, 'C72101', 'C72104', col_todas) +
                                    soma_intervalo(row, 'C73051', 'C73054', col_todas) +
                                    soma_intervalo(row, 'C73101', 'C73104', col_todas) +
                                    soma_intervalo(row, 'C7417', 'C7420', col_todas) +
                                    soma_intervalo(row, 'C7437', 'C7440', col_todas) +
                                    soma_intervalo(row, 'C7517', 'C7520', col_todas) +
                                    soma_intervalo(row, 'C7537', 'C7540', col_todas) +
                                    soma_intervalo(row, 'C7617', 'C7620', col_todas) +
                                    soma_intervalo(row, 'C7637', 'C7640', col_todas) +
                                    trata_lista(row, lista_cols= ['C155051', 'C155052', 'C155101', 'C155102'], operacao=soma) +
                                    trata_lista(row, lista_cols= ['C156051', 'C156052', 'C156101', 'C156102'], operacao=soma) +
                                    trata_lista(row, lista_cols= ['C157051', 'C157052', 'C157101', 'C157102'], operacao=soma) +
                                    trata_lista(row, lista_cols= ['C158051', 'C158052', 'C158101', 'C158102'], operacao=soma),
       'qt_ing_proc_seletivo':  0,
       'qt_ing_vg_remanesc':  0,
       'qt_ing_vg_prog_especial':  0,
       'qt_ing_outra_forma':  0,
       'qt_ing_0_17': row['C09011'] + row['C09012'] + row['C09121'] + row['C09122'] + row['C161011'] + row['C161012'] + row['C161121'] + row['C161122'],
       'qt_ing_18_24': row['C09021'] + row['C09022'] + row['C09131'] + row['C09132'] + row['C161021'] + row['C161022'] + row['C161131'] + row['C161132'],
       'qt_ing_25_29': row['C09031'] + row['C09032'] + row['C09141'] + row['C09142'] + row['C161031'] + row['C161032'] + row['C161141'] + row['C161142'],
       'qt_ing_30_34': row['C09041'] + row['C09042'] + row['C09151'] + row['C09152'] + row['C161041'] + row['C161042'] + row['C161151'] + row['C161152'],
       'qt_ing_35_39': row['C09051'] + row['C09052'] + row['C09161'] + row['C09162'] + row['C161051'] + row['C161052'] + row['C161161'] + row['C161162'],
       'qt_ing_40_49': row['C09061'] + row['C09062'] + row['C09071'] + row['C09072'] + row['C09171'] + row['C09172'] + row['C09181'] + row['C09182'] +
                       row['C161061'] + row['C161062'] + row['C161171'] + row['C161172'] + row['C161071'] + row['C161072'] + row['C161181'] + row['C161182'],
       'qt_ing_50_59': row['C09081'] + row['C09082'] + row['C09091'] + row['C09092'] + row['C09191'] + row['C09192'] + row['C09201'] + row['C09202'] +
                       row['C161081'] + row['C161082'] + row['C161191'] + row['C161192'] + row['C161091'] + row['C161092'] + row['C161201'] + row['C161201'],
       'qt_ing_60_mais': row['C09101'] + row['C09102'] + row['C09111'] + row['C09112'] + row['C09211'] + row['C09212'] + row['C09221'] + row['C09222'] +
                         row['C161101'] + row['C161102'] + row['C161211'] + row['C161212'] + row['C161111'] + row['C161112'] + row['C161221'] + row['C161222'],
       'qt_ing_branca': 0,
       'qt_ing_preta': row['C138014'] + row['C138015'] + row['C138024'] + row['C138025'],
       'qt_ing_parda': row['C138034'] + row['C138035'] + row['C138044'] + row['C138045'],
       'qt_ing_amarela': 0,
       'qt_ing_indigena': row['C138054'] + row['C138055'] + row['C138064'] + row['C138065'],
       'qt_ing_cornd': soma_intervalo(row, 'C72011', 'C7640', col_todas) +
                       soma_intervalo(row, 'C155011', 'C158102', col_todas) -
                       trata_lista(row, lista_cols= ['C138014', 'C138015', 'C138024', 'C138025'], operacao=soma) -
                       trata_lista(row, lista_cols= ['C138034', 'C138035', 'C138044', 'C138045'], operacao=soma) -
                       trata_lista(row, lista_cols= ['C138054', 'C138055', 'C138064', 'C138065'], operacao=soma) ,
       'qt_ing_mob_academica': soma_intervalo(row, 'C03011', 'C03054', col_todas) +
                               soma_intervalo(row, 'C159011', 'C159052', col_todas) +
                               soma_intervalo(row, 'C159111', 'C159112', col_todas) +
                               soma_intervalo(row, 'C159151', 'C159172', col_todas) +
                               soma_intervalo(row, 'C159231', 'C159232', col_todas) +
                               soma_intervalo(row, 'C160011', 'C160052', col_todas) +
                               soma_intervalo(row, 'C160111', 'C160112', col_todas) +
                               soma_intervalo(row, 'C160151', 'C160172', col_todas) +
                               soma_intervalo(row, 'C160231', 'C160232', col_todas),
       'qt_ing_nacbras': soma_intervalo(row, 'C72011', 'C7640', col_todas) +
                         soma_intervalo(row, 'C155011', 'C158102', col_todas),
       'qt_ing_nacestrang': 0,
       'qt_ing_financ': soma_intervalo(row, 'C1511', 'C16187', col_todas),
       'qt_ing_financ_reemb': soma_intervalo(row, 'C1511', 'C1551', col_todas) +
                              soma_intervalo(row, 'C15101', 'C15121', col_todas),
       'qt_ing_fies': row['C1511'],
       'qt_ing_rpfies': 0,
       'qt_ing_financ_reemb_outros': soma_intervalo(row, 'C1521', 'C1551', col_todas),
       'qt_ing_financ_nreemb': soma_intervalo(row, 'C1571', 'C1591', col_todas),
       'qt_ing_prounii': row['C1571'],
       'qt_ing_prounip': row['C1581'],
       'qt_ing_nrpfies': 0,
       'qt_ing_financ_nreemb_outros': row['C1591'] + soma_intervalo(row, 'C15101', 'C15121', col_todas),
       'qt_ing_deficiente': row['C138094'] + row['C138095'] + row['C138104'] + row['C138105'],
       'qt_ing_reserva_vaga': 0,
       'qt_ing_rvredepublica': row['C138114'] + row['C138115'] + row['C138124'] + row['C138125'],
       'qt_ing_rvetnico': 0,
       'qt_ing_rvpdef': row['C138091'] + row['C138101'],
       'qt_ing_rvsocial_rf': 0,
       'qt_ing_rvoutros': row['C138134'] + row['C138135'] + row['C138144'] + row['C138145'],
       'qt_ing_procescpublica': 0,
       'qt_ing_procescprivada': 0,
       'qt_ing_procnaoinformada': 0,
       'qt_ing_parfor': 0,
       'qt_ing_ativ_extracurricular': 0,
       'qt_ing_apoio_social': soma_intervalo(row, 'C1571', 'C15121', col_todas),
       'qt_mat': soma_intervalo(row, 'C7811', 'C7814', col_todas) +
                 soma_intervalo(row, 'C0421', 'C0424', col_todas) +
                 soma_intervalo(row, 'C167011', 'C167012', col_todas) +
                 soma_intervalo(row, 'C168011', 'C168012', col_todas),
       'qt_mat_fem': row['C167011'] + row['C168011'] + row['C831'] + row['C833'] + row['C7811'] + row['C7813'],
       'qt_mat_masc': row['C167012'] + row['C168012'] + row['C832'] + row['C834'] + row['C7812'] + row['C7814'],
       'qt_mat_diurno': row['C831'] + row['C832'] + row['C7811'] + row['C7812'],
       'qt_mat_noturno': row['C833'] + row['C834'] + row['C7813'] + row['C7814'],
       'qt_mat_0_17':  0,
       'qt_mat_18_24':  0,
       'qt_mat_25_29':  0,
       'qt_mat_30_34':  0,
       'qt_mat_35_39':  0,
       'qt_mat_40_49':  0,
       'qt_mat_50_59':  0,
       'qt_mat_60_mais':  0,
       'qt_mat_branca':  0,
       'qt_mat_preta':  0,
       'qt_mat_parda':  0,
       'qt_mat_amarela':  0,
       'qt_mat_indigena':  0,
       'qt_mat_cornd':  soma_intervalo(row, 'C7811', 'C7814', col_todas) +
                        soma_intervalo(row, 'C0421', 'C0424', col_todas) +
                        soma_intervalo(row, 'C167011', 'C167012', col_todas) +
                        soma_intervalo(row, 'C168011', 'C168012', col_todas),
       'qt_mat_nacbras': soma_intervalo(row, 'C7811', 'C7814', col_todas) +
                         soma_intervalo(row, 'C0421', 'C0424', col_todas) +
                         soma_intervalo(row, 'C167011', 'C167012', col_todas) +
                         soma_intervalo(row, 'C168011', 'C168012', col_todas),
       'qt_mat_nacestrang': 0,
       'qt_mat_deficiente': row['C138098'] + row['C138099'] + row['C138108']+ row['C138099'] +
                            soma_intervalo(row, 'C180011', 'C180101', col_todas),
       'qt_mat_financ': soma_intervalo(row, 'C1511', 'C15121', col_todas),
       'qt_mat_financ_reemb': soma_intervalo(row, 'C1511', 'C1551', col_todas),
       'qt_mat_fies': row['C1511'],
       'qt_mat_rpfies': row['C15101'] + row['C15111'],
       'qt_mat_financ_reemb_outros': soma_intervalo(row, 'C1521', 'C1551', col_todas),
       'qt_mat_financ_nreemb': soma_intervalo(row, 'C1571', 'C1591', col_todas),
       'qt_mat_prounii': row['C1571'],
       'qt_mat_prounip': row['C1581'],
       'qt_mat_nrpfies': 0,
       'qt_mat_financ_nreemb_outros': 0,
       'qt_mat_reserva_vaga': 0,
       'qt_mat_rvredepublica': 0,
       'qt_mat_rvetnico': 0,
       'qt_mat_rvpdef': 0,
       'qt_mat_rvsocial_rf': 0,
       'qt_mat_rvoutros': 0,
       'qt_mat_procescpublica': 0,
       'qt_mat_procescprivada': 0,
       'qt_mat_procnaoinformada': 0,
       'qt_mat_parfor': 0,
       'qt_mat_apoio_social': 0,
       'qt_mat_ativ_extracurricular': 0,
       'qt_mat_mob_academica': 0,
       'qt_conc': soma_intervalo(row, 'C8111', 'C8124', col_todas) +
                  soma_intervalo(row, 'C162011', 'C162022', col_todas) +
                  soma_intervalo(row, 'C165011', 'C165022', col_todas) +
                  soma_intervalo(row, 'C166011', 'C166022', col_todas),
       'qt_conc_fem': soma_intervalo(row, 'C8111', 'C8124', col_impar) +
                      soma_intervalo(row, 'C162011', 'C162022', col_impar) +
                      soma_intervalo(row, 'C165011', 'C165022', col_impar) +
                      soma_intervalo(row, 'C166011', 'C166022', col_impar),
       'qt_conc_masc': soma_intervalo(row, 'C8111', 'C8124', col_par) +
                       soma_intervalo(row, 'C162011', 'C162022', col_par) +
                       soma_intervalo(row, 'C165011', 'C165022', col_par) +
                       soma_intervalo(row, 'C166011', 'C166022', col_par),
       'qt_conc_diurno': row['C8111'] + row['C8112'] + row['C8121'] + row['C8122'],
       'qt_conc_noturno': row['C8113'] + row['C8114'] + row['C8123'] + row['C8124'],
       'qt_conc_0_17': 0,
       'qt_conc_18_24': 0,
       'qt_conc_25_29': 0,
       'qt_conc_30_34': 0,
       'qt_conc_35_39': 0,
       'qt_conc_40_49': 0,
       'qt_conc_50_59': 0,
       'qt_conc_60_mais': 0,
       'qt_conc_branca': 0,
       'qt_conc_preta': row['C138016'] + row['C138017'] + row['C138026'] + row['C138027'],
       'qt_conc_parda': row['C138036'] + row['C138037'] + row['C138046'] + row['C138047'],
       'qt_conc_amarela': 0,
       'qt_conc_indigena': row['C138056'] + row['C138057'] + row['C138066'] + row['C138067'],
       'qt_conc_cornd':  soma_intervalo(row, 'C8111', 'C8124', col_todas) +
                  soma_intervalo(row, 'C162011', 'C162022', col_todas) +
                  soma_intervalo(row, 'C165011', 'C165022', col_todas) +
                  soma_intervalo(row, 'C166011', 'C166022', col_todas),
       'qt_conc_nacbras': soma_intervalo(row, 'C8111', 'C8124', col_todas) +
                          soma_intervalo(row, 'C162011', 'C162022', col_todas) +
                          soma_intervalo(row, 'C165011', 'C165022', col_todas) +
                          soma_intervalo(row, 'C166011', 'C166022', col_todas),
       'qt_conc_nacestrang': 0,
       'qt_conc_deficiente': row['C138096'] + row['C138097'] + row['C138106'] + row['C138107'],
       'qt_conc_financ': 0,
       'qt_conc_financ_reemb': 0,
       'qt_conc_fies': 0,
       'qt_conc_rpfies': 0,
       'qt_conc_financ_reemb_outros': 0,
       'qt_conc_financ_nreemb': 0,
       'qt_conc_prounii': 0,
       'qt_conc_prounip': 0,
       'qt_conc_nrpfies': 0,
       'qt_conc_financ_nreemb_outros': 0,
       'qt_conc_reserva_vaga': 0,
       'qt_conc_rvredepublica': row['C138116'] + row['C138117'] + row['C138126'] + row['C138127'],
       'qt_conc_rvetnico': 0,
       'qt_conc_rvpdef': 0,
       'qt_conc_rvsocial_rf': 0,
       'qt_conc_rvoutros': 0,
       'qt_conc_procescpublica': 0,
       'qt_conc_procescprivada': 0,
       'qt_conc_procnaoinformada': 0,
       'qt_conc_parfor': 0,
       'qt_conc_apoio_social': 0,
       'qt_conc_ativ_extracurricular': 0,
       'qt_conc_mob_academica': 0,
       'qt_sit_trancada': soma_intervalo(row, 'C0621', 'C0634', col_todas) +
                          soma_intervalo(row, 'C14211', 'C14224', col_todas) +
                          trata_lista(row, lista_cols= ['C163011', 'C163012', 'C163013', 'C163014'], operacao=soma),
       'qt_sit_desvinculado': soma_intervalo(row, 'C1011', 'C1018', col_todas) +
                              trata_lista(row, lista_cols= ['C163021', 'C163022', 'C163023', 'C163024'], operacao=soma),
       'qt_sit_transferido': soma_intervalo(row, 'C1021', 'C1024', col_todas) +
                             soma_intervalo(row, 'C1025', 'C1028', col_todas) +
                             soma_intervalo(row, 'C1031', 'C1034', col_todas) +
                             soma_intervalo(row, 'C1035', 'C1038', col_todas) +
                             soma_intervalo(row, 'C163031', 'C163054', col_todas),
       'qt_sit_falecido': 0,
       'qt_parfor': 0,
       'qt_aluno_deficiente': row['C138094'] + row['C138095'] + row['C138104'] + row['C138105'],
       'qt_apoio_social': 0,
       'qt_ativ_extracurricular': 0,
       'qt_mob_academica': 0,
   }
   # Criar uma nova instância de curso_censo com os dados mapeados
   curso_censo.append(dados_curso)
# deleta o dataframe que não precisa mais
del df
# Transformar o resultado em dataframe
censo_df = pd.DataFrame(curso_censo)
# Selecionar todas as colunas que começam com "qt_"
qt_columns = [col for col in censo_df.columns if col.startswith('qt_')]
# Converter essas colunas para o tipo inteiro
censo_df[qt_columns] = censo_df[qt_columns].astype(int)
# Renomeando a coluna criada a partir do índice para 'id'
censo_df.columns.values[0] = 'id'
# descobre o nro do ultimo id
ultimo_id = ultimo_id(Curso_censo)
ultimo_id = ultimo_id[0]
# Resetando o índice para transformar o índice na primeira coluna
df = recria_e_reindexa_dataframe(censo_df, ultimo_id)
# Troca o nome da primeira coluna
# Salvar os dados da ies_censo
if tab_censo == 'S':
    # Determinar o tamanho de cada parte
    n_parts = 5
    size_of_part = len(df) // n_parts
    # Dividir o DataFrame em partes aproximadamente iguais
    dfs_parts = [df.iloc[i * size_of_part: (i + 1) * size_of_part].reset_index(drop=True) for i in range(n_parts)]
    # Exibir os DataFrames separados
    for i, df_part in enumerate(dfs_parts):
        print(f"\nDataFrame parte {i + 1}:")
        salvar_bdados(df_part, Curso_censo, 'id')
    print('Final do Processo')