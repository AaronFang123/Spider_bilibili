# -*- coding: utf-8 -*
# 通过提供的Uid 列表爬取其所有用户信息，独立于start.py
import codecs
import os
import requests
import sys
import json
import jsonpath
from fake_useragent import UserAgent
import random
import time

reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()


def get_user_info(mid):
    print 'getting {}'.format(mid)
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = 'https://api.bilibili.com/x/web-interface/card?mid={}'.format(mid)
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return __video_info_1(response.content)

    except requests.exceptions.RequestException as e:
        print(e)


def __video_info_1(content):
    obj = json.loads(content)
    infodict = jsonpath.jsonpath(obj, '$..data')[0]
    translate = {
            u'文章数'.decode('utf8'): infodict['article_count'],
            u'生日'.decode('utf8'): infodict['card']['birthday'],
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
    return infostr, translate


def readinfo(filename):
    userlist = []
    with codecs.open(filename, "r") as f:
        for line in f.readlines():
            userlist.append(line.strip('\n'))
    return userlist


def write(s):
    if not os.path.exists('User Information'):
        os.makedirs('User Information')
    with codecs.open(unicode(r'User Information.txt'), 'w', encoding='utf-16') as f:
        f.write(s)
    print 'User information written'


def sleep():
    a = random.uniform(0.3, 0.8)
    random_num = round(a, 3)
    time.sleep(random_num)


def main():
    s = ''
    uidlist = readinfo("all_uid_list.txt")
    length = len(uidlist)
    count = 1
    for uid in uidlist:
        sleep()
        print "{}/{}".format(count, length)
        count = count + 1
        t, dict_uinfo = get_user_info(uid)
        print t
        s = s + t + "\n"
    write(s)


if __name__ == '__main__':
    main()
