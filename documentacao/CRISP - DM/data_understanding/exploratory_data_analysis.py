# EDA - Exploratory Data Analysis
import numpy as np
import pandas as pd

# analise das informações da tabela
def null_values(df):
    """
    Retorna se existe valor nulo no dataset
   
    """
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            print(f"{col} - {df[col].isnull().sum()} valores nulos")
        else:
            print(f"{col} - Não existem valores nulos no dataset")

def duplicated_values(df):
    """
    Retorna se existem valores duplicados no dataset

    """
    return f"Existem {df.duplicated().sum()} valores duplicados no dataset"

def duplicated_values_each_column(df):
    """
    Retorna se existem valores duplicados no dataset em cada coluna

    """
    
    for col in df.columns:
        print(f"{col} - {df[col].duplicated().sum()}")


def generic_info(df): 
    """
    Retornam informações sobre o dataset referentes ao tamanho e distribuição dos dados de cada coluna (max e min)

    """

    print(f"O dataset tem o shape de {df.shape[0]} linhas e {df.shape[1]} colunas")

    print('-'*50)

    print("As colunas  obtém os seguintes dados de máximo, mínimo e média:\n")
  
    for col in df.columns:
        if df[col].dtype == 'int64' or df[col].dtype == 'float64':
            print(f'{col}: {df[col].min(),df[col].max()}, {np.mean(df[col])}')
        else:
            print(f'{col}: {df[col].unique()}')
        

