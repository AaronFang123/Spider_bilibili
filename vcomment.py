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

import multiprocessing

reload(sys)
sys.setdefaultencoding('utf8')
sysencoding = sys.getfilesystemencoding()


def sleep():
    a = random.uniform(0.3, 0.8)
    random_num = round(a, 3)
    time.sleep(random_num)


def __get_all_comments_in_a_video(aid):
    s = ""
    time_start = time.time()
    counter = 0
    try:
        ua = UserAgent()
        # pre-loan,get total pages number
        headers = {'User-Agent': ua.random}
        s = ''
        for i in range(1, 6):
            url_json = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid={}'.format(i, aid)
            html = requests.get(url_json, headers=headers).content

            sleep()

            obj = json.loads(html)
            last_page = jsonpath.jsonpath(obj, '$..data')[0]

            dict1 = last_page['replies']
            if not dict1:
                break
            for j in dict1:
                s = str(s + j['content']['message'] + ' EOC '+'\n')
                counter += 1

    except Exception as err_msg:
        print "sub_task():error message=%s" % str(err_msg)
    time_end = time.time()
    print '    av {0} totally cost: {1}s, comments:{2}'.format(aid, time_end - time_start, counter)
    return str(s)


def save_comments_result(string, name):
    if not os.path.exists('Detail_video_comments_result'):
        os.makedirs('Detail_video_comments_result')
    with codecs.open(unicode(r'Detail_video_comments_result/{}.txt').format(name), 'w', encoding='utf-16') as f:
        f.write(string)


def get_comments_mutiprocess(aidlist):
    pool = multiprocessing.Pool(8)  # multiprocessing.cpu_count()
    all_comments_list = pool.map(__get_all_comments_in_a_video, aidlist)
    pool.terminate()
    s = ''
    for i in all_comments_list:
        try:
            s = s + str(i) + '\n'
        except TypeError as exp:
            print exp.message
            s = str(s)
    count_mark = "EOC"
    comments_count_inside = s.count(count_mark)
    print 'total comments: {0}'.format(comments_count_inside)
    print 'comments get ready,writing files......'
    return s, comments_count_inside
