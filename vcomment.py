# -*- coding: utf-8 -*
import codecs
import os

import jsonpath
import requests
import json
import sys
import random
from fake_useragent import UserAgent
import time
import datetime
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf8')
sysencoding = sys.getfilesystemencoding()


def __get_all_comments_in_a_video(aid):
    try:
        ua = UserAgent()
        # pre-loan,get total pages number
        print 'Getting video comments from av{},now time: {},Please wait......' \
            .format(aid, datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        s = ''
        for i in range(1, 200):
            headers = {'User-Agent': ua.random, 'Connection': 'close'}
            url_json = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}'.format(i, aid)
            html = requests.get(url_json, headers=headers).content

            # sleep
            a = random.uniform(2.01, 3)
            random_num = round(a, 3)
            time.sleep(random_num)

            obj = json.loads(html)
            last_page = jsonpath.jsonpath(obj, '$..data')[0]

            dict1 = last_page['replies']
            if not dict1:
                break
            for j in dict1:
                s = str(s + j['content']['message'] + '\n')
    except Exception as err_msg:
        print "sub_task():error message=%s" % str(err_msg)

    return str(s)


def save_comments_result(string, name):
    if not os.path.exists('Detail_video_comments_result'):
        os.makedirs('Detail_video_comments_result')
    with codecs.open(unicode(r'Detail_video_comments_result/{}.txt').format(name), 'w', encoding='utf-16') as f:
        f.write(string)


def get_comments_mutiprocess(aidlist):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    all_comments_list = pool.map(__get_all_comments_in_a_video, aidlist)
    pool.terminate()
    s = ''
    n = 1  # counter
    for i in all_comments_list:
        try:
            print 'No. {},time:{}'.format(n, datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
            n += 1
            s = s + str(i) + '\n'
        except TypeError as exp:
            print exp.message
            s = str(s)
    print 'comments get ready,writing files......'
    return s
