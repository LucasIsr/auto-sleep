from link import Link
import datetime
import time

url = Link('https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', 'Chrome', sleep=4, headless=False)

url.openLink()

url.maximize()

url.sendKeys('//*[@id="edtEmpresa"]', 'Atlasbr')

url.sendKeys('//*[@id="edtUsuario"]','49660821883')

url.sendKeys('//*[@id="edtSenha"]','moby123')

url.clickElement('//*[@id="frmPai"]/div/div[4]/div/i')

url.clickElement('//*[@id="botaologistica"]/a')

url.clickElement('//*[@id="logistica"]/li[2]/a')

url.clickElement('//*[@id="relatorioLogistica"]/li[1]/a')

url.switchWindow(1)

url.sendKeys('//*[@id="mui-9"]','FVS5B06')

time.sleep(300)

