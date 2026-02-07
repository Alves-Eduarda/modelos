#importando as bibliotecas

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

def correlation_graph(df: pd.DataFrame):

    plt.figure(figsize=(10, 8))
    corr = df.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm')
    plt.title("Matriz de Correlação - Análise do Churn")


def pairplot_churn(df: pd.DataFrame, col: list, part:str):

    g = sns.pairplot(df[col], hue=part, diag_kind="hist")

    g.fig.suptitle("Pairplot para análise do Churn", y=1.05)
    g.fig.tight_layout()
