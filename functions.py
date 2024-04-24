import time
import datetime
from link.app.link import Link
import os
import shutil
import pandas as pd
from threading import Thread
import psycopg2


with open('paths.txt', mode='r', encoding='utf-8') as path_file:
    for row in path_file:
        if row.strip().split('=')[0] == 'DOWNLOAD_PATH':
            DOWNLOAD_PATH = row.strip().split('=')[1]

        if row.strip().split('=')[0] == 'PLACAS_PATH':
            PLACAS_PATH = row.strip().split('=')[1]

        if row.strip().split('=')[0] == 'POSTGRE_PASSWORD':
            POSTGRE_PASSWORD = row.strip().split('=')[1]


class AtlasFunctions:


    @staticmethod
    def clean():
        for file in os.listdir(DOWNLOAD_PATH):
            if '.' in file:
                os.remove(os.path.join(DOWNLOAD_PATH, file))

        for file in os.listdir(PLACAS_PATH):
            os.remove(os.path.join(PLACAS_PATH, file))

    @staticmethod
    def extract_position(d1: str | None = None, d2: str | None = None):
        '''
        Metodo para extrair relatorio de posicao do Atlas
        '''

        with open('paths.txt', mode='r', encoding='utf-8') as path_file:
            for row in path_file:
                if row.strip().split('=')[0] == 'USUARIO':
                    USUARIO = row.strip().split('=')[1]

                if row.strip().split('=')[0] == 'SENHA':
                    SENHA = row.strip().split('=')[1]

        url = Link(url='http://app-vibra.atlasgr.com.br/', driver='Chrome', sleep=1)

        url.openLink()

        url.maximize()

        url.sendKeys('//*[@id="mui-1"]', USUARIO )

        url.sendKeys('//*[@id="mui-2"]', SENHA )

        url.clickElement('//*[@id="__next"]/div[1]/div/div/div/div[2]/div/div/button')

        url.clickElement('//*[@id="__next"]/div[1]/div[1]/div[3]/div[3]/div[1]')

        url.clickElement('//*[@id="__next"]/div[1]/div[1]/div[3]/div[3]/div[2]/div[3]/div')

        time.sleep(3)

        url.switchWindow(1)

        url.clearText('//*[@id="mui-6"]')

        if not d2:
            d2 = datetime.date.today() - datetime.timedelta(days=2)
            d2 = d2.strftime('%d%m%Y')

        if not d1:
            d1 = datetime.date.today() - datetime.timedelta(days=1)
            d1 = d1.strftime('%d%m%Y')

        time.sleep(2)

        url.sendKeys('//*[@id="mui-6"]', str(d2))

        for _ in range(5):
            try:
                time.sleep(1)
                alerta = url.switchToAlert()
                time.sleep(1)
                alerta.accept()
            except: 
                pass 

        url.clearText('//*[@id="mui-7"]')
        url.sendKeys('//*[@id="mui-7"]', str(d1))

        for _ in range(5):
            try:
                time.sleep(1)
                alerta = url.switchToAlert()
                time.sleep(1)
                alerta.accept()
            except:
                pass
            
        for file in os.listdir(DOWNLOAD_PATH):
            if 'Relatorio Alertas.xlsx' in file:
                try:
                    df = pd.read_excel(os.path.join(DOWNLOAD_PATH, file))
                except Exception as e:
                    print(e)
                df = df.drop_duplicates(subset='Placa')
                for _, linha in df.iterrows():
                    x = 0
                    while x == 0:
                        try:
                            placa = linha['Placa']
                            url.sendKeys('//*[@id="mui-5"]', placa)

                            url.pressKey('enter')

                            time.sleep(3)

                            url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

                            url.clearText('//*[@id="mui-5"]')

                            try:
                                os.mkdir(os.path.join(PLACAS_PATH, placa))
                            except:
                                for file in os.listdir(os.path.join(PLACAS_PATH, placa)):
                                    file_path = os.path.join(PLACAS_PATH, placa)
                                    os.remove(os.path.join(file_path, file))

                            for file_placa in os.listdir(DOWNLOAD_PATH):
                                if 'Relatorio Posicao' in file_placa:
                                    placa_folder = os.path.join(PLACAS_PATH, placa)
                                    shutil.move(os.path.join(DOWNLOAD_PATH, file_placa), os.path.join(placa_folder, f'{placa}.xlsx'))
                                    thread = Thread(target=ReportsFunctions.analyze_reports(placa))
                                    thread.start()

                            x = 1
                        except Exception as e:
                            print(f'Erro na placa {placa}')
                            print(str(e))
                            pass

        url.quitSite()

        time.sleep(3)
        for folder in os.listdir(PLACAS_PATH):
            if 'resultado' not in folder:
                os.remove(os.path.join(os.path.join(PLACAS_PATH, folder), f'{folder}.xlsx'))
                os.rmdir(os.path.join(PLACAS_PATH, folder))

    @staticmethod
    def extract_alert(date: str | None = None):
        '''
        Metodo utilizado para extrair o relatorio de alertas pernoite do Atlas 
        '''
        with open('paths.txt', mode='r', encoding='utf-8') as path_file:
            for row in path_file:
                if row.strip().split('=')[0] == 'USUARIO':
                    USUARIO = row.strip().split('=')[1]

                if row.strip().split('=')[0] == 'SENHA':
                    SENHA = row.strip().split('=')[1]


        url = Link(url='http://app-vibra.atlasgr.com.br/', driver='Chrome', sleep=1)

        url.openLink()

        url.maximize()

        url.sendKeys('//*[@id="mui-1"]', USUARIO )

        url.sendKeys('//*[@id="mui-2"]', SENHA )

        url.clickElement('//*[@id="__next"]/div[1]/div/div/div/div[2]/div/div/button')

        url.clickElement('//*[@id="__next"]/div[1]/div[1]/div[3]/div[3]/div[1]')

        url.clickElement('//*[@id="__next"]/div[1]/div[1]/div[3]/div[3]/div[2]/div[1]/div')

        #url.clickElement('//*[@id="relatorioLogistica"]/li[1]/a')

        time.sleep(5)

        url.switchWindow(1)
        
        url.clearField('//*[@id="mui-6"]')

        if not date:
            date = datetime.date.today() - datetime.timedelta(days=1)
            date = str(date.strftime('%d/%m/%Y'))

        url.clearText('//*[@id="mui-10"]')
        url.sendKeys('//*[@id="mui-10"]', date)

        url.clearText('//*[@id="mui-11"]')
        url.sendKeys('//*[@id="mui-11"]', date)

        time.sleep(2)

        url.sendKeys('//*[@id="mui-6"]','PERNOITE')

        url.pressKey('down')

        url.pressKey('enter')

        url.pressKey('enter')

        time.sleep(2)

        url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

        time.sleep(3)

        url.quitSite()


class ReportsFunctions:


    @staticmethod
    def analyze_reports(plate: str) -> None:
        '''
        Metodo que analisara o relatorio de posicoes e ira fazer o calculo de 8 horas descansadas
        '''
        # Cria o arquivo de resultados se não existir
        if not os.path.exists(os.path.join(PLACAS_PATH, 'resultado.xlsx')):
            df_result = pd.DataFrame(
                    columns = ['Placa', 'Status']
                )
            
            df_result.to_excel(os.path.join(PLACAS_PATH, 'resultado.xlsx'))

        if len(plate) == 7:
            placa_folder = os.path.join(PLACAS_PATH, plate) # Juntando a pasta de placas geral com a placa tirada da planilha de alerta
            file_path = os.path.join(placa_folder, str(plate) + '.xlsx') # Juntando o arquivo xlsx com a pasta da respectiva placa 
            df = pd.read_excel(file_path) # Lendo o relatorio de posicao para tranformar em um data frame

            dict_inicial = { # Dicionario criado para armazenar o index e data hora da primeira velocidade zerada 
                'data': None,
                'index': None
            }

            dict_final = { # Dicionario criado para armazenar index e data hota da ultima velocidade zerada
                'data': None,
                'index': None
            }

            dict_input = {
                'Placa': [plate],
                'Status': ['Não cumprido']
            }
                
            contador = 1 # Responsavel por fazer a comparacao do index para saber se temos uma sequencia de velocidade zerada 
            for index, row in df.iterrows():
                if row['Velocidade'] == 0: # Entra na condicao abaixo se a velocidade for zero
                    if not dict_inicial['data']: # Entra nessa condicao se o dict inicial nao estiver preenchido 
                        dict_inicial['data'] = row['Data']
                        dict_inicial['index'] = index

                    else: # Se o dict inicial estiver preenchido ele coleta o index e data hora da ultima velocidade zerada 
                        if index - contador == dict_inicial['index']: # Compara para saber se temos uma sequencia de velocidade zerada
                            contador += 1
                            dict_final['data'] = row['Data']
                            dict_final['index'] = index

                elif row['Velocidade'] <= 10 and row['Velocidade'] > 0:
                    if dict_inicial['data']:
                        if index - contador == dict_inicial['index']:
                            contador += 1
                            dict_final['data'] = row['Data']
                            dict_final['index'] = index

                else: # Entra na condicao abaixo se a velocidade for maior que zero 
                    if dict_inicial['data'] and dict_final['data']: # Armazena a data hora da primeira e ultima velocidade zerada 
                        calc_insterticio = datetime.datetime.strptime(dict_final['data'], '%d/%m/%Y-%H:%M:%S') - \
                            datetime.datetime.strptime(dict_inicial['data'], '%d/%m/%Y-%H:%M:%S')
                            # Convertendo a data hora da planilha para datetime e fazendo o calculo de data final - data inicial 
                            
                        horas_realizadas = calc_insterticio.total_seconds() / 3600 # O resultado total de segundos sera divido por 3600s

                        if horas_realizadas > 8.0 or df['CPF'].nunique() > 1: # Define o status como cumprido
                            dict_input['Status'] = 'Cumprido'                      

                    # Zera após fazer a comparação e o contador 
                    dict_inicial['data'] = None
                    dict_inicial['index'] = None

                    dict_final['data'] = None
                    dict_final['index'] = None
                    contador = 1

            df_result = pd.read_excel(os.path.join(PLACAS_PATH, 'resultado.xlsx'))

            df_main = pd.DataFrame(
                dict_input
            )
                        
            df_result = pd.concat([df_result, df_main])
            df_result = df_result[['Placa', 'Status']]
            df_result.to_excel(os.path.join(PLACAS_PATH, 'resultado.xlsx'))
                        
    @staticmethod
    def analyze_reports_manual(plate: str) -> None:
        '''
        Método para analisar manualmente uma placa e validar a mesma, desenvolvida apenas para teste
        '''

        if len(plate) == 7:
            placa_folder = os.path.join(PLACAS_PATH, plate) # Juntando a pasta de placas geral com a placa tirada da planilha de alerta
            file_path = os.path.join(placa_folder, str(plate) + '.xlsx') # Juntando o arquivo xlsx com a pasta da respectiva placa 
            df = pd.read_excel(file_path) # Lendo o relatorio de posicao para tranformar em um data frame
            dict_inicial = { # Dicionario criado para armazenar o index e data hora da primeira velocidade zerada 
                'data': None,
                'index': None
            }

            dict_final = { # Dicionario criado para armazenar index e data hota da ultima velocidade zerada
                'data': None,
                'index': None
            }

            dict_input = {
                'Placa': [plate],
                'Status': ['Não cumprido']
            }
                
            contador = 1 # Responsavel por fazer a comparacao do index para saber se temos uma sequencia de velocidade zerada 
            for index, row in df.iterrows():
                if row['Velocidade'] == 0: # Entra na condicao abaixo se a velocidade for zero
                    if not dict_inicial['data']: # Entra nessa condicao se o dict inicial nao estiver preenchido 
                        dict_inicial['data'] = row['Data']
                        dict_inicial['index'] = index

                    else: # Se o dict inicial estiver preenchido ele coleta o index e data hora da ultima velocidade zerada 
                        if index - contador == dict_inicial['index']: # Compara para saber se temos uma sequencia de velocidade zerada
                            contador += 1
                            dict_final['data'] = row['Data']
                            dict_final['index'] = index

                else: # Entra na condicao abaixo se a velocidade for maior que zero 
                    if dict_inicial['data'] and dict_final['data']: # Armazena a data hora da primeira e ultima velocidade zerada 
                        calc_insterticio = datetime.datetime.strptime(dict_final['data'], '%d/%m/%Y-%H:%M:%S') - \
                            datetime.datetime.strptime(dict_inicial['data'], '%d/%m/%Y-%H:%M:%S')
                            # Convertendo a data hora da planilha para datetime e fazendo o calculo de data final - data inicial 
                            
                        horas_realizadas = calc_insterticio.total_seconds() / 3600 # O resultado total de segundos sera divido por 3600s

                        if horas_realizadas > 8.0 or df['CPF'].nunique() > 1: # Define o status como cumprido
                            dict_input['Status'] = 'Cumprido'

                        print(f'Index inicial: {dict_inicial["index"]}    Data inicial: {dict_inicial["data"]}')
                        print(f'Index final: {dict_final["index"]}    Data final: {dict_final["data"]}') 
                        print(f'Horas de descanso realizadas: {horas_realizadas}') 
                        print('\n')                  

                    # Zera após fazer a comparação e o contador 
                    dict_inicial['data'] = None
                    dict_inicial['index'] = None

                    dict_final['data'] = None
                    dict_final['index'] = None
                    contador = 1

    @staticmethod
    def insert_result(d1: str | None = None, d2: str | None = None) -> None:
        for file in os.listdir(PLACAS_PATH):
            if 'resultado' in file:
                try:
                    if not d2:
                        d2 = datetime.date.today() - datetime.timedelta(days=1)
                        d2 = str(d2.strftime('%Y-%m-%d'))

                    if not d1:
                        d1 = datetime.date.today() - datetime.timedelta(days=1)
                        d1 = str(d1.strftime('%Y-%m-%d'))

                    df = pd.read_excel(os.path.join(PLACAS_PATH, file))
                    df['dt_insercao'] = datetime.date.today()
                    df['chave'] = df.apply(lambda x: f'{x["Placa"]}-{x["dt_insercao"]}', axis=1)
                    df['d1'] = d1
                    df['d2'] = d2
                    
                    con = psycopg2.connect(host='4.228.57.67', database='db_vibra', user='postgres', password=POSTGRE_PASSWORD)
                    cur = con.cursor()

                    values = df[
                        [
                            'chave',
                            'Placa',
                            'Status',
                            'dt_insercao',
                            'd1',
                            'd2',
                        ]
                    ]

                    values = [tuple(row) for row in values.values]

                    columns = [
                        'chave',
                        'placa',
                        'status',
                        'dt_insercao',
                        'dt_analise_1',
                        'dt_analise_2',
                    ]

                    initial_command = f'''
                        INSERT INTO sc_diversos.tb_intersticio ({', '.join(columns)})
                        VALUES ({', '.join(['%s'] * len(columns))})
                        ON CONFLICT (chave) DO NOTHING;
                    '''

                    cur.executemany(initial_command, values)

                    update_command = f'''
                        INSERT INTO sc_diversos.tb_intersticio ({', '.join(columns)})
                        VALUES ({', '.join(['%s'] * len(columns))})
                        ON CONFLICT (chave) DO UPDATE
                        SET {', '.join([f"{column} = excluded.{column}" for column in columns])};
                    '''

                    cur.executemany(update_command, values)

                    con.commit()
                    
                except Exception as e:
                    print(e)
                finally:
                    cur.close()
                    con.close()

