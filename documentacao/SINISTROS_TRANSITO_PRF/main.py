# importando as bibliotecas
import logging
import sys
from pathlib import Path

import pandas as pd

ROOT = Path.cwd().parent 
sys.path.append(str(ROOT))

logging.basicConfig(
    filename="saida_treinamento_validacao.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

import os
import time

import matplotlib.pyplot as plt
import numpy as np

from data_preparation.preparation_final_data import preparation_data
from data_understanding.unzip_files import generate_random_sample
from evaluation.evaluation_code import (plot_fake_analysis,
                                        plot_prediction_error, return_metrics,metrics_pred_fake)
from modeling.train import (decision_tree_model, gradboost_model,
                            random_forest_model, variable_to_model, poissonregr_model, hist_gradboost_model)

dir = os.path.join(ROOT,r'SINISTROS_TRANSITO_PRF\contents\arquivos_descompactados')

logging.info("LEITURA DOS DADOS E PREPARAÇÃO DAS FEATURES INICIADA")

base, tempo_exec = preparation_data(dir=dir,tipo_tabela="real",tabela="")

logging.info(f"O código de preparação levou {tempo_exec:.2f} segundos para ser executado")

logging.info(base.shape)

logging.info("ETAPA DE PREPARAÇÃO DOS DADOS CONCLUÍDA")
logging.info("#"*100)

logging.info("ETAPA DA MODELAGEM INICIADA")

#variáveis de treino, teste e validação
X_train, y_train, X_test, y_test, X_val, y_val = variable_to_model(base,2022,2023,2025)

logging.info("SEPARAÇÃO DAS VARIÁVEIS DE TREINO, TESTE E VALIDAÇÃO CONCLUÍDA")

#aplicação dos modelos
# inicio = time.time()
# rd_forest_model = random_forest_model(X_train,y_train)
# final = time.time()
# logging.info(f"random forest concluído com sucesso - tempo de execução : {(final - inicio):.2f} segundos")

# inicio = time.time()
# decision_model = decision_tree_model(X_train,y_train)
# final = time.time()
# logging.info(f"decision tree concluído com sucesso  - tempo de execução : {(final - inicio):.2f} segundos")

inicio = time.time()
grad_boost_model = gradboost_model(X_train,y_train)
final = time.time()
logging.info(f"gradient boosting concluído com sucesso - tempo de execução : {(final - inicio):.2f} segundos")

inicio = time.time()
poisson_model = poissonregr_model(X_train,y_train)
final = time.time()
logging.info(f"poisson regressor concluído com sucesso - tempo de execução : {(final - inicio):.2f} segundos")

inicio = time.time()
hist_grad_boost_model = hist_gradboost_model(X_train,y_train)
final = time.time()
logging.info(f"hist gradient boosting concluído com sucesso - tempo de execução : {(final - inicio):.2f} segundos")

logging.info("#"*100)
logging.info("ETAPA DA AVIALAÇÃO - CONJUNTO DE VALIDAÇÃO")

#validação dos modelos (variáveis de validação)
# metricas_rd_forest = return_metrics(rd_forest_model,X_val,y_val)
# metricas_decision = return_metrics(decision_model,X_val,y_val)
metricas_gradboost = return_metrics(grad_boost_model,X_val,y_val,"gradient_boosting")
metricas_poisson = return_metrics(poisson_model ,X_val,y_val,"poisson")
metricas_hist_gradboost = return_metrics(hist_grad_boost_model,X_val,y_val,"hist_gradient_boosting")

# resultado = {"random_forest":metricas_rd_forest,
#              "decision_tree":metricas_decision,
#              "gradient_boosting":metricas_gradboost}

resultado = {"gradient_boosting":metricas_gradboost,
             "poisson":metricas_poisson,
             "hist_gradient_boosting":metricas_hist_gradboost}

# plot_prediction_error(rd_forest_model,X_val,y_val)
# plot_prediction_error(decision_model,X_val,y_val)
# plot_prediction_error(grad_boost_model,X_val,y_val)

logging.info("===== RESULTADOS DOS MODELOS =====")

logging.info(resultado)

for modelo, metricas in resultado.items():
    logging.info(f"Modelo: {modelo}")
    for nome, valor in metricas.items():
        logging.info(f"   {nome}: {valor:.4f}")
    logging.info("-" * 40)

logging.info("#"*100)
logging.info("ETAPA DA AVIALAÇÃO - CONJUNTO DE TESTE")

#validação dos modelos (variáveis de teste)
# metricas_rd_forest_final = return_metrics(rd_forest_model,X_test,y_test)
# metricas_decision_final = return_metrics(decision_model,X_test,y_test)
metricas_gradboost_final = return_metrics(grad_boost_model,X_test,y_test,"gradient_boosting")
metricas_poisson_final = return_metrics(poisson_model ,X_test,y_test,"poisson")
metricas_hist_gradboost_final = return_metrics(hist_grad_boost_model,X_test,y_test,"hist_gradient_boosting")

# resultado_final = {"random_forest":metricas_rd_forest_final,
#                    "decision_tree":metricas_decision_final,
#                    "gradient_boosting":metricas_gradboost_final}

resultado_final = {"gradient_boosting":metricas_gradboost_final,
                   "poisson":metricas_poisson_final,
                   "hist_gradient_boosting":metricas_hist_gradboost_final}

# plot_prediction_error(rd_forest_model,X_test,y_test)
# plot_prediction_error(decision_model,X_test,y_test)
# plot_prediction_error(grad_boost_model,X_test,y_test)

logging.info(resultado_final)

for modelo, metricas in resultado_final.items():
    logging.info(f"Modelo: {modelo}")
    for nome, valor in metricas.items():
        logging.info(f"   {nome}: {valor:.4f}")
    logging.info("-" * 40)

#Aplicação do melhor modelo em dados aleatórios para o ano de 2026
logging.info("#"*100)
logging.info("INICIANDO A PREDIÇÃO EM CASOS ALEATÓRIOS PARA O 1º SEMESTRE DE 2026")

base_fake = generate_random_sample(dir, n_registros=20000)

base_fake_total, tempo_exec_fake = preparation_data(dir="",tipo_tabela="fake",tabela=base_fake)

logging.info(f"O código de preparação levou {tempo_exec_fake:.2f} segundos para ser executado")

logging.info(base_fake_total.shape)

X_train_fake = base_fake_total.drop(columns=['feridos']).reindex(columns=X_train.columns, fill_value=0)

pred_fake = hist_grad_boost_model.predict(X_train_fake)

metricas_fake = metrics_pred_fake(pred_fake)

logging.info(metricas_fake)

with open("previsoes_saida.txt","w") as file:
    file.write("\n".join(map(str, pred_fake)))

plot_fake_analysis(y_train,pred_fake)
plt.show()

logging.info("CÓDIGO FINALIZADO")
logging.info("#"*100)