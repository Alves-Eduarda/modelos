import io
import os
import zipfile
from pathlib import Path

import pandas as pd
import requests

parent_dir = Path.cwd().parent

def download_file():
    """
        Retorna os dados que serão utilizados no projeto
    """
    url = r'https://www.kaggle.com/api/v1/datasets/download/barun2104/telecom-churn'
    diretorio = os.path.join(parent_dir,'contents')

    response = requests.get(url=url,stream=True)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(diretorio)

    print("Download e extração concluídos!")


#leitura dos dados
def return_data(file,extension = 'csv'):
    """
    Retorna os dados que serão trabalhados no projeto
   
    """

    if extension == 'csv':
        df = pd.read_csv(os.path.join(parent_dir,file),sep=',')
    else:
        df = pd.read_excel(os.path.join(parent_dir,file))
    
    return df