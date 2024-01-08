import os
import shutil
import pandas as pd
from extrair_posicoes import extract_position

DOWNLOAD_PATH = r'C:\Users\lucas\Downloads'
PLACAS_PATH = r'C:\Users\lucas\Downloads' 

for file in os.listdir(DOWNLOAD_PATH):
    if 'Relatorio Alertas.xlsx' in file:
        df = pd.read_excel(os.path.join(DOWNLOAD_PATH, file))
        df = df.drop_duplicates(subset='Placa')
        for index, linha in df.iterrows():
            placa = linha['Placa']
            extract_position(placa)
            os.mkdir(os.path.join(PLACAS_PATH, placa))
            for file_placa in os.listdir(DOWNLOAD_PATH):
                if 'Relatorio Posicao.xlsx' in file_placa:
                    placa_folder = PLACAS_PATH + f'\{placa}'
                    shutil.move(os.path.join(DOWNLOAD_PATH, file_placa), os.path.join(placa_folder, f'{placa}.xlsx'))
