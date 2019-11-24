# -*- coding: utf-8 -*
import codecs
import os
import requests
import sys
import json
import jsonpath
from fake_useragent import UserAgent

reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()


def get_user_info(uid, name):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    print 'User Information: {}'.format(name)
    url = 'https://api.bilibili.com/x/web-interface/card?mid={}'.format(uid)
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            __video_info_1(response.content, name)

    except requests.exceptions.RequestException as e:
        print(e)


def __video_info_1(content, name):
    obj = json.loads(content)

    infodict = jsonpath.jsonpath(obj, '$..data')[0]
    translate = {
                 u'文章数'.encode('utf8'): infodict['article_count'],
                 u'生日'.encode('utf8'): infodict['card']['birthday'],
                 u'自我简介'.decode('utf8'): infodict['card']['description'],
                 u'头像'.decode('utf8'): infodict['card']['face'],
                 u'投稿总数'.decode('utf8'): infodict['archive_count'],

                 u'粉丝数'.decode('utf8'): infodict['card']['fans'],
                 u'朋友数'.decode('utf8'): infodict['card']['friend'],
                 u'等级'.decode('utf8'): infodict["card"]['level_info']['current_level'],
                 u'Up主mid(id)'.decode('utf8'): infodict["card"]['mid'],
                 u'昵称'.decode('utf8'): infodict["card"]['name'],

                 u'官方认证'.decode('utf8'): infodict["card"]['official_verify']['desc'],
                 u'性别'.decode('utf8'): infodict["card"]['sex'],
                 u'签名'.decode('utf8'): infodict["card"]['sign'],
                 u'是否为vip'.decode('utf8'): infodict["card"]['vip']['vipStatus'],
                 u'粉丝数'.decode('utf8'): infodict["follower"],
                 }
    infostr = ''
    for k, v in translate.items():
         infostr = infostr + str(k) + ':' + str(v) + '\n'
    print infostr
    if not os.path.exists('User Information'):
        os.makedirs('User Information')
    with codecs.open(unicode(r'User Information/{}.txt').format(name), 'w', encoding='utf-16') as f:
        f.write(infostr)
    print 'User information written'
