#importando as bibliotecas
import pickle

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import PoissonRegressor
from sklearn.tree import DecisionTreeRegressor


def variable_to_model(df,max_year_train,year_val,max_year_test):
    """
    Docstring for define_data_to_model

    :param df: dataframe
    :param year_val: o ano de validação, indicado ser 2 anos a menos que o ano máximo de teste
    :param max_year_train: o ano máximo que servirá como limite para o conjunto de treino
    :param max_year_test: o ano máximo que servirá como limite para o conjunto de teste
    """

    df_train = df[df['ano'] <= int(max_year_train)]
    df_val = df[df['ano'] == int(year_val) ]
    df_test = df[(df['ano'] > int(year_val)) & (df['ano'] <= max_year_test)]

    X_train = df_train.drop(columns=['feridos'])
    y_train = df_train['feridos']

    X_val = df_val.drop(columns=['feridos'])
    y_val = df_val['feridos']

    X_test = df_test.drop(columns=['feridos']) 
    y_test = df_test['feridos']

    return X_train, y_train, X_test, y_test, X_val, y_val

def random_forest_model(X,y):

    regr_model = RandomForestRegressor(random_state=42)
    regr_model.fit(X, y)

    # salvando o modelo treinado
    with open("modelo_random_forest.pkl", "wb") as f:
        pickle.dump(regr_model, f)

    return regr_model

def decision_tree_model(X,y):

    decision_regr = DecisionTreeRegressor(random_state=42)

    decision_regr_model = decision_regr.fit(X,y)

    # salvando o modelo treinado
    with open("modelo_decision_tree.pkl", "wb") as f:
        pickle.dump(decision_regr_model, f)
    
    return decision_regr_model

def gradboost_model(X,y):

    grad_boost = GradientBoostingRegressor(loss="huber")
                                           
    grad_boost_model = grad_boost.fit(X,y)

    # salvamento do modelo
    with open("modelo_gradient_boosting.pkl", "wb") as f:
        pickle.dump(grad_boost_model, f)

    return grad_boost_model

def poissonregr_model(X,y):

    pregr = PoissonRegressor(alpha=0)
    
    pregr_model = pregr.fit(X,y)

    # salvamento
    with open("modelo_poisson_regressor.pkl", "wb") as f:
        pickle.dump(pregr_model, f)

    return pregr_model

def hist_gradboost_model(X,y):

    histgrad_boost = HistGradientBoostingRegressor(loss="poisson")

    hgrad_model = histgrad_boost.fit(X,y)

    # salvamento
    with open("modelo_hist_gradient_boosting.pkl", "wb") as f:
        pickle.dump(hgrad_model, f)

    return hgrad_model




