# importando as bibliotecas

import warnings

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from upsetplot import UpSet, from_memberships

warnings.filterwarnings(
    "ignore",
    module="upsetplot"
)

# geração das análises gráficas

def dist_graph(df: pd.DataFrame, col: list):

    df_dist = df[col]
    df_dist.hist(bins=20, figsize=(15, 10), layout=(3, 3), grid=True)
    plt.title("Distribuição das variáveis")
    plt.tight_layout()
    

def bar_graph(df: pd.DataFrame, col: str):

    df_vis_churn = df[col].value_counts()

    plt.figure(figsize=(8, 6))
    plt.bar(df_vis_churn.index.astype(str), df_vis_churn.values, color=['green', 'lightblue'])

    plt.title('Quantidade de Churn')
    plt.xlabel('Churn (0 = Não, 1 = Sim)')
    plt.ylabel('Quantidade')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

def hist_graph(df: pd.DataFrame,var:str,part: str):

    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x=var, hue=part, kde=True, element="step", palette='viridis')
    plt.title(f'Distribuição da Variável {var} por Status de Churn')


def correlation_multivariable(df: pd.DataFrame, col : list):
    
    df_vis_churn = (
    df
    .groupby(col)
    .size()
    .reset_index(name='count'))

    memberships = []
    counts = []

    for _, row in df_vis_churn.iterrows():
        m = []

        if row['ContractRenewal'] == 1:
            m.append('ContractRenewal')

        if row['DataPlan'] == 1:
            m.append('DataPlan')

        if row['Churn'] == 1:
            m.append('Churn')

        memberships.append(m)
        counts.append(row['count'])


    upset_data = from_memberships(
        memberships,
        data=counts
    )


    UpSet(
        upset_data,
        subset_size='sum',
        show_counts=True,
        sort_by='degree'
    ).plot()

    plt.suptitle(
        f'Intersecções entre {col[0], col[1], col[2]}',
        fontsize=14
    )


def count_plot(df:pd.DataFrame,col:str, part:str):

    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x=col, hue=part, palette='viridis')

    plt.title('Quantidade de Churn por Número de Chamadas ao Suporte', fontsize=14)
    plt.xlabel('Número de Chamadas (CustServCalls)', fontsize=12)
    plt.ylabel('Quantidade de Clientes', fontsize=12)
    plt.legend(title='Churn', labels=['Não (0)', 'Sim (1)'])
    plt.grid(axis='y', linestyle='--', alpha=0.6)


