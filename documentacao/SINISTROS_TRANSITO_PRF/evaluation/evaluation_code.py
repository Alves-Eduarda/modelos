import pandas as pd
import numpy as np

from sklearn.metrics import mean_absolute_error, mean_squared_error,  r2_score, root_mean_squared_error
from sklearn.ensemble import (RandomForestRegressor, GradientBoostingRegressor)
from sklearn.tree import DecisionTreeRegressor

def return_metrics(model,X,y) -> dict:

    y_pred = model.predict(X)

    mae = mean_absolute_error(y,y_pred)
    mse = mean_squared_error(y,y_pred)
    r2 = r2_score(y,y_pred)
    rmse = root_mean_squared_error(y, y_pred)

    return {"mae":mae,"mse":mse,"r2":r2,"rmse":rmse}

