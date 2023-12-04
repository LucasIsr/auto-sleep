from link import Link
import datetime
import time

url = Link('https://connect.atlasgr.com.br/portalatlas/Atlas_Login.php', 'Chrome', sleep=4, headless=False)

url.openLink()

url.maximize()

url.sendKeys('//*[@id="edtEmpresa"]', 'Atlasbr')

url.sendKeys('//*[@id="edtUsuario"]','12345678922')

url.sendKeys('//*[@id="edtSenha"]','moby123')

url.clickElement('//*[@id="frmPai"]/div/div[4]/div/i')