import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from yellowbrick.regressor import PredictionError

from sklearn.metrics import mean_absolute_error, mean_squared_error,  r2_score, root_mean_squared_error, mean_poisson_deviance
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor)
from sklearn.tree import DecisionTreeRegressor

def return_metrics(model,X,y,nome_model) -> dict:

    y_pred = model.predict(X)
    y_pred = np.clip(y_pred, 0, None)

    if nome_model != "poisson":

        mae = mean_absolute_error(y,y_pred)
        mse = mean_squared_error(y,y_pred)
        r2 = r2_score(y,y_pred)
        rmse = root_mean_squared_error(y, y_pred)

        return {"mae":mae,"mse":mse,"r2":r2,"rmse":rmse}
    
    else:
        mae = mean_absolute_error(y,y_pred)
        mse = mean_squared_error(y,y_pred)
        r2 = r2_score(y,y_pred)
        poisson_dev = mean_poisson_deviance(y, y_pred)
        rmse = root_mean_squared_error(y, y_pred)

        return {"mae":mae,"mse":mse,"r2":r2,"rmse":rmse,"poisson_dev":poisson_dev}

def plot_prediction_error(model,X,y):

    fig, ax = plt.subplots(figsize=(6,6))
    pev = PredictionError(model,ax=ax)
    pev.fit(X,y)
    pev.finalize()
    
    fig.savefig(
        f"visualization/{model}_prediction_error.png",
        dpi=300,
        bbox_inches="tight"
    )

def plot_fake_analysis(y,pred):

    # pd.Series(y).plot(kind="kde", label="real")
    # pd.Series(pred).plot(kind="kde", label="previsto")

    # plt.legend()
    # plt.title("Distribuição Real vs Prevista")

    plt.hist(y, bins=range(0, int(max(y))+2), density=True, alpha=0.5, label="real")
    plt.hist(pred, bins=range(0, int(max(pred))+2), density=True, alpha=0.5, label="previsto")
    plt.legend()
    plt.title("Distribuição Real vs Prevista")


def metrics_pred_fake(y_pred):

    return {"min": np.min(y_pred),
            "max": np.max(y_pred),
            "media": np.mean(y_pred),
            "mediana": np.median(y_pred),
            "desvio_padrao": np.std(y_pred)}