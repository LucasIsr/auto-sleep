from link import Link
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

time.sleep(2)

url.switchWindow(1)

url.sendKeys('//*[@id="mui-6"]','PERNOITE')

url.pressDown()

url.pressEnter()

url.clickElement('//*[@id="__next"]/div[1]/form/button')

time.sleep(2)

url.clickElement('//*[@id="__next"]/div[2]/div/div/div[1]/div/div/button[1]')

time.sleep(2)

url.quitSite(1)

time.sleep(300)

