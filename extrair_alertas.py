from link.app.link import Link
import time
import datetime

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
    d2 = d2.strftime('%d%m%Y')
    d1 = datetime.date.today() - datetime.timedelta(days=1)
    d1 = d1.strftime('%d/%m/%Y')

    time.sleep(2)

    url.sendKeys('//*[@id="mui-6"]','PERNOITE')

    url.pressDown()

    url.pressEnter()

    url.clickElement('//*[@id="__next"]/div[1]/form/button')

    time.sleep(2)

    url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

    time.sleep(3)

    url.quitSite()

