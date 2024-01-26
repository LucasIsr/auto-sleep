from functions import AtlasFunctions, ReportsFunctions

# Extraindo o relatório principal de alertas contendo todas as placas necessárias
#AtlasFunctions.extract_alert()
print('Relatório de alertas extraído...')

# Extraindo o relatório de cada placa baseado no relatório de alertas
#ReportsFunctions.extract_all_reports()


ReportsFunctions.analyze_reports()
