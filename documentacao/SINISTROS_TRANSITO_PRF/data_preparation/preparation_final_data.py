# importação das bibliotecas
import os

import sys
from pathlib import Path

import time

ROOT = Path.cwd().parent 
sys.path.append(str(ROOT))

import numpy as np
import pandas as pd

from data_preparation.data_prep import (cod_ciclico, codificacao_freq, codificacao_freq_normal,
                       generate_file_ibge, remove_col)
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder

from data_understanding.eda import (convert_to_numeric, days_week,
                                    extract_data, extract_time)
from data_understanding.unzip_files import generate_files


def preparation_data(dir,tipo_tabela,tabela) -> pd.DataFrame:

    t_inicial = time.time()

    if tipo_tabela == "real":

        #leitura da base
        bases = generate_files(dir)

    elif tipo_tabela == "fake":
        bases = tabela
        
    else:
        return "Configurações de preparação não definidas. Tente novamente"

    #Tratamento das colunas
    
    # substituindo os valores escritos (null) por nulos de fato
    bases.replace('(null)',np.nan,inplace=True)
    
    # substituindo as vírgulas por pontos
    bases['km'] = convert_to_numeric(bases,'km')

    bases['br'] = convert_to_numeric(bases,'br')

    bases['longitude'] = convert_to_numeric(bases,'longitude')

    bases['latitude'] = convert_to_numeric(bases,'latitude')

    # ajustando os valores que contém datas e horários
    bases['data'] = extract_data(bases,'data_inversa')

    bases['horario'] = extract_time(bases,"horario")

    # Criação de novas variáveis a partir da data (feature engineering)
    bases['ano_novo'] = bases['data'].dt.year

    bases['hora'] = pd.to_datetime(bases['horario']).apply(lambda x: x.hour)

    bases['mes'] = bases['data'].dt.month

    bases['dia'] = bases['data'].dt.day

    # ajuste nas palavras das colunas categóricas
    bases['dia_semana_novo'] = days_week(bases,'dia_semana')

    bases['condicao_metereologica'] = bases['condicao_metereologica'].str.lower()

    bases['condicao_metereologica'] = bases['condicao_metereologica'].str.replace('céu','ceu')

    bases['condicao_metereologica'] = bases['condicao_metereologica'].str.replace('ignorada','ignorado')

    bases['fase_dia'] = bases['fase_dia'].str.lower()

    # retirando da base as colunas que só se apresentam após 2016, colunas que já foram ajustadas em outras variáveis e o id    
    bases = remove_col(bases,['latitude','longitude','delegacia','uop','regional','ano','dia_semana','id','data_inversa','horario'])

    # Renomeando as colunas criadas
    bases.rename(columns={'ano_novo':'ano','dia_semana_novo':'dia_semana'},inplace=True)

    # Vamos remover estes dados nulos pois estão em pequeno volume
    bases.dropna(axis=0,inplace=True)

    #Remoção das colunas que geram vazamento de informações
    bases = remove_col(bases,['feridos_graves','feridos_leves','pessoas','ilesos','ignorados','mortos'])

    #Transformação das colunas categóricas para numéricas
   
    # Adicionando o código referente a UF e Municipio
    #substituição
    bases['uf_mun'] = bases['uf'] + "-" + bases['municipio']
    df_ibge = generate_file_ibge(os.path.join(ROOT,r"SINISTROS_TRANSITO_PRF/contents/municipio_tse_ibge.csv"))
    lista_cod_uf = df_ibge[['SG_UF','CD_UF_IBGE']].copy()

    lista_cod_uf = lista_cod_uf.drop_duplicates(keep='first')

    bases = bases.merge(lista_cod_uf,left_on='uf',right_on='SG_UF',how='left')

    bases = bases.merge(df_ibge[['uf_mun','CD_MUNICIPIO_IBGE']], on='uf_mun',how='left')

    bases = remove_col(bases,['SG_UF'])

    bases.dropna(axis=0,inplace=True)
    # Alterando o tipo da coluna de float para int
    bases['CD_MUNICIPIO_IBGE'] = bases['CD_MUNICIPIO_IBGE'].astype('int64')

    #Removendo as colunas que já foram transformadas
    bases = remove_col(bases,['uf','municipio','uf_mun'])

    #Método de categorização
    colunas = ['classificacao_acidente','sentido_via','tipo_pista','uso_solo']
    one_hot_enc = OneHotEncoder(sparse_output=False,handle_unknown='ignore')

    encoded = one_hot_enc.fit_transform(bases[colunas])

    df_encoded = pd.DataFrame(
        encoded,
        columns=one_hot_enc.get_feature_names_out(colunas),
        index=bases.index
    )

    bases_resultado = pd.concat([bases.drop(columns=colunas), df_encoded], axis=1)

    #codificação por frequencia
    colunas_freq = ['causa_acidente','tipo_acidente','condicao_metereologica','tracado_via']
    bases_resultado = codificacao_freq(bases_resultado,colunas_freq)

    bases_resultado = remove_col(bases_resultado,col=['causa_acidente','tipo_acidente','condicao_metereologica','tracado_via'])

    # codificação cíclica
    bases_resultado['dia_semana_num'] = bases_resultado['dia_semana'].map({
    'segunda':0,'terca':1,'quarta':2,
    'quinta':3,'sexta':4,'sabado':5,'domingo':6})


    bases_resultado = cod_ciclico(bases_resultado,'dia_semana_num',7)
    bases_resultado = cod_ciclico(bases_resultado,'mes',12)
    bases_resultado = cod_ciclico(bases_resultado,'hora',24)

    bases_resultado = remove_col(bases_resultado,['dia_semana_num','dia_semana','data'])

    #codificação ordinal
    # Definir a ordem correta das categorias
    ordem = ['amanhecer', 'pleno dia', 'anoitecer','plena noite']

    encoder = OrdinalEncoder(categories=[ordem])

    # Aplicar a transformação
    bases_resultado['fase_dia_encoded'] = encoder.fit_transform(bases_resultado[['fase_dia']])

    # Removendo as colunas transformadas
    bases_resultado = remove_col(bases_resultado,['fase_dia','hora','mes','dia'])

    #variáveis numéricas que são categóricas - br e km

    bases_resultado['br_km'] = bases_resultado['br'].astype(str).str.strip() + "_" + bases_resultado['km'].astype(str).str.strip()
    bases_resultado = codificacao_freq_normal(bases_resultado,['br_km'])

    #criando uma coluna referente ao posicionamento do km nas brs (é recomendada para a modelagem)
    #max_km_por_br = bases_resultado.groupby('br', as_index=True)['km'].max()
    #bases_resultado['km_relativo'] = bases_resultado['km'] / max_km_por_br

    bases_resultado = remove_col(bases_resultado,['br','km'])

    t_final = time.time()

    tempo_execucao = t_final - t_inicial

    #Geração do dataset para treinamento do modelo

    return bases_resultado, tempo_execucao

