# import requests
from bs4 import BeautifulSoup
# import csv
import os
import sys
import time
# import http.client
# import random
import datetime
# import traceback
# import json
# import xlrd
# import xlsxwriter
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import NoSuchElementException
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
    phrases = []
    sorts = []
    verbs = []
    dt_ranges = []
    with open(i_name, 'r', encoding='utf-8') as f:
        lst = f.read()
    if lst[0] == '\ufeff':
        # print('Gocha!')
        lst = lst[1:]
    lst = [p.strip() for p in lst.splitlines()]
    lst = list(filter(None, lst))
    for p in lst:
        verbs.append(False)
        dt_ranges.append([None, None])
        phrases.append(p)
        sorts.append(False)
        if p.find(' SORT:D') >= 0:
            sorts[-1] = True
            phrases[-1] = p[:p.find(' SORT:D')]
            p = p.replace(' SORT:D', '')
        if p.find(' VERBATIM:1') >= 0:
            verbs[-1] = True
            phrases[-1] = p[:p.find(' VERBATIM:1')]
            p = p.replace(' VERBATIM:1', '')
        if p.find(' DTRANGE:') >= 0:
            phrases[-1] = p[:p.find(' DTRANGE:')]
            tmp = p[p.find(' DTRANGE:')+9:]
            if tmp.startswith('last'):
                tmp2 = tmp.split(' ')
                dt_ranges[-1][0] = tmp2[-1]
                dt_ranges[-1][1] = tmp2[-2]
            else:
                dt_ranges[-1][0] = 'range'
                dt_ranges[-1][1] = tmp

    phrases = [p.replace(' ', '+') for p in phrases]

    # for p, v, d in zip(phrases, verbs, dt_ranges):
    #     print(p, v, d, flush=True)
    # print((phrases, verbs, dt_ranges))
    # sys.exit('here')

    # phrases = [p.split(' ') for p in phrases]
    # phrases = ['+'.join(p) for p in phrases]
    # print(phrases)

    return phrases, sorts, verbs, dt_ranges

def get_info(driver: webdriver.Chrome, url: str, delay: float):
    types, links, headings, add_links, add_headings = [], [], [], [], []

    driver.get(url)
    time.sleep(delay)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # s = soup.find('a')
    '''div id="center_col"'''
    center = soup.find('div', id='center_col')
    [s.extract() for s in soup('ol') if s.find('a') and 'webcache' in s.find('a').get('href')]  #.startswith('http://webcache')]  # =='Cached']

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

def main_process(phrases, sorts, verbs, dt_ranges, headless, delay, local, country, lang_res, lang_int):
    centers = []
    headless = headless or False  # default options
    delay = delay or 1
    driver, wait = init_driver(headless, delay)
    '''&cr=countryRU&lr=lang_uk&hl=ru'''
    g_url = 'https://www.google.com.au/search?q={text}&cr=country{c}&lr=lang_{lr}&hl={li}&ie=UTF-8&num=20'
    g_main = 'https://www.google.com.au/search?q={text}&ie=UTF-8&num=20'
    # suf_site = '&as_sitesearch='

    for i, (phrase, s, v, dt) in enumerate(zip(phrases, sorts, verbs, dt_ranges)):
        # print(phrase)
        # print()
        if not local:
            url = g_url.format(text=phrase, c=country, lr=lang_res, li=lang_int)
        else:
            url = g_main.format(text=phrase)

        if v:
            url = url + '&tbs=li:1'
        if dt[0]:
            if dt[0] == 'range':
                r = dt[1].split('-')
                url = url + '&tbs=cdr:1,cd_min:{s},cd_max:{f}'.format(s=r[0], f=r[1])
            elif dt[0].startswith('se'):
                url = url + '&tbs=qdr:s{s}'.format(s=dt[1])
            elif dt[0].startswith('mi'):
                url = url + '&tbs=qdr:n{s}'.format(s=dt[1])
            elif dt[0].startswith('ho'):
                url = url + '&tbs=qdr:h{s}'.format(s=dt[1])
            elif dt[0].startswith('da'):
                url = url + '&tbs=qdr:d{s}'.format(s=dt[1])
            elif dt[0].startswith('we'):
                url = url + '&tbs=qdr:w{s}'.format(s=dt[1])
            elif dt[0].startswith('mo'):
                url = url + '&tbs=qdr:m{s}'.format(s=dt[1])
            elif dt[0].startswith('ye'):
                url = url + '&tbs=qdr:y{s}'.format(s=dt[1])
        if s:
            if '&tbs=' not in url:
                url = url + '&tbs=sbd:1'  # '&sort=date'#
            else:
                url = url + ',sbd:1'
        center = get_info(driver, url, delay)
        centers.append(center)
        # input('wait:')

    driver.stop_client()
    driver.close()
    driver.quit()

    return centers

def send_mail(centers: list, phrases: list, sorts: list, verbs: list, dt_ranges: list, sender, login, password, receiver, subject):  # (links: list, headings: list):
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
    header = '<h1><b>Search {n}: {phrase}</b></h1><i>{s}{v}{d}</i><br><br>'
    body = ''
    for i, (phrase, s, v, dt, center) in enumerate(zip(phrases, sorts, verbs, dt_ranges, centers)):
        tmp = phrase.split('+')
        text = ' '.join(tmp)
        s_text = ' Sorted by Relevance;'
        v_text = ' Verbatim: 0;'
        d_text = ''
        if s:
            s_text = ' Sorted by Date;'
        if v:
            v_text = ' Verbatim: 1;'
        if dt[0]:
            if dt[0] == 'range':
                d_text = ' Dates: ' + dt[1] + ';'
            else:
                d_text = ' Last ' + dt[1] + ' ' + dt[0] + ';'
        body = body + header.format(n=i+1, s=s_text, v=v_text, d=d_text, phrase=text) + str(center)
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

    headless, delay, local, country, lang_res, lang_int, sender, login, password, receiver, subject = open_setting(s_name)
    phrases, sorts, verbs, dt_ranges = input_phrases(i_name)
    centers = main_process(phrases, sorts, verbs, dt_ranges, headless, delay, local, country, lang_res, lang_int)
    send_mail(centers, phrases, sorts, verbs, dt_ranges, sender, login, password, receiver, subject)

'''https://myaccount.google.com/lesssecureapps
https://myaccount.google.com/u/2/lesssecureapps
allow less secure apps access to SMPT server'''
