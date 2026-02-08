# importando os bibliotecas
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
from imblearn.over_sampling import RandomOverSampler

# Separando os dados em treino, teste e validação

# separação do conjunto de treino, validação e teste

def data_train(df: pd.DataFrame):

    X, y = df.drop('Churn',axis=1), df['Churn'] # separando as features e o target

    # treino e teste
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    #X_temp, X_test, y_temp, y_test -> vão pegar o dado original e separar em 80% pra treino e 20% pra teste

    # treino e validação
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.25, stratify=y_temp, random_state=42
    )

    return X_temp, X_test, X_train, X_val, y_temp, y_test, y_train, y_val

    # A partir dos dados originais separados para treino vamos criar o conjunto de validação. Ou seja, dos 80% separado
    # para treino, vamos separá-lo em 75% para treino e 25% para validação.


# Aplicando o método de aumentar as amostras dos dados, mediante o desbalanceamento da classe de Churn
# vamos utilizar uma técnica de oversampling para separarmos as variáveis de treino e teste de forma balanceada
def balanced_data(X,y):
    ros = RandomOverSampler(random_state=42)
    X_resampled, y_resampled = ros.fit_resample(X, y)

    return X_resampled, y_resampled


def xgboost_aplication(df: pd.DataFrame):

    X_temp, X_test, X_train, X_val, y_temp, y_test, y_train, y_val = data_train(df)

    X_resampled, y_resampled = balanced_data(X_train, y_train)

    # Aplicando o modelo XGBOOST

    # Modelo com todas variáveis
    xgboost_model = XGBClassifier(
        scale_pos_weight=1, 
        eval_metric='logloss'
    )

    # treinando o modelo
    xgboost_model.fit(X_resampled, y_resampled)

     # Aplicando o modelo XGboost com feature importante
    importances = xgboost_model.feature_importances_

    df_importances = pd.DataFrame({
        'feature': X_resampled.columns,
        'importance': importances
    }).sort_values(by='importance', ascending=False)

    # colunas com feature importance acima de 0.05
    target = 'Churn'

    features_selecionadas = df_importances.loc[
    df_importances['importance'] > 0.05, 'feature'
    ].tolist()

    # adiciona a variável alvo
    feature_importance_to_test = features_selecionadas + [target]


    return xgboost_model, X_val, y_val, feature_importance_to_test

def xgboost_aplication_with_feature_importance(df: pd.DataFrame):

    X_temp_fi, X_test_fi, X_train_fi, X_val_fi, y_temp_fi, y_test_fi, y_train_fi, y_val_fi = data_train(df)

    # balanceando os dados
    X_resampled_fi, y_resampled_fi = balanced_data(X_train_fi, y_train_fi)

    xgboost_model_fi = XGBClassifier(
        scale_pos_weight=1,
        eval_metric='logloss'
    )

    # aplicando o modelo
    xgboost_model_fi.fit(X_resampled_fi, y_resampled_fi)

    return xgboost_model_fi, X_val_fi, y_val_fi

def logistc_regression_aplication(df: pd.DataFrame):
    # Aplicando o modelo Regressão Logística

    lr_model = LogisticRegression(max_iter=1000)

    X_temp, X_test, X_train, X_val, y_temp, y_test, y_train, y_val = data_train(df)

    X_resampled, y_resampled = balanced_data(X_train, y_train)

    # treinando o modelo
    lr_model.fit(X_resampled, y_resampled)

    return lr_model, X_val, y_val



