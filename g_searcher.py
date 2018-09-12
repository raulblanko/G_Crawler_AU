import requests
from bs4 import BeautifulSoup
import csv
import os
import sys
import time
import http.client
import random
import datetime
import traceback
import json
import xlrd
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import demjson
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# initialization of Chrome webdriver
def init_driver(headless, delay):
    chrome_options = Options()
    chrome_options.add_argument('--dns-prefetch-disable')
    chrome_options.add_argument('log-level=3')
    chrome_options.set_headless(headless)
    driver = webdriver.Chrome('chromedriver.exe', chrome_options=chrome_options)
    wait = WebDriverWait(driver, delay)
    driver.set_window_rect(280, 10, 1050, 720)
    # driver.get('https://www.google.com/preferences?')
    # ans = input('Press Enter after you make changes: ')
    return driver, wait

def input_phrases(i_name):
    # phrases = []
    with open(i_name, 'r', encoding='utf-8') as f:
        lst = f.read().splitlines()
    phrases = [p.strip() for p in lst]
    phrases = list(filter(None, phrases))
    phrases = [p.split(' ') for p in phrases]
    phrases = ['+'.join(p) for p in phrases]
    print(phrases)
    return phrases

def get_info(driver: webdriver.Chrome, url: str, delay: float):
    types, links, headings, add_links, add_headings = [], [], [], [], []

    driver.get(url)
    time.sleep(delay)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # s = soup.find('a')
    '''div id="center_col"'''
    center = soup.find('div', id='center_col')

    return center
    # '''div id="taw"
    #
    # '''
    # '''div id='search'''
    # '''div id="bottomads"'''
    # frames = soup.find_all('div', class_='bkWMgd')
    # n = 0
    # for frame in frames:
    #     all_h3 = frame.find_all('h3', class_='r')
    #     all_divs = frame.find_all('div', class_='s')
    #     print(len(all_h3), len(all_divs), len(all_h3)==len(all_divs))
    #     for h3 in all_h3:
    #         a = h3.find('a')
    #         links.append(a.get('href'))
    #         n += 1
    #         print(n, links[-1])
    #
    #     for div in all_divs:
    #         sp = div.find('span', class_='st')
    #         headings.append(sp.get_text())
    #         print('\t', headings[-1])
    #
    # return links, headings

def save_settings(name):
    sets = {'headless': False,
            'delay': 1,
            'country': 'AU',
            'results_language': 'EN',
            'interface_language': 'EN',
            'from': 'pavlo.beliaev@gmail.com',
            'login': 'pavlo.beliaev',
            'password': 'the_password',
            'to': 'a.agency@ukr.net',
            'subject': 'google search',
            }
    with open(name, 'w', encoding='utf-8') as f:
        print(demjson.encode(sets, strict=False, compactly=False, sort_keys=demjson.SORT_NONE), file=f)

def open_setting(name):
    if name not in os.listdir():
        sys.exit(no_input.format(name=name))
    with open(name, 'r', encoding='utf-8') as f:
        sets = demjson.decode(f.read(), strict=False)

    return sets.values()

def main_process(phrases, headless, delay, country, lang_res, lang_int):
    centers = []
    headless = headless or False  # default options
    delay = delay or 1
    country = country or 'AU'
    lang_res = lang_res or 'EN'
    lang_int = lang_int or 'EN'
    driver, wait = init_driver(headless, delay)
    '''&cr=countryRU&lr=lang_uk&hl=ru'''
    g_url = 'https://www.google.com/search?q={text}&cr=country{c}&lr=lang_{lr}&hl={li}&num=20'

    for i, phrase in enumerate(phrases):
        print(phrase)
        print()
        url = g_url.format(text=phrase, c=country, lr=lang_res, li=lang_int)
        # links, headings = get_info(driver, url, delay)
        center = get_info(driver, url, delay)
        centers.append(center)
        # input('wait:')

    driver.stop_client()
    driver.close()
    driver.quit()

    return centers, phrases

def send_mail(centers: list, phrases: list, sender, login, password, receiver, subject):  # (links: list, headings: list):
    # sender = "beliaev.pavlo@gmail.com"
    # receiver = "a.agency@ukr.net"
    td = datetime.datetime.today()

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject + td.strftime(' at %Y.%m.%d %H:%M:%S')
    msg['From'] = sender
    msg['To'] = receiver

    start = '''\
    <html>
      <head></head>
      <body>'''
    end = '''  </body>
    </html>'''
    header = '<h1>Search {n}: {phrase}</h1><br><br>'
    body = ''
    for i, (phrase, center) in enumerate(zip(phrases, centers)):
        tmp = phrase.split('+')
        text = ' '.join(tmp)
        body = body + header.format(n=i, phrase=text) + str(center)
    html = start + body + end
    letter = MIMEText(html, 'html')
    msg.attach(letter)

    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login(login, password)
    mail.sendmail(sender, receiver, msg.as_string())
    mail.quit()


i_name = 'keywords.txt'
s_name = 'settings.txt'
no_input = "Missing '{name}' in current folder"

if __name__=='__main__':

    headless, delay, country, lang_res, lang_int, sender, login, password, receiver, subject = open_setting(s_name)
    phrases = input_phrases(i_name)
    centers, phrases = main_process(phrases, headless, delay, country, lang_res, lang_int)
    send_mail(centers, phrases, sender, login, password, receiver, subject)

'''https://myaccount.google.com/lesssecureapps
https://myaccount.google.com/u/2/lesssecureapps
allow less secure apps access to SMPT server'''
