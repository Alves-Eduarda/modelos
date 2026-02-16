# importando as bibliotecas
import pandas as pd 
import unicodedata
import numpy as np

# Remover colunas desnecessárias
def remove_col(df,col) -> pd.DataFrame:

    """
      Docstring for cod_ciclico
    
    :param df: dataframe
    :param col: colunas que irão ser removidas

    """

    for c in col:
        df.drop(columns={c},inplace=True)
    
    return df

# Remover os acentos
def remover_acentos(texto):
    """

      Docstring for cod_ciclico
    
    :param texto: valores da coluna que será aplicada a remoção de acentos 
    
    """

    if pd.isna(texto):
        return texto
    return ''.join(
        c for c in unicodedata.normalize('NFD', str(texto))
        if unicodedata.category(c) != 'Mn'
    )

# Gerar o arquivo de codificação da UF e IBGE por substituição
def generate_file_ibge(dir) -> pd.DataFrame:

    """
      Docstring for cod_ciclico
    
    :param dir: diretório aonde a planilha está localizada
    
    """

    df_ibge = pd.read_csv(dir,encoding='latin1',sep=';')

    df_ibge['NM_MUNICIPIO_IBGE'] = df_ibge['NM_MUNICIPIO_IBGE'].str.upper()

    df_ibge_copia = df_ibge[['SG_UF','CD_UF_IBGE','CD_MUNICIPIO_IBGE','NM_MUNICIPIO_IBGE']].copy()

    df_ibge_copia['municipio_norm'] = df_ibge_copia['NM_MUNICIPIO_IBGE'].apply(remover_acentos).str.upper().str.strip()

    df_ibge_copia['uf_mun'] = df_ibge_copia['SG_UF'] + "-" + df_ibge_copia['municipio_norm']

    return df_ibge_copia

# Transformar as colunas categóricas em numéricas com a transformação de OneHotEncoder
def cod_ciclico(df,col,max_val) -> pd.DataFrame:
    """
    Docstring for cod_ciclico
    
    :param df: Description
    :param col: Description
    :param max_val: depende da informação se for dia ou mês
    """
    
    df[f'{col}_sen'] = np.sin(2*np.pi*df[col]/max_val)
    df[f'{col}_cos'] = np.cos(2*np.pi*df[col]/max_val)

    return df


# Padronizar os dados a partir da distribução deles 
def codificacao_freq(df,col) -> pd.DataFrame:

    for c in col:
        freq = df[c].value_counts()
        df[f"{c}_freq"] = df[c].map(freq)
    
    return df


def codificacao_freq_normal(df:pd.DataFrame,col:list) -> pd.DataFrame:
    
    for c in col:
        freq_map = df[c].value_counts(normalize=True)

        df[f'{c}_freq_normal'] = df[c].map(freq_map)

        # tratar valores raros (opcional mas recomendado)
        limite = 0.0001
        df[f'{c}_freq_normal'] = df[f'{c}_freq_normal'].where(df[f'{c}_freq_normal'] > limite, limite)

        # se quiser remover coluna original
        df.drop(columns=[c], inplace=True)
    
    return df

# exportar o dado preparado para modelagem
def export_sample(df,num_max):

    df_output = df[0:num_max]

    return df_output.to_csv("base_resultado_amostra.csv",sep=';',index=False,encoding='utf-8')
