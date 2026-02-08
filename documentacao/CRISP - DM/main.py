from data_preparation.preparation_data import processing_data
from modeling.train import *
from evaluation.evaluation import evaluate_model, range_test_risk_churn
from evaluation.graphic_evalutation import plot_roc_cure
import matplotlib.pyplot as plt

# recebendo o dado processado
df_padronizado = processing_data()

# criando as variáveis pós treino dos modelos
xgboost_model, X_val_bg, y_val_bg, feature_importance_to_test = xgboost_aplication(df_padronizado)

xgboost_model_fi, X_val_bg_fi, y_val_bg_fi = xgboost_aplication_with_feature_importance(df_padronizado[feature_importance_to_test])

lr_model, X_val_lr, y_val_lr = logistc_regression_aplication(df_padronizado)

#aplicando a avaliação do modelo
evaluate_model(lr_model, X_val_lr, y_val_lr, 'Logistic Regression')
evaluate_model(xgboost_model, X_val_bg, y_val_bg, 'XGBoost sem Feature Importance')
evaluate_model(xgboost_model_fi, X_val_bg_fi, y_val_bg_fi, 'XGBoost com Feature Importance')

# analisando os modelos por grafico ( curva ROC)
models = {'LR': lr_model, 'XGB': xgboost_model, 'XGB - FI': xgboost_model_fi}
plot_roc_cure(models, [X_val_bg, X_val_bg_fi], [y_val_bg, y_val_bg_fi])
plt.show()

# aplicando os testes de validação com o modelo XGBOOST (melhor resultado)
result = range_test_risk_churn(xgboost_model, X_val_bg, y_val_bg)

print(result)

#   risk_band  clientes  churn_rate
#0     Baixo       220    0.036364
#1     Médio       220    0.018182
#2      Alto       227    0.374449

