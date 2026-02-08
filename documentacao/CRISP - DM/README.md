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

    - download_data,py
    - exploratory_data_analysis.py
    - graphics_eda.py
    - EDA.ipynb

---------------------------------------------------------------------------------------------------------------------------------------------

## Preparação dos dados

Nesta etapa os dados foram padronizados para seguirem para o processo de modelagem.

    - preparation_data.py
    - graphics_prep_data.py
    - Preparation_data.ipynb

---------------------------------------------------------------------------------------------------------------------------------------------

## Modelagem

Os modelos aplicados para resolução deste problema foram : XGboost (com e sem feature importance) e Regressão Logística. Ambos modelos de classificação, considerando que nossa variável alvo obtém duas classes : Usuários com Churn (1) e Uusários sem Churn (0). Para o treinamento também foi aplicada uma técnica de oversampling para balancear os dados evitando viés e overfitting.

    - train.py

---------------------------------------------------------------------------------------------------------------------------------------------

## Avaliação

Nesta etapa buscamos analisar a eficiência do modelo com melhor desempenho. 

    - evaluation.py

Tivemos os seguintes resultados para os modelos: 

📊 Avaliação dos Modelos

🔹 Métricas Globais

| Modelo                          | ROC AUC | PR AUC | Acurácia |
|---------------------------------|--------:|-------:|---------:|
| Logistic Regression             | 0,8344  | 0,4825 | 77,66%   |
| XGBoost (sem Feature Importance)| 0,8988  | 0,8041 | 92,80%   |
| XGBoost (com Feature Importance)| 0,8977  | 0,7598 | 91,15%   |

---

🔹 Logistic Regression — Métricas por Classe

| Classe | Precision | Recall | F1-score | Suporte |
|-------:|----------:|-------:|---------:|--------:|
| 0 (Não Churn) | 0,9566 | 0,7737 | 0,8555 | 570 |
| 1 (Churn)     | 0,3738 | 0,7938 | 0,5083 | 97  |

| Métrica | Valor |
|--------|-------:|
| Acurácia | 77,66% |
| Macro Avg F1 | 0,6819 |
| Weighted Avg F1 | 0,8050 |

---

🔹 XGBoost (sem Feature Importance) — Métricas por Classe

| Classe | Precision | Recall | F1-score | Suporte |
|-------:|----------:|-------:|---------:|--------:|
| 0 (Não Churn) | 0,9531 | 0,9632 | 0,9581 | 570 |
| 1 (Churn)     | 0,7692 | 0,7216 | 0,7447 | 97  |

| Métrica | Valor |
|--------|-------:|
| Acurácia | 92,80% |
| Macro Avg F1 | 0,8514 |
| Weighted Avg F1 | 0,9271 |

---

🔹 XGBoost (com Feature Importance) — Métricas por Classe

| Classe | Precision | Recall | F1-score | Suporte |
|-------:|----------:|-------:|---------:|--------:|
| 0 (Não Churn) | 0,9459 | 0,9509 | 0,9484 | 570 |
| 1 (Churn)     | 0,7021 | 0,6804 | 0,6911 | 97  |

| Métrica | Valor |
|--------|-------:|
| Acurácia | 91,15% |
| Macro Avg F1 | 0,8197 |
| Weighted Avg F1 | 0,9110 |


**A partir do modelo com melhor desempenho,Xgboost sem a aplicação da feature importance, foi criada uma análise em relação a faixa de risco do churn. Segue o resultado obtido:**

📈 Resultado por Faixa de Risco

| Faixa de Risco | Número de Clientes | Taxa de Churn |
|---------------|-------------------|---------------|
| Baixo         | 220               | 3,64%         |
| Médio         | 220               | 1,82%         |
| Alto          | 227               | 37,44%        |

Este resultado nos indica que o modelo consegue identificar bem a parcela do churn para aqueles como risco alto. Então, numa ação de retenção conseguiríamos atingir uma boa parcela. Contudo, considerando a faixa baixa e média ele não consegue distinguir muito bem os dois grupos.

---------------------------------------------------------------------------------------------------------------------------------------------
