Local do painel de estatísticas do INEP
https://app.powerbi.com/view?r=eyJrIjoiMGJiMmNiNTAtOTY1OC00ZjUzLTg2OGUtMjAzYzNiYTA5YjliIiwidCI6IjI2ZjczODk3LWM4YWMtNGIxZS05NzhmLWVhNGMwNzc0MzRiZiJ9&pageName=ReportSection4036c90b8a27b5f58f54

Baixados os arquivos do INEP em https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-da-educacao-superior e https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/sinopses-estatisticas/educacao-superior-graduacao

Criado a pasta de trabalho e separado por pasta os dados
d:\Trab\Inep\AAnalisar (Dados brutos, baixados do site)
d:\Trab\Inep\Anexos  (Para anexos baixados dos dados principais)
d:\Trab\Inep\Sinopses  (Para os arquivos das SINOPSE)
Salvado os arquivos de Sinopse com o nome SinopesAAAA.xlsx onde AAAA é o ano de referência do arquivo (a aplicação irá gerar no banco de dados que a informação é deste ano) e movido estes para a pasta c:\trab\inep\sinopse

d:\Trab\Inep\Microdados (Para os arquivos de microdados)
d:\Trab\Inep\Microdados\censo (Dados dos censos anuais)
d:\Trab\Inep\Microdados\Dicionario (dicionário de dados dos arquivos de microdados)
d:\Trab\Inep\Microdadosz\ies  (cadastro das IES)

Extraído os arquivos de cada ano e:
- Salvado os arquivos de microdados com o conteúdo das IFES com o nome IES_AAAA.csv onde AAAA é o ano de referência do arquivo (a aplicação irá gerar no banco de dados que a informação é deste ano) e movido estes para a pasta c:\trab\inep\microdados\ies
- Salvado os arquivos de microdados com o conteúdo do dicionário de dados do arquivo que contém as IFES com o nome dic_ies_AAAA.xlsx onde AAAA é o ano de referência do arquivo (a aplicação irá gerar no banco de dados que a informação é deste ano) e movido estes para a pasta c:\trab\inep\microdados\dicionario
- Salvado os arquivos de microdados com o conteúdo dos cursos com o nome Censo_AAAA.xlsx onde AAAA é o ano de referência do arquivo (a aplicação irá gerar no banco de dados que a informação é deste ano) e movido estes para a pasta c:\trab\inep\microdados\censo
- Salvado os arquivos de microdados com o conteúdo do dicionário de dados do arquivo de cursos com o nome dic_censo_AAAA.xlsx onde AAAA é o ano de referência do arquivo (a aplicação irá gerar no banco de dados que a informação é deste ano) e movido estes para a pasta c:\trab\inep\microdados\censo

Rodado a rotina criar_dicionario_apartir_planilha.py para criar os arquivos dic_ies.xlsx com diferença do dicionário de dados entre os anos da base do IES e dic_censo.xslx para os anos da base do censo

