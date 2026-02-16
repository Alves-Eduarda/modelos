# importando as bibliotecas
import os
import shutil
import zipfile
from pathlib import Path
import sqlite3
import pandas as pd

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