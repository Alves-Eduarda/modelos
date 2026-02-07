# importando as biliotecas
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from data_understanding.download_data import download_file, return_data

def processing_data() -> pd.DataFrame:

    # Download dos dados
    download_file()

    # Leitura dos dados
    df = return_data('contents/telecom_churn.csv')

# padronização dos dados (apenas nas colunas do tipo float)

    # Identifique suas colunas
    cols_float = ['AccountWeeks','DataUsage', 'CustServCalls', 'DayMins', 'DayCalls', 'MonthlyCharge', 'OverageFee','RoamMins'] # Colunas contínuas
    cols_binarias = ['Churn', 'ContractRenewal','DataPlan'] # Colunas 0 e 1

    # Criar o transformador
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), cols_float)
        ],
        remainder='passthrough' # não altera as colunas binárias
    )

    # Aplicar ao DataFrame
    df_processado = preprocessor.fit_transform(df)

    # 2. Recupera os nomes das colunas na ordem correta
    # O sklearn mantém a ordem: (colunas transformadas + colunas do passthrough)
    colunas_finais = preprocessor.get_feature_names_out()

    colunas_finais = [i.replace('num__','').replace('remainder__','') for i in colunas_finais]

    # 3. Cria o novo DataFrame usando o índice do original
    df_padronizado  = pd.DataFrame(df_processado, columns=colunas_finais, index=df.index)

    return df_padronizado