from functions import AtlasFunctions, ReportsFunctions
import datetime


print(f'Início: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

# Relatório de alertas - d-1
# Relatório de posições - d-2 / d-1

data_inicio = datetime.date(2024, 3, 4)
data_fim = datetime.date(2024, 3, 12)

while data_inicio <= data_fim:

    try:
        d1 = data_inicio - datetime.timedelta(days=1)

        # Limpando pastas antes da execução
        AtlasFunctions.clean()

        # Extraindo o relatório principal de alertas contendo todas as placas necessárias
        print('Iniciando extração do relatório de alertas')
        AtlasFunctions.extract_alert(str(data_inicio.strftime('%d/%m/%Y')))

        # Extraindo o relatório de cada placa baseado no relatório de alertas e já fazendo a análise de instertício
        print('Extraindo e analisando as placas')
        AtlasFunctions.extract_position(str(d1.strftime('%d/%m/%Y')), str(data_inicio.strftime('%d/%m/%Y')))

        print('Inputando dados de resultado no banco')
        ReportsFunctions.insert_result(str(d1.strftime('%d/%m/%Y')), str(data_inicio.strftime('%d/%m/%Y')))

        print(f'Data {data_inicio} bem sucedida!')
        data_inicio += datetime.timedelta(days=1)

    except:
        print(f'Data {data_inicio} falhou.')
        break

print(f'Fim: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')