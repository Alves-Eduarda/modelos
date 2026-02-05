# EDA - Exploratory Data Analysis

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


#leitura dos dados
def return_data(file):
    """
    Retorna os dados que serão trabalhados no projeto
   
    """

    df = pd.read_csv(file,sep=',')
    return df

# analise das informações da tabela
def null_values(df):
    """
    Retorna se existe valor nulo no dataset
   
    """
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            print(f"{col} - {df[col].isnull().sum()} valores nulos")
        else:
            print("Não existem valores nulos no dataset")

def duplicated_values(df):
    """
    Retorna se existem valores duplicados no dataset

    """
    return df.duplicated().sum()

def generic_info(df): 
    """
    Retornam informações sobre o dataset referentes ao tamanho e distribuição dos dados de cada coluna (max e min)

    """

    print(f"O dataset tem o shape de {df.shape[0]} linhas e {df.shape[1]} colunas")

    print('-'*50)

    print("As colunas  obtém os seguintes dados de máximo e mínimo:\n")
  
    for col in df.columns:
        if df[col].dtype == 'int64' or df[col].dtype == 'float64':
            print(f'{col}: {df[col].min(),df[col].max()}, {np.mean(df[col])}')
        else:
            print(f'{col}: {df[col].unique()}')
        

# geração das análises gráficas

def dist_graph(df: pd.DataFrame, col: list):

    df_dist = df[col]
    df_dist.hist(bins=20, figsize=(15, 10), layout=(3, 3), grid=True)
    plt.tight_layout()
    plt.show()
    plt.save()

def bar_graph():
    pass

def hist_graph(df: pd.DataFrame,var:str,part: str):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=var, hue=part, kde=True, element="step", palette='viridis')
    plt.title('Distribuição da Variável MonthlyCharge por Status de Churn')
    plt.show()

