# importando as bibliotecas
import pandas as pd
import logging

import sys
from pathlib import Path

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
from data_preparation.preparation_final_data import preparation_data
from modeling.train import variable_to_model, random_forest_model, decision_tree_model, gradboost_model
from evaluation.evaluation_code import return_metrics

dir = os.path.join(ROOT,r'SINISTROS_TRANSITO_PRF\contents\arquivos_descompactados')

base, tempo_exec = preparation_data(dir)

logging.info(f"O código de preparação levou {tempo_exec:.2f} segundos para ser executado")

logging.info(base.shape)

logging.info("ETAPA DE PREPARAÇÃO DOS DADOS CONCLUÍDA")
logging.info("#"*100)

logging.info("ETAPA DA MODELAGEM INICIADA")

#variáveis de treino, teste e validação
X_train, y_train, X_test, y_test, X_val, y_val = variable_to_model(base,2022,2023,2025)

logging.info("SEPARAÇÃO DAS VARIÁVEIS DE TREINO, TESTE E VALIDAÇÃO CONCLUÍDA")

#aplicação dos modelos
inicio = time.time()
rd_forest_model = random_forest_model(X_train,y_train)
final = time.time()
logging.info(f"random forest concluído com sucesso - tempo de execução : {(final - inicio):.2f} segundos")

inicio = time.time()
decision_model = decision_tree_model(X_train,y_train)
final = time.time()
logging.info(f"decision tree concluído com sucesso  - tempo de execução : {(final - inicio):.2f} segundos")

inicio = time.time()
grad_boost_model = gradboost_model(X_train,y_train)
final = time.time()
logging.info(f"gradient boosting concluído com sucesso - tempo de execução : {(final - inicio):.2f} segundos")

logging.info("#"*100)
logging.info("ETAPA DA AVIALAÇÃO - CONJUNTO DE VALIDAÇÃO")

#validação dos modelos (variáveis de validação)
metricas_rd_forest = return_metrics(rd_forest_model,X_val,y_val)
metricas_decision = return_metrics(decision_model,X_val,y_val)
metricas_gradboost = return_metrics(grad_boost_model,X_val,y_val)

resultado = {"random_forest":metricas_rd_forest,
             "decision_tree":metricas_decision,
             "gradient_boosting":metricas_gradboost}

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
metricas_rd_forest_final = return_metrics(rd_forest_model,X_test,y_test)
metricas_decision_final = return_metrics(decision_model,X_test,y_test)
metricas_gradboost_final = return_metrics(grad_boost_model,X_test,y_test)

resultado_final = {"random_forest":metricas_rd_forest_final,
                   "decision_tree":metricas_decision_final,
                   "gradient_boosting":metricas_gradboost_final}

logging.info(resultado_final)

for modelo, metricas in resultado_final.items():
    logging.info(f"Modelo: {modelo}")
    for nome, valor in metricas.items():
        logging.info(f"   {nome}: {valor:.4f}")
    logging.info("-" * 40)
