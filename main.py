from functions import AtlasFunctions
import datetime


print(f'Início: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

# Extraindo o relatório principal de alertas contendo todas as placas necessárias
#AtlasFunctions.extract_alert()

AtlasFunctions.extract_alert()
print('extraido a alertas')

# Extraindo o relatório de cada placa baseado no relatório de alertas e já fazendo a análise de instertício

AtlasFunctions.extract_position()

print(f'Fim: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')