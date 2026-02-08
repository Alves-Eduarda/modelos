# importando as bibliotecas
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)
import pandas as pd


def evaluate_model(model, X_val, y_val, nome):

    y_prob = model.predict_proba(X_val)[:,1]
    y_pred = (y_prob >= 0.5).astype(int)

    print(f'\n {nome}')
    print('ROC AUC:', roc_auc_score(y_val, y_prob))
    print('PR AUC:', average_precision_score(y_val, y_prob))
    print(classification_report(y_val, y_pred, digits=4))


def range_test_risk_churn(model, X, y):

    y_val_prob = model.predict_proba(X)[:, 1] # selecionando no array da probabilidade apenas os casos com churn

    df_val = X.copy()
    df_val['y_true'] = y.values # selecionando a variável de churn para o dataset de validação
    df_val['prob_churn'] = y_val_prob # valores previstos a partir do treinamento do modelo

    df_val['risk_band'] = pd.qcut(
        df_val['prob_churn'],
        q=[0, 0.33, 0.66, 1.0], # faixa de risco
        labels=['Baixo', 'Médio', 'Alto']
    )

    summary = (
        df_val
        .groupby('risk_band')
        .agg(
            clientes=('y_true', 'count'),
            churn_rate=('y_true', 'mean')
        )
        .reset_index()
    )

    return summary
