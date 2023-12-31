import time
import datetime
from link.app.link import Link

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

    time.sleep(2)
    url.sendKeys('//*[@id="mui-6"]', str(d2))

    for i in range(5):
        try:
            alerta = url.switchToAlert()
            alerta.accept()
        except: 
            pass 
        
        time.sleep(2)
        url.clearText('//*[@id="mui-7"]')
        url.sendKeys('//*[@id="mui-7"]', str(d1))

        for i in range(5):
            try:
                alerta = url.switchToAlert()
                alerta.accept()
            except:
                pass
        
        url.sendKeys('//*[@id="mui-5"]', placa)

        url.clickElement('//*[@id="__next"]/div[1]/form/button')

        time.sleep(10)

        url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

        url.quitSite()
