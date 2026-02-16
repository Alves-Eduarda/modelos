# Análise do histórico de Sinistro de Trânsito no Brasil \[ 2007 - 2025 ]

## Entendimento do negócio

Este projeto visa prever a quantidade de sinistro nas rodovias do Brasil baseados no dados levantados pela Polícia Rodoviária Federal desde 01/01/2007. 
Este estudo pode nos ajudar a identificar quais rodovias apresentam quantidades excessivas de sinistro para atuar preventivamente e evitar que tais casos ocorram através de ações de educação populacional sobre os riscos da direção de automóveis em rodovias.

### 📊 Dicionário de Dados

|Coluna|Tipo|Descrição|+
|-|-|-|
|id|inteiro|Identificador único do registro do acidente|
|data\_inversa|string (data)|Data do acidente no formato DD/MM/AAAA|
|dia\_semana|string|Dia da semana em que ocorreu o acidente|
|horario|string (hora)|Horário do acidente|
|uf|string|Unidade Federativa onde ocorreu o acidente|
|br|string|Rodovia federal (BR)|
|km|string|Quilômetro da rodovia onde ocorreu o acidente|
|municipio|string|Município do local do acidente|
|causa\_acidente|string|Causa principal do acidente|
|tipo\_acidente|string|Tipo do acidente (ex: colisão, capotamento)|
|classificacao\_acidente|string|Classificação do acidente quanto à gravidade|
|fase\_dia|string|Fase do dia (ex: dia, noite, amanhecer)|
|sentido\_via|string|Sentido da via no momento do acidente|
|condicao\_metereologica|string|Condição meteorológica no momento do acidente|
|tipo\_pista|string|Tipo de pista (simples, dupla, etc.)|
|tracado\_via|string|Traçado da via (reta, curva, etc.)|
|uso\_solo|string|Uso do solo no local (urbano ou rural)|
|ano|inteiro|Ano de ocorrência do acidente|
|pessoas|inteiro|Número total de pessoas envolvidas|
|mortos|inteiro|Número de vítimas fatais|
|feridos\_leves|inteiro|Número de feridos leves|
|feridos\_graves|inteiro|Número de feridos graves|
|ilesos|inteiro|Número de pessoas sem ferimentos|
|ignorados|inteiro|Número de pessoas com estado ignorado|
|feridos|inteiro|Total de pessoas feridas|
|veiculos|inteiro|Número de veículos envolvidos|

## Entendimento dos dados

Os dados podem ser baixados através do portal de dados abertos do Governo Federal. Cada base fica disponível em uma pasta compactada (.zip). Abaixo segue as informações para quem deseja fazer o download das informações:

Fonte: https://dados.gov.br/dados/conjuntos-dados/sinistros-de-transito-agrupados-por-ocorrencia
E-mail da área técnica: direx@prf.gov.br

Arquivos: 

1. Cada extração dos anos está localizada na pasta arquivos_descompactados
2. O arquivo *historico_datatran.csv* é o resultado da junção dos arquivos da pasta arquivos_descompactados
3. Os arquivos *municipio_tse_ibge.csv e leiame- municipio_tse_ibge.pdf* contém os dados referentes aos códigos de IBGE para UF e MUNICÍPIO 
4. O arquivo *lista_municipios_sem_correspondencia.xlsx* contém os municípios e seus códigos ao qual não obteram correspondência com a base do histórico de sinistros

Códigos utilizados:

- eda.py
- unzip_files.py

Através dos dados, vamos buscar prever a quantidade de feridos nos sinistros das rodovias brasileiras. Após conseguirmos prever, será aplicado uma série temporal a partir da agregação de mês. A ideia é tentar responder a seguinte pergunta: 

**Conseguimos prever a quantidade de feridos a partir do histórico para o 1º semestre do ano de 2026?**

Para isso foram exploradas as seguintes análises:

1. Qual é o cenário pós implementação da Lei seca (2008) de feridos e mortos nas rodovias federais

![Total de mortes e feridos por ano provocadas pelo motivo de álcool](visualization/total_de_mortes_feridos_por_ano_causa_alcool.png)

2. Principais ufs, brs e municípios com maior quantidade de número de mortos

**UF**

- Considerando todo o histórico dos anos de 2007 até 2025

![Histórico de mortes por UFs - 2007 até 2025](visualization/total_de_mortes_por_uf_tds_anos.png)

- Considerando apenas o ano de 2025

![Ufs com maior quantidade de mortes em 2025](visualization/total_de_mortes_por_uf_2025.png)

**brs**

![Top 15 brs com maior volume de mortes](visualization/total_de_mortes_por_brs.png)

**Municípios**

- Considerando todo o histórico dos anos de 2007 até 2025

![TOP 10 municípios com maior volume de mortes](visualization/total_de_mortes_por_municipio.png)

- Considerando apenas o ano de 2025

![TOP 10 municípios com maior volume de mortes em 2025](visualization/total_de_mortes_por_municipio_2025.png)

3. Quantidade de feridos num período de meses, anos e horário

- meses 

![Volume de feridos por mês](visualization/feridos_por_mes.png)

- horário

![Volume de feridos e mortes por horário](visualizationtotal_de_mortes_feridos_por_horario.png)


4. Quais as principais causas de acidentes através da nuvem de palavras

![Nuvem de palavras - principais causas de acidentes](nuvem_de_palavras.png)

5. Quais são os dias da semana com maior quantidade de feridos

![Volume de feridos por dia de semana](total_de_mortes_por_dia_da_semana.png)

6. Análise da permanência dos outliers (números acima da média devido aos desastres nas rodovias)

Foram encontradas reportagens que comprovam os acidentes com número de pessoas acima de 100. Sendo assim, foi escolhido a permanência dos casos para serem considerados no treinamento do modelo.

## Preparação dos dados

1. Criação de colunas a partir da data_inversa: data, meses, ano
2. Ajuste nas padronizações dos valores categóricos para numéricos: latitude, longitude, br, km
3. Remoção de colunas que não estão presentes no histórico: regional, delegacia, uop, latitude e longitude
4. Padronização dos valores categóricos: fase_dia, condicao_metereologica
5. Remoção das colunas que causam vazamento de informações
6. Transformação das colunas categóricas em numéricas

Códigos utilizados:

- data_prep.py
- preparation_final_data.py

## Modelagem

Aplicação dos modelos para regressão: 

- GradientBoosting
- Random Forest
- Decision Tree

Código com os modelos:

- train.py

## Avaliação dos modelos

- evaluation_code.py

## Visualização dos gráficos

- vizualization (pasta)

# Código principal 

- main.py

*visualização dos resultados* : saida_treinamento_validacao.txt