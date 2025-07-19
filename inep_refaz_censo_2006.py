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

ano = 2006
tab_aread = 'N'
tab_areae = 'N'
tab_curso = 'N'
tab_rotulo = 'N'
tab_censo =  'N'
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
    6:4,
    7:5
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
# Renomear o nome das tabelas
if ano == 2004:
    df = df.rename(columns={'NOMEAREAESPECIFIC': 'NOMEAREAESPECIFICA', 'CATADMCOMUM': 'CATADMCOMUN'})
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
curso_df = df[['CURSO', 'NOMEDOCURSO', 'CODAREADETALHADA']].drop_duplicates()
cursoe_df = curso_df[['CURSO']].drop_duplicates()
# Recuperar as areas detalhadas dos dados do curso
sql = 'select * from curso order by 1'
df_aux = carregar_dataframe(sql)
#  Identificar quais registros de cursoe_df não estão em df_aux
curso_nao_exist = cursoe_df[~cursoe_df['CURSO'].isin(df_aux['codigo'])]
# Unir os dados das áreas ao dataframe original
curso_nao_exist = curso_nao_exist.merge(curso_df, how='left', left_on='CURSO', right_on='CURSO')
# renomear para o nome das colunas da tabela no banco
curso_nao_exist = curso_nao_exist.rename(columns={'CURSO': 'codigo', 'NOMEDOCURSO': 'nome', 'CODAREADETALHADA': 'area_detalhada'})
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
df.rename(columns={'CODMUNICCURSO': 'municipio'}, inplace=True)
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
# Filtra as linhas onde a coluna 'TP_REDE' possui valores nulos
df['tp_rede'] = df['categoria'].apply(lambda x: 1 if x < 4 else 2)
# Criando a coluna IN_GRATUITA com base na condição de TP_REDE
df['in_gratuito'] = df['tp_rede'].apply(lambda x: True if x == 1 else False)

df['dimensao'] = 1
df.loc[df['MOD_DISTANCIA'] == 'S', 'dimensao'] = 2

# Modalidade de ensino
df['tp_modalidade_ensino'] = 1
df.loc[df['MOD_DISTANCIA'] == 'S', 'tp_modalidade_ensino'] = 2
# Nivel academico
df['tp_nivel_academico'] = 2
df.loc[df['NIVELCURSO'] == 'GRADUACAO', 'tp_nivel_academico'] = 2

# Organicação acad
antes_org = df.groupby('ORDEMORGACAD').size().reset_index(name='qtde_registros')
df['ORDEMORGACAD'] = df['ORDEMORGACAD'].replace(de_para_org)
df.rename(columns={'ORDEMORGACAD': 'org_academica'}, inplace=True)
depois_org = df.groupby('org_academica').size().reset_index(name='qtde_registros')

# Tratar a região
df.loc[df['REGIAO'] == 'Sul', 'regiao'] = 4
df.loc[df['REGIAO'] == 'Sudeste', 'regiao'] = 3
df.loc[df['REGIAO'] == 'Nordeste', 'regiao'] = 2
df.loc[df['REGIAO'] == 'Norte', 'regiao'] = 1
df.loc[df['REGIAO'] == 'Centro-Oeste', 'regiao'] = 5

# Trocar o nome de algumas colunas
df.rename(columns={'ANO': 'ano_censo'}, inplace=True)
df.rename(columns={'IES': 'ies'}, inplace=True)
df.rename(columns={'CURSO': 'curso'}, inplace=True)
df.rename(columns={'CO_CINE_ROTULO': 'cine_rotulo'}, inplace=True)
df.rename(columns={'CODAREAGERAL': 'area_geral'}, inplace=True)
df.rename(columns={'CODAREAESPECIFICA': 'area_especifica'}, inplace=True)
df.rename(columns={'CODAREADETALHADA': 'area_detalhada'}, inplace=True)
# deletar algumas colunas que não são mais necessárias
df.drop(columns=['CODMUNIC', 'MUNICIPIO', 'EH_CAPITAL', 'COD_UF', 'NOME_UF', 'NOMEORGACAD'], inplace=True)
df.drop(columns=['NOMEDOCURSO', 'REGIAO', 'DTINIFUNCCURSO', 'NIVELCURSO', 'SUBNIVEL', 'MOD_PRESENC', 'MOD_DISTANCIA'], inplace=True)
df.drop(columns=['EH_BACHARELADO', 'EH_LICENCPLENA', 'EH_LICCURTA', 'EH_TECNO', 'EH_ESPECPROF'], inplace=True)
df.drop(columns=['NOMEAREACURSO', 'NOMEAREAGERAL', 'NOMEAREAESPECIFICA', 'NOMEAREADETALHADA', 'CATEGADM', 'COD_DEP'],  inplace=True)
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
       'qt_vg_total': soma_intervalo(row, 'C62011', 'C6620', col_todas) +
                      trata_lista(row, lista_cols = ['C84011', 'C84021', 'C84031', 'C84041', 'C84051', 'C08471'], operacao=soma),
       'qt_vg_total_diurno': soma_intervalo(row, 'C62011', 'C6620', col_impar),
       'qt_vg_total_noturno': soma_intervalo(row, 'C62011', 'C6620', col_par),
       'qt_vg_total_ead': trata_lista(row, lista_cols = ['C84011', 'C84021', 'C84031', 'C84041', 'C84051', 'C08471'], operacao=soma),
       'qt_vg_nova': 0,
       'qt_vg_proc_seletivo': trata_lista(row, lista_cols = ['C62011', 'C62012', 'C62041', 'C62042', 'C62061', 'C62062', 'C62091', 'C62092', 'C63011', 'C63012',
                                                             'C63041', 'C63042',  'C63061', 'C63062', 'C63091', 'C63092', 'C6401', 'C6402', 'C6407', 'C6408',
                                                             'C6411', 'C6412', 'C6417', 'C6418', 'C6501', 'C6502', 'C6507', 'C6508',  'C6511', 'C6512', 'C6517',
                                                             'C6518', 'C6601', 'C6602', 'C6607', 'C6608',  'C6611', 'C6612', 'C6617', 'C6618'], operacao=soma) +
                              trata_lista(row, lista_cols = ['C84011', 'C84031', 'C84041', 'C84051', 'C08471'], operacao=soma),
       'qt_vg_remanesc': 0,
       'qt_vg_prog_especial': row['C138101'] + row['C138111'] + row['C138121'] + row['C138131'] + row['C138141'],
       'qt_inscrito_total': soma_intervalo(row, 'C67011', 'C7160', col_todas) +
                            soma_intervalo(row, 'C84014', 'C84015', col_todas) +
                            soma_intervalo(row, 'C84024', 'C84025', col_todas) +
                            soma_intervalo(row, 'C84034', 'C84035', col_todas) +
                            soma_intervalo(row, 'C84044', 'C84045', col_todas) +
                            soma_intervalo(row, 'C84054', 'C84065', col_todas),
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
       'qt_inscrito_total_ead': trata_lista(row, lista_cols = ['C84014', 'C84025'], operacao=soma),
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
                 soma_intervalo(row, 'C19011', 'C19222', col_todas),
       'qt_ing_fem': soma_intervalo(row, 'C72011', 'C7640', col_impar) +
                     soma_intervalo(row, 'C19011', 'C19222', col_impar),
       'qt_ing_masc': soma_intervalo(row, 'C72011', 'C7640', col_par) +
                     soma_intervalo(row, 'C19011', 'C19222', col_par),
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
                            soma_intervalo(row, 'C84072', 'C84075', col_todas),
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
                      trata_lista(row, lista_cols= ['C84084', 'C84085'], operacao=soma),
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
                                    trata_lista(row, lista_cols= ['C84092', 'C84093'], operacao=soma),
       'qt_ing_selecao_simplifica':  0,
       'qt_ing_egr': soma_intervalo(row, 'C03021', 'C03024', col_todas) +
                     soma_intervalo(row, 'C03011', 'C03014', col_todas) +
                     soma_intervalo(row, 'C7729', 'C7732', col_todas) +
                     soma_intervalo(row, 'C7701', 'C7704', col_todas),
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
                                    trata_lista(row, lista_cols= ['C84124', 'C84125'], operacao=soma),
       'qt_ing_proc_seletivo':  0,
       'qt_ing_vg_remanesc':  0,
       'qt_ing_vg_prog_especial':  0,
       'qt_ing_outra_forma':  0,
       'qt_ing_0_17': row['C09011'] + row['C09012'] + row['C09121'] + row['C09122'] + row['C19011'] + row['C19012'] + row['C19121'] + row['C19122'],
       'qt_ing_18_24': row['C09021'] + row['C09022'] + row['C09131'] + row['C09132'] + row['C19021'] + row['C19022'] + row['C19131'] + row['C19132'],
       'qt_ing_25_29': row['C09031'] + row['C09032'] + row['C09141'] + row['C09142'] + row['C19031'] + row['C19032'] + row['C19141'] + row['C19142'],
       'qt_ing_30_34': row['C09041'] + row['C09042'] + row['C09151'] + row['C09152'] + row['C19041'] + row['C19042'] + row['C19151'] + row['C19152'],
       'qt_ing_35_39': row['C09051'] + row['C09052'] + row['C09161'] + row['C09162'] + row['C19051'] + row['C19052'] + row['C19161'] + row['C19162'],
       'qt_ing_40_49': row['C09061'] + row['C09062'] + row['C09071'] + row['C09072'] + row['C09171'] + row['C09172'] + row['C09181'] + row['C09182'] +
                       row['C19061'] + row['C19062'] + row['C19171'] + row['C19172'] + row['C19071'] + row['C19072'] + row['C19181'] + row['C19182'],
       'qt_ing_50_59': row['C09081'] + row['C09082'] + row['C09091'] + row['C09092'] + row['C09191'] + row['C09192'] + row['C09201'] + row['C09202'] +
                       row['C19081'] + row['C19082'] + row['C19191'] + row['C19192'] + row['C19091'] + row['C19092'] + row['C19201'] + row['C19201'],
       'qt_ing_60_mais': row['C09101'] + row['C09102'] + row['C09111'] + row['C09112'] + row['C09211'] + row['C09212'] + row['C09221'] + row['C09222'] +
                         row['C19101'] + row['C19102'] + row['C19211'] + row['C19212'] + row['C19111'] + row['C19112'] + row['C19221'] + row['C19222'],
       'qt_ing_branca': 0,
       'qt_ing_preta': row['C138014'] + row['C138015'] + row['C138024'] + row['C138025'],
       'qt_ing_parda': row['C138034'] + row['C138035'] + row['C138044'] + row['C138045'],
       'qt_ing_amarela': 0,
       'qt_ing_indigena': row['C138054'] + row['C138055'] + row['C138064'] + row['C138065'],
       'qt_ing_cornd': soma_intervalo(row, 'C72011', 'C7640', col_todas) +
                       soma_intervalo(row, 'C19011', 'C19222', col_todas),
       'qt_ing_mob_academica': soma_intervalo(row, 'C03011', 'C03054', col_todas),
       'qt_ing_nacbras': soma_intervalo(row, 'C72011', 'C7640', col_todas) +
                         soma_intervalo(row, 'C19011', 'C19222', col_todas),
       'qt_ing_nacestrang': 0,
       'qt_ing_financ': soma_intervalo(row, 'C1511', 'C1551', col_todas),
       'qt_ing_financ_reemb': soma_intervalo(row, 'C1511', 'C1551', col_todas),
       'qt_ing_fies': row['C1511'],
       'qt_ing_rpfies': 0,
       'qt_ing_financ_reemb_outros': soma_intervalo(row, 'C1521', 'C1521', col_todas),
       'qt_ing_financ_nreemb': soma_intervalo(row, 'C1561', 'C1541', col_todas),
       'qt_ing_prounii': 0,
       'qt_ing_prounip': 0,
       'qt_ing_nrpfies': 0,
       'qt_ing_financ_nreemb_outros': row['C1551'],
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
       'qt_ing_apoio_social': 0,
       'qt_mat': soma_intervalo(row, 'C7811', 'C7814', col_todas) +
                 soma_intervalo(row, 'C0421', 'C0424', col_todas) +
                 soma_intervalo(row, 'C2011', 'C2012', col_todas) +
                 soma_intervalo(row, 'C2021', 'C2022', col_todas),
       'qt_mat_fem': row['C2011'] + row['C2021'] + row['C831'] + row['C833'] + row['C7811'] + row['C7813'],
       'qt_mat_masc': row['C2012'] + row['C2022'] + row['C832'] + row['C834'] + row['C7812'] + row['C7814'],
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
                        soma_intervalo(row, 'C2011', 'C2012', col_todas) +
                        soma_intervalo(row, 'C2021', 'C2022', col_todas),
       'qt_mat_nacbras': soma_intervalo(row, 'C7811', 'C7814', col_todas) +
                         soma_intervalo(row, 'C0421', 'C0424', col_todas) +
                         soma_intervalo(row, 'C2011', 'C2012', col_todas) +
                         soma_intervalo(row, 'C2021', 'C2022', col_todas),
       'qt_mat_nacestrang': 0,
       'qt_mat_deficiente': 0,
       'qt_mat_financ': soma_intervalo(row, 'C1511', 'C1551', col_todas),
       'qt_mat_financ_reemb': soma_intervalo(row, 'C1511', 'C1541', col_todas),
       'qt_mat_fies': row['C1511'],
       'qt_mat_rpfies': 0,
       'qt_mat_financ_reemb_outros': soma_intervalo(row, 'C1521', 'C1551', col_todas),
       'qt_mat_financ_nreemb': soma_intervalo(row, 'C1521', 'C1561', col_todas),
       'qt_mat_prounii': 0,
       'qt_mat_prounip': 0,
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
                  soma_intervalo(row, 'C2211', 'C2222', col_todas) +
                  soma_intervalo(row, 'C231', 'C234', col_todas),
       'qt_conc_fem': soma_intervalo(row, 'C8111', 'C8124', col_impar) +
                      soma_intervalo(row, 'C2211', 'C2222', col_impar) +
                      soma_intervalo(row,  'C231', 'C234', col_impar),
       'qt_conc_masc': soma_intervalo(row, 'C8111', 'C8124', col_par) +
                       soma_intervalo(row, 'C2211', 'C2222', col_par) +
                       soma_intervalo(row,  'C231', 'C234', col_par),
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
                         soma_intervalo(row, 'C2211', 'C2222', col_todas) +
                         soma_intervalo(row, 'C231', 'C234', col_todas),
       'qt_conc_nacbras': soma_intervalo(row, 'C8111', 'C8124', col_todas) +
                          soma_intervalo(row, 'C2211', 'C2222', col_todas) +
                          soma_intervalo(row, 'C231', 'C234', col_todas),
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
                          trata_lista(row, lista_cols= ['C2111', 'C2112', 'C2113', 'C2114'], operacao=soma),
       'qt_sit_desvinculado': soma_intervalo(row, 'C1011', 'C1018', col_todas) +
                              trata_lista(row, lista_cols= ['C2121', 'C2122', 'C2123', 'C2124'], operacao=soma),
       'qt_sit_transferido': soma_intervalo(row, 'C1021', 'C1024', col_todas) +
                             soma_intervalo(row, 'C1025', 'C1028', col_todas) +
                             soma_intervalo(row, 'C1031', 'C1034', col_todas) +
                             soma_intervalo(row, 'C1035', 'C1038', col_todas) +
                             soma_intervalo(row, 'C2131', 'C2142', col_todas) +
                             soma_intervalo(row, 'C2133', 'C2144', col_todas),
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