from link import Link
import datetime
import time

date_hour = datetime.datetime.now()
date_hour_formated = date_hour.strftime('%d/%m/%Y %H:%M:%S')


url = Link('https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', 'Chrome', sleep=4, headless=False)

url.openLink()

url.maximize()

url.sendKeys('//*[@id="edtEmpresa"]', 'Atlasbr')

url.sendKeys('//*[@id="edtUsuario"]','12345678922')

url.sendKeys('//*[@id="edtSenha"]','moby123')

url.clickElement('//*[@id="frmPai"]/div/div[4]/div/i')

url.clickElement('//*[@id="botaologistica"]/a/span[1]')

url.clickElement('//*[@id="logistica"]/li[2]/a')

url.clickElement('//*[@id="relatorioLogistica"]/li[1]/a')

time.sleep(300)

