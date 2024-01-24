import time
import datetime
from link.app.link import Link
import os
import shutil
import pandas as pd



DOWNLOAD_PATH = r'C:\Users\lucas\Downloads'
PLACAS_PATH = r'C:\Users\lucas\Downloads' 


class AtlasFunctions:


    @staticmethod
    def extract_position(placa):
        url = Link(link='https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', driver='Chrome', sleep=1, headless=False, driver_path='chromedriver.exe')

        url.openLink()

        url.maximize()

        url.sendKeys('//*[@id="edtEmpresa"]', 'Atlasbr')

        url.sendKeys('//*[@id="edtUsuario"]','49660821883')

        url.sendKeys('//*[@id="edtSenha"]','moby123')

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

        for i in range(5):
            try:
                time.sleep(1)
                alerta = url.switchToAlert()
                time.sleep(1)
                alerta.accept()
            except: 
                pass 
            

        url.clearText('//*[@id="mui-7"]')
        url.sendKeys('//*[@id="mui-7"]', str(d1))

        for i in range(5):
            try:
                time.sleep(1)
                alerta = url.switchToAlert()
                time.sleep(1)
                alerta.accept()
            except:
                pass
            
        url.sendKeys('//*[@id="mui-5"]', placa)

        url.clickElement('//*[@id="__next"]/div[1]/form/button')

        time.sleep(10)

        url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

        url.quitSite()

    @staticmethod
    def extract_alert():
        url = Link(link='https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', driver='Chrome', sleep=1, headless=False, driver_path='chromedriver.exe')

        url.openLink()

        url.maximize()

        url.sendKeys('//*[@id="edtEmpresa"]', 'Atlasbr')

        url.sendKeys('//*[@id="edtUsuario"]','49660821883')

        url.sendKeys('//*[@id="edtSenha"]','moby123')

        url.clickElement('//*[@id="frmPai"]/div/div[4]/div/i')

        url.clickElement('//*[@id="botaologistica"]/a')

        url.clickElement('//*[@id="logistica"]/li[2]/a')

        url.clickElement('//*[@id="relatorioLogistica"]/li[1]/a')

        time.sleep(2)

        url.switchWindow(1)

        url.clearText('//*[@id="mui-6"]')

        d2 = datetime.date.today() - datetime.timedelta(days=2)
        d2 = str(d2.strftime('%d%m%Y'))
        url.clearText('//*[@id="mui-10"]')
        url.sendKeys('//*[@id="mui-10"]', d2)

        d1 = datetime.date.today() - datetime.timedelta(days=1)
        d1 = str(d1.strftime('%d/%m/%Y'))
        url.clearText('//*[@id="mui-11"]')
        url.sendKeys('//*[@id="mui-11"]', d1)

        time.sleep(2)

        url.sendKeys('//*[@id="mui-6"]','PERNOITE')

        url.pressDown()

        url.pressEnter()

        url.clickElement('//*[@id="__next"]/div[1]/form/button')

        time.sleep(2)

        url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

        time.sleep(3)

        url.quitSite()


class ReportsFunctions:


    @staticmethod
    def extract_all_reports():
        for file in os.listdir(DOWNLOAD_PATH):
            if 'Relatorio Alertas.xlsx' in file:
                df = pd.read_excel(os.path.join(DOWNLOAD_PATH, file))
                df = df.drop_duplicates(subset='Placa')
                for _, linha in df.iterrows():
                    placa = linha['Placa']
                    AtlasFunctions.extract_position(placa)
                    os.mkdir(os.path.join(PLACAS_PATH, placa))
                    for file_placa in os.listdir(DOWNLOAD_PATH):
                        if 'Relatorio Posicao.xlsx' in file_placa:
                            placa_folder = PLACAS_PATH + f'\{placa}'
                            shutil.move(os.path.join(DOWNLOAD_PATH, file_placa), os.path.join(placa_folder, f'{placa}.xlsx'))

    @staticmethod
    def analyze_reports():
        for folder in os.listdir(PLACAS_PATH):
            placa_folder = os.path.join(PLACAS_PATH, folder)
            file_path = os.path.join(placa_folder, str(folder) + '.xlsx')
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                if row['Velocidade'] == 0:
                    print(row['Velocidade'])
                    print(row['Data'])
                    time.sleep(0.5)
ReportsFunctions.analyze_reports()