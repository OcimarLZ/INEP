Abordagem

Acessar as planilhas do INEP sobre a Educação Superior. Foram baixados as SINOPSE e o Microdados de 1995 até 2022.

Após isto, está sendo feita uma análise inicial para identificar que informações estão disponíveis e a versão a cada ano das informqações, pois com o decorrer do tempo, maiores detalhes estão disponíveis.

A pesquisa se limitará aos dados de 2014 a 2024 e apenas os dados referente ao município de Chapecó.

Na análise inicial dos dados, alguns problemas foram apurados:
a) Ainda não há dados de 2023 e 2024, o que serão publicados durante o desenrolar da pesquisa.
b) Constatado a inviabilidade da pesquisa a partir dos dados da SINOPSE, pois até 2020, os dados não chegam na granularidade de municipio, separados os dados apenas das capitais e do interior.
c) Nos dados de SINOPSE, há variação a cada ano, mas com 2 diferentes formatos, muito incompatíveis entre si, o que dificulta a pesquisa. Como citei anteriormente, de 1995 até 2020 os dados são num formato e de 2021 muda para um novo formato, que permite um maior detalhamento.   
d) Portanto, dados de 2014 até 2020, precisam ser extraídos das planilhas de microdados. Nestes dados, recuperados dados entre 1995 e 2022, denota grande mudança nos dados a cada ano, o que reflete na diferença entre as planilhas. Como são mais de 300 informações, identificar o que mudou a cada ano é algo complexo, principalmente, informação que tenha derivado para 2 ou mais informações durante o processo ou duas ou mais informações que foram aglutinadas numa só.

Diante da dificuldade e do foco da pesquisa, ao menos 7 anos precisam ser retirados das planilhas de microdados, portanto, o uso da SINOPSE fica comprometida ou ao menos precisa ser complementada.

Dicidido então pela seguinte abordagem inicialmente.
a) Criar uma solução em linguagem Python utilizando práticas de Ciência de Dados para auxiliar na interpretação (auxiliar no entendimento do que se tem dos dados disponíveis no INEP), validação e transformação destes dados em banco de dados de forma estruturada e compreensível
b) Para isto, foram criadas rotinas para a criação de um dicionário de dados do que contém cada planilha e para a tarefa de entendimento do que é cada um dos dados
c) Deverá a seguir ser criado o banco de dados estruturado a partir destas planilhas do INEP
d) Como parte do trabalho, deverão ser elencadas as informações pertinentes para a pesquisa e a granularidade que serão necessárias
e) A partir das informações elencadas para a pesquisa, deverá ser construído um Datamart (um banco de dados específico para a pesquisa) para o mesmo ser fonte das análises necessárias para o desenvolvimento do projeto 
f) Conforme surgirem as demandas por dados e/ou informações, ferramantas de Business Intelligence (BI), de SQL (Linguagem Estruturada de Consulta) e de Ciência de Dados serão utilizadas para pesquisar, simular e produzir dados e informações, sejam em textos ou gráficos
g) Os artefatos produzidos contendo informações sobre os dados da pesquisa, sofrerão a aplicação dos métodos de pesquisa para compreender fenómenos, tendências e questionamentos.





Local do painel de estatísticas do INEP
https://app.powerbi.com/view?r=eyJrIjoiMGJiMmNiNTAtOTY1OC00ZjUzLTg2OGUtMjAzYzNiYTA5YjliIiwidCI6IjI2ZjczODk3LWM4YWMtNGIxZS05NzhmLWVhNGMwNzc0MzRiZiJ9&pageName=ReportSection4036c90b8a27b5f58f54



Objetivos:
1. Obter os dados necessários:
   2. Sinopse: 2021 e 2022, os dados estão mais completos
   3. De 1995 a 
 