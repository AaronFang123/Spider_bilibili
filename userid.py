# -*- coding: utf-8 -*
# input:one key world to search
# output:the uid(Str,remarks a user) and the nickname(Str) of the user
# entry: search_ID(keyword)

# Original version:11,1,2019

import requests
import bs4
import re
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()


def search_ID(nickname):
    try:
        print 'finding:{}'.format(nickname)
    except UnicodeDecodeError:
        nickname = nickname.decode(sysencoding, "ignore").encode(sysencoding, "ignore")
        print 'finding:{}'.format(nickname)
    nickname = nickname.decode(sysencoding, "ignore").encode(sysencoding, "ignore")
    url = 'https://search.bilibili.com/upuser?keyword={}'.format(nickname)

    print url

    try:
        reponse = requests.get(url)
        if reponse.status_code == 200:
            print 'got search result page'
            uid, target_name = __get_space_url_name(reponse.text, nickname)
            return uid, target_name
    except requests.RequestException:
        print 'error occurs'
        return None


def __get_space_url_name(html, nickname):
    soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        url_target = soup.find('a', attrs={'target': '_blank', 'class': 'title'}).get('href')
    except AttributeError:
        print 'No such user,exit...'
        sys.exit()

    Uid = re.search('\d+', url_target, re.S).group()
    target_real_name = soup.find('a', attrs={'target': '_blank', 'class': 'title'}).get('title')
    print 'the target User is: ' + target_real_name
    print 'the uid is: ' + Uid
    return Uid, target_real_name
