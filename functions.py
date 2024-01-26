import time
import datetime
from link.app.link import Link
import os
import shutil
import pandas as pd



DOWNLOAD_PATH = r'/Users/fanecovsf/Downloads'
PLACAS_PATH = r'/Users/fanecovsf/Downloads/placas' 


class AtlasFunctions:


    @staticmethod
    def extract_position(placa):
        url = Link(url='https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', driver='Chrome', sleep=1)

        url.openLink()

        url.maximize()

        url.sendKeys('//*[@id="edtEmpresa"]', 'Atlasbr')

        url.sendKeys('//*[@id="edtUsuario"]','49660821883')

        url.sendKeys('//*[@id="edtSenha"]','Lk206049')

        url.clickElement('//*[@id="frmPai"]/div/div[4]/div/i')

        url.clickElement('//*[@id="botaologistica"]/a')

        url.clickElement('//*[@id="logistica"]/li[2]/a')

        url.clickElement('//*[@id="relatorioLogistica"]/li[3]/a')

        time.sleep(3)

        url.switchWindow(1)

        url.clearText('//*[@id="mui-6"]')

        d2 = datetime.date.today() - datetime.timedelta(days=2)
        d2 = d2.strftime('%d%m%Y')
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
            
        url.sendKeys('//*[@id="mui-5"]', placa)

        url.pressKey('enter')

        time.sleep(10)

        url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

        url.quitSite()

    @staticmethod
    def extract_alert():
        url = Link(url='https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', driver='Chrome', sleep=1)

        url.openLink()

        url.maximize()

        url.clearField('//*[@id="edtEmpresa"]')

        url.sendKeys('//*[@id="edtEmpresa"]', 'ATLASBR')

        url.sendKeys('//*[@id="edtUsuario"]','49660821883')

        url.sendKeys('//*[@id="edtSenha"]','Lk206049')

        url.clickElement('//*[@id="frmPai"]/div/div[4]/div/i')

        url.clickElement('//*[@id="botaologistica"]/a')

        url.clickElement('//*[@id="logistica"]/li[2]/a')

        url.clickElement('//*[@id="relatorioLogistica"]/li[1]/a')

        time.sleep(2)

        url.switchWindow(1)

        url.clearField('//*[@id="mui-6"]')

        d2 = datetime.date.today() - datetime.timedelta(days=2)
        d2 = str(d2.strftime('%d/%m/%Y'))
        url.clearText('//*[@id="mui-10"]')
        url.sendKeys('//*[@id="mui-10"]', d2)

        d1 = datetime.date.today() - datetime.timedelta(days=1)
        d1 = str(d1.strftime('%d/%m/%Y'))
        url.clearText('//*[@id="mui-11"]')
        url.sendKeys('//*[@id="mui-11"]', d1)

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
    def extract_all_reports():
        """
        Função usada para extrair todos os relatórios por placa, essa função já ira acionar a função 'extract_position' da AtlasFunctions
        """

        # Inicia a extração por placa
        for file in os.listdir(DOWNLOAD_PATH):
            if 'Relatorio Alertas.xlsx' in file:
                df = pd.read_excel(os.path.join(DOWNLOAD_PATH, file))
                df = df.drop_duplicates(subset='Placa')
                for _, linha in df.iterrows():
                    placa = linha['Placa']
                    print(f'Iniciando extração da placa {placa}')
                    AtlasFunctions.extract_position(placa)

                    try:
                        os.mkdir(os.path.join(PLACAS_PATH, placa))
                    except:
                        for file in os.listdir(os.path.join(PLACAS_PATH, placa)):
                            file_path = os.path.join(PLACAS_PATH, placa)
                            os.remove(os.path.join(file_path, file))

                    for file_placa in os.listdir(DOWNLOAD_PATH):
                        if 'Relatorio Posicao.xlsx' in file_placa:
                            placa_folder = os.path.join(PLACAS_PATH, placa)
                            shutil.move(os.path.join(DOWNLOAD_PATH, file_placa), os.path.join(placa_folder, f'{placa}.xlsx'))
                            print(f'Placa {placa} extraída com sucesso')

    @staticmethod
    def analyze_reports():
        for folder in os.listdir(PLACAS_PATH):
            status_instersticio = 'Não cumprido'
            placa_folder = os.path.join(PLACAS_PATH, folder)
            file_path = os.path.join(placa_folder, str(folder) + '.xlsx')
            df = pd.read_excel(file_path)

            dict_inicial = {
                'data': None,
                'index': None
            }

            dict_final = {
                'data': None,
                'index': None
            }
            
            contador = 1
            for index, row in df.iterrows():
                if row['Velocidade'] == 0:
                    if not dict_inicial['data']:
                        dict_inicial['data'] = row['Data']
                        dict_inicial['index'] = index

                    else:
                        if index - contador == dict_inicial['index']:
                            contador += 1
                            dict_final['data'] = row['Data']
                            dict_final['index'] = index

                else:
                    if dict_inicial['data'] and dict_final['data']:
                        calc_insterticio = datetime.datetime.strptime(dict_final['data'], '%d/%m/%Y-%H:%M:%S') - \
                            datetime.datetime.strptime(dict_inicial['data'], '%d/%m/%Y-%H:%M:%S')
                        
                        horas_realizadas = calc_insterticio.total_seconds() / 3600

                        print(f'Horas cumpridas da placa {folder}: {horas_realizadas}')

                        if horas_realizadas > 8.0:
                            status_instersticio = 'Cumprido'

                        # Zera após fazer a comparação
                        dict_inicial['data'] = None
                        dict_inicial['index'] = None

                        dict_final['data'] = None
                        dict_final['index'] = None

            print(f'Status interstício da placa {folder}: {status_instersticio}')
            print('------------------------------------')
                        




