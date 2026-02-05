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
O problema de negócio é identificar a parcela de clientes que obtém um perfil propenso a saída/cancelamento do serviço contratado. Analisando os dados, é possível identificar que podemos aplicar um modelo supervisonado utilizando a coluna de churn como nosso rótulo e as demais como features para treinar o algoritmo a identificar os padrões destes perfis.

Para uma empresa que busca identificar previamente a saída de clientes de sua base, seria interessante utilizar este modelo para agir através de estratégias de marketing visando reter este perímetro.