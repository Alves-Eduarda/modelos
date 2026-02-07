# Previsão de churn em plataforma de streaming

* Link para fonte dos dados: https://www.kaggle.com/api/v1/datasets/download/barun2104/telecom-churn

* Pasta com o dataset: contents

* Pasta com as imagens geradas através das análises: visualization

## Entendimento do Negócio

### Descrição do problema de negócio

O problema de negócio é identificar a parcela de clientes que obtém um perfil propenso a saída/cancelamento do serviço contratado. Analisando os dados, é possível identificar que podemos aplicar um modelo supervisonado utilizando a coluna de churn como nosso rótulo e as demais como features para treinar o algoritmo a identificar os padrões destes perfis. Para uma empresa que busca identificar previamente a saída de clientes de sua base, seria interessante utilizar este modelo para agir através de estratégias de marketing visando reter este perímetro.

### 📊 Dicionário de Dados (Churn Dataset)

| Coluna | Descrição |
| :--- | :--- |
| **churn** | Indicador de cancelamento (1 se o cliente cancelou o serviço, 0 caso contrário). |
| **accountweeks** | Número de semanas que o cliente mantém a conta ativa. |
| **ContractRenewal** | Indica se o cliente renovou o contrato recentemente (1 = Sim, 0 = Não). |
| **DataPlan** | Indica se o cliente possui um plano de dados (1 = Sim, 0 = Não). |
| **DataUsage** | Consumo mensal de dados medido em gigabytes (GB). |
| **CustServCalls** | Número de chamadas feitas para o centro de atendimento ao cliente. |
| **DayMins** | Média de minutos de uso durante o dia por mês. |
| **DayCalls** | Média de chamadas realizadas no período diurno. |
| **MonthlyCharge** | Valor médio da fatura mensal do cliente. |
| **OverageFee** | O valor mais alto de taxa por excesso de uso nos últimos 12 meses. |
| **RoamMins** | Média de minutos gastos em roaming (fora da área de cobertura). |

---------------------------------------------------------------------------------------------------------------------------------------------

## Entendimento dos dados

Para entendimento do negócio foram criadas funções que buscavam identificar como os dados estão distribuídos, quais suas correlações com a variável alvo (Churn) e se existiam valores que deverão ser tratados na etapa de preparação de dados.

* códigos: 
    ** download_data,py
    ** exploratory_data_analysis.py
    ** graphics_eda.py
    ** EDA.ipynb

---------------------------------------------------------------------------------------------------------------------------------------------

## Preparação dos dados

Nesta etapa os dados foram padronizados para seguirem para o processo de modelagem.

* códigos
    ** preparation_data.py
    ** graphics_prep_data.py
    ** Preparation_data.ipynb

---------------------------------------------------------------------------------------------------------------------------------------------

## Modelagem

Os modelos aplicados para resolução deste problema foram : Random Forest, XGboost. Ambos modelos de classificação, considerando que nossa variável alvo obtém duas classes : Usuários com Churn (1) e Uusários sem Churn (0).

* códidos:
    ** train.py

---------------------------------------------------------------------------------------------------------------------------------------------

## Avaliação

Nesta etapa buscamos analisar a eficiência do modelo com melhor desempenho. 

* códigos
    ** evaluation.py

---------------------------------------------------------------------------------------------------------------------------------------------
