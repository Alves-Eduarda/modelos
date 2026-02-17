# importando as bibliotecas
import os
import shutil
import zipfile
from pathlib import Path
import sqlite3
import pandas as pd
import numpy as np

dir_cur = Path.cwd()

def unzip_files(dir: str):

    try:

        # diretorio com os arquivos descompactados
        output = os.path.join(dir,'arquivos_descompactados')

        os.makedirs(os.path.join(dir,output),exist_ok=True)

        for f in os.listdir(dir):
            if f.lower().endswith('.zip'):
               zip_path = os.path.join(dir, f)

               with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    for member in zip_ref.namelist():
                    # skip directories
                        if member.endswith("/"):
                            continue
                        # extract file to a temp location
                        zip_ref.extract(member, output)

                        source_path = os.path.join(output, member)
                        target_path = os.path.join(output, os.path.basename(member))

                        # move file to output root (flatten structure)
                        shutil.move(source_path, target_path)
        
        return "Arquivos descompactados"
    except Exception as error:
        return f"Erro ao tentar descompactar os arquivos - {error}"


def check_consistencia_colunas(dir):

    colunas = {}
    qtd_colunas = {}
    tam_bases = {}

    for f in os.listdir(dir):
        file = os.path.join(dir,f)
        df_temp = pd.read_csv(file,sep=';',encoding='latin1',low_memory=False)

        colunas[f] = list(df_temp.columns)
        qtd_colunas[f] = df_temp.shape[1]
        tam_bases[f] = df_temp.shape[0]

    return colunas, qtd_colunas, tam_bases


def generate_files(dir) -> pd.DataFrame:

    df_final = pd.DataFrame()

    for f in os.listdir(dir):
        file = os.path.join(dir,f)
        df_temp = pd.read_csv(file,sep=';',encoding='latin1',low_memory=False)


        df_final = pd.concat([df_final,df_temp])

    return df_final

def generate_sql_file(dir):

    tabela = generate_files(dir)

    conn = sqlite3.connect("dados.db")
    tabela.to_sql("tabela", conn, if_exists="replace", index=False)
    conn.close()


def generate_random_sample(dir, n_registros=1000,seed=42):

    df = generate_files(dir)

    np.random.seed(seed)

    # intervalo de datas
    datas = pd.to_datetime(
        np.random.choice(
            pd.date_range("2026-01-01", "2026-06-30"),
            size=n_registros,
            replace=True
        )
    )

    novo = pd.DataFrame()

    # id sequencial
    novo["id"] = range(1, n_registros + 1)

    # data
    novo["data_inversa"] = datas.strftime("%d/%m/%Y")
    novo["ano"] = 2026
    novo["dia_semana"] = datas.day_name(locale='pt_BR').str.lower()

    # horario aleatório
    segundos = np.random.randint(0, 24*60*60, n_registros)
    novo["horario"] = pd.to_datetime(segundos, unit="s").strftime("%H:%M:%S")

    # função para amostragem proporcional
    def sample(col):
        dist = df[col].value_counts(normalize=True)
        return np.random.choice(
            dist.index,
            size=n_registros,
            p=dist.values
        )

    # colunas categóricas

    cols_cat = [
        'uf','br','km','municipio','causa_acidente','tipo_acidente',
        'classificacao_acidente','fase_dia','sentido_via',
        'condicao_metereologica','tipo_pista','tracado_via','regional','uso_solo',
        'latitude','longitude','delegacia','uop'
    ]

    for c in cols_cat:
        novo[c] = sample(c)

    # variáveis numéricas baseadas na distribuição
    def sample_num(col):
        return np.random.choice(df[col].dropna(), size=n_registros)

    novo["veiculos"] = sample_num("veiculos")
    novo["pessoas"] = sample_num("pessoas")

    # gerar vítimas coerentes
    novo["mortos"] = np.random.binomial(novo["pessoas"], 0.02)
    novo["feridos_graves"] = np.random.binomial(novo["pessoas"], 0.05)
    novo["feridos_leves"] = np.random.binomial(novo["pessoas"], 0.15)

    novo["feridos"] = novo["feridos_leves"] + novo["feridos_graves"]

    novo["ilesos"] = np.maximum(
        0,
        novo["pessoas"] - (novo["mortos"] + novo["feridos"])
    )

    novo["ignorados"] = np.random.binomial(novo["pessoas"], 0.01)

    return novo


