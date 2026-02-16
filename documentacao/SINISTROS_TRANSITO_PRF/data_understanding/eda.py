# importando as bibliotecas
import numpy as np
import pandas as pd


def convert_to_numeric(df,col):

    dados_tratados = (
        df[col]
        .astype(str)
        .str.strip()
        .str.replace(',', '.', regex=False)
        .str.replace(r'[^0-9\.-]', '', regex=True)
        .replace('', None)
        .pipe(pd.to_numeric, errors='coerce')
    )

    return dados_tratados


def extract_data(df,col):


    datas = (
        pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')
        .fillna(pd.to_datetime(df[col], format='%d/%m/%Y', errors='coerce'))
        .fillna(pd.to_datetime(df[col], format='%d/%m/%y', errors='coerce'))
    )

    return datas


def extract_time(df,col):    

    df[col] = df[col].astype(str).str.strip()

    horario = pd.to_datetime(
            df[col],
            format='%H:%M:%S',
            errors='coerce')
    

    return horario


def days_week(df,col):

    dias_semana = {
    'segunda-feira':'segunda',
    'terça-feira':'terca',
    'quarta-feira':'quarta',
    'quinta-feira':'quinta',
    'sexta-feira':'sexta',
    'sábado':'sabado',
    'segunda':'segunda',
    'terça':'terca',
    'quarta':'quarta',
    'quinta':'quinta',
    'sexta':'sexta',
    'domingo':'domingo',
    'sabado':'sabado'}

    dias_padronizados = df[col].str.lower().map(dias_semana)

    return dias_padronizados