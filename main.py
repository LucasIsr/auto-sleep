from functions import AtlasFunctions, ReportsFunctions
import datetime


print(f'Início: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

# Definir essa variável apenas para execução manual, None por padrão
main_date = None #datetime.date(year=2024, month=5, day=23)

d_1 = None
d_2 = None

if main_date:
    d_1 = main_date - datetime.timedelta(days=1)
    d_1 = d_1.strftime("%d/%m/%Y")

    d_2 = main_date - datetime.timedelta(days=2)
    d_2 = d_2.strftime("%d/%m/%Y")

result = False

while not result:
    try:
        # Relatório de alertas - d-1
        # Relatório de posições - d-2 / d-1
        # Limpando pastas antes da execução
        AtlasFunctions.clean()

        # Extraindo o relatório principal de alertas contendo todas as placas necessárias
        print('Iniciando extração do relatório de alertas')
        AtlasFunctions.extract_alert(d_1)

        # Extraindo o relatório de cada placa baseado no relatório de alertas e já fazendo a análise de instertício
        print('Extraindo e analisando as placas')
        AtlasFunctions.extract_position(d1=d_1, d2=d_2)

        print('Inputando dados de resultado no banco')
        ReportsFunctions.insert_result()

        result = True

    except Exception as e:
        with open('log.txt', 'a') as file:
            file.write(f'Log de erro {datetime.datetime.now()}   Erro: {e}\n')