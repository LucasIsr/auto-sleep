from functions import AtlasFunctions, ReportsFunctions
import datetime


print(f'Início: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

# Extraindo o relatório principal de alertas contendo todas as placas necessárias
print('Iniciando extração do relatório de alertas')
AtlasFunctions.extract_alert()

# Extraindo o relatório de cada placa baseado no relatório de alertas e já fazendo a análise de instertício
print('Extraindo e analisando as placas')
AtlasFunctions.extract_position()

print('Inputando dados de resultado no banco')
ReportsFunctions.insert_result()

print(f'Fim: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')