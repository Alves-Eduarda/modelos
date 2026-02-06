import requests
import zipfile
import os
import io

def download_file():
    """
        Retorna os dados que serão utilizados no projeto
    """
    url = r'https://www.kaggle.com/api/v1/datasets/download/barun2104/telecom-churn'
    diretorio = os.path.join(os.getcwd(),'contents')

    response = requests.get(url=url,stream=True)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(diretorio)

    print("Download e extração concluídos!")
