import os.path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders

from selenium.webdriver import Chrome
from selenium.webdriver import PhantomJS

from selenium import webdriver

import time

_user = "mi_xi_shi_zi@163.com"
_pwd  = "liaozhou1998"
_to   = "liaozhou98@kindle.cn"

_url = 'https://theeconomist.ctfile.com/dir/15138480-24778641-46296f/'
_files = ['20180414.mobi','20180421.mobi','20180428.mobi']

def get_book(url, file):
	options = webdriver.ChromeOptions()
	prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'C:/Users/liaoz/Desktop/The Economist/'}
	options.add_experimental_option('prefs', prefs)

	# driver = PhantomJS()
	driver = Chrome(chrome_options=options)
	driver.get(url)

	link = driver.find_element_by_link_text(file)
	link_url = link.get_attribute("href")
	# print(link_url)
	driver.get(link_url)
	driver.find_element_by_id('free_down_link').click()

	time.sleep(100)
	driver.quit()

def send_email(filename):
	msg = MIMEMultipart()
	msg['Subject'] = 'convert'  #邮件标题
	msg['From'] = _user #显示发件人
	msg['To'] = _to #接收邮箱
	s = smtplib.SMTP_SSL("smtp.163.com", 465,timeout = 30)#连接smtp邮件服务器,qq邮箱端口为465
	basename = os.path.basename(filename) 
	print(basename)
	fp = open(filename,'rb')
	att = MIMEText(fp.read(),'base64','gbk')
	att['Content-Type'] = 'application/octer-stream'
	att.add_header('Content-Disposition', 'attachment',filename=('gbk', '', basename))
	encoders.encode_base64(att)
	msg.attach(att)
	s.login(_user, _pwd)#登陆服务器
	s.sendmail(_user, _to, msg.as_string())#发送邮件
	s.close()

def main():
	for _file in _files:
		get_book(_url, _file)
		send_email(_file)

if __name__ == '__main__':
	main()