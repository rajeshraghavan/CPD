# Xpath and CSS element are for Welcome string within the CPD portal
# Script will initiate a login
from selenium import webdriver
import requests
import time
import smtplib
from datetime import datetime
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(recipients):
    SENDER = 'cp4d_prd@illumina.com'
    SENDERNAME = 'DEV IBM Cloud Pak for Data'
    RECIPIENT = recipients
    HOST = "smtp.illumina.com"
    PORT = 25
    SUBJECT = 'Login to http://dspdev.illumina.com Failed!'
    BODY_HTML = """<html>
            <head></head>
            <body>                  
              <h1>Login to DSP DEV Failed:</h1>
              <h2>Please Check CP4D URL <a href='https://dspdev.illumina.com'>https://dspdev.illumina.com</a></h2>                  
            </body>
            </html>"""
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = email.utils.formataddr((SENDERNAME, SENDER))
    msg['To'] = RECIPIENT

    part2 = MIMEText(BODY_HTML, 'html')
    msg.attach(part2)

    try:
        server = smtplib.SMTP(HOST, PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.sendmail(SENDER, RECIPIENT, msg.as_string())
        server.close()

    except Exception as e:
        print("Error: ", e)
    else:
        print("Notification Email Sent!")

class FindByXPathCSS():

    def test(self):
        baseUrl = "https://dspdev1.illumina.com"
        driver = webdriver.Chrome()
        driver.get(baseUrl)
        driver.implicitly_wait(10)
        elementByXpath = driver.find_element_by_xpath("/html//div[@id='app']/div/div[@class='pageContainer']/div[@class='HomepageContainer__homepage--1tLjx']//h1[@class='Welcome__title--AIf-a']")

        if elementByXpath is not None:
            print("The string element Welcome was found in XPATH")

        elementbycss = driver.find_element_by_css_selector(".Welcome__title--AIf-a")

        if elementbycss is not None:
            print("We found an element by CSS")

        '''ending_time = time.time()
        elapsed_time = str(ending_time - initial_time)
        print('The Round Trip Time for {} is {}'.format(url, elapsed_time))'''

    def endTest(self):
        driver = webdriver.Chrome()
        driver.close()

#################
# Main
#################

recipients = "GIS.BI.Admins@p1.illumina.xmatters.com"
#recipients = "rraghavan@illumina.com"
url_check = FindByXPathCSS()
url = "https://dspdev.illumina.com"
counter = 0
try:
    initial_time = time.time()
    url_check.test()
    ending_time = time.time()
    elapsed_time = str(ending_time - initial_time)
    print('The Round Trip Time for {} is {} seconds'.format(url, elapsed_time))
    url_check.endTest()
    exit(0)
except Exception as msg:
    while counter < 3:
        print("Unable to reach the URL, trying again after 20 seconds")
        time.sleep(20)
        counter += 1
        continue
    print("Unable to reach the URL after 3 tries")
    send_mail(recipients)
    url_check.endTest()
    exit(1)
else:
    url_check.endTest()
    exit(0)