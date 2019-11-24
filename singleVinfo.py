# -*- coding: utf-8 -*
import random
import time
import requests
import sys
import json
import jsonpath
from fake_useragent import UserAgent

reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()


def user_info(aid):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    print 'Video Information: {}'.format(aid)
    url = 'https://api.bilibili.com/x/web-interface/view?aid={}'.format(aid)
    # sleep
    a = random.uniform(1.5, 2.5)
    random_num = round(a, 3)
    time.sleep(random_num)
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            maindict = __video_info_1(response.content, aid)
            return maindict
    except requests.exceptions.RequestException as e:
        print(e)


def __video_info_1(content, aid):
    obj = json.loads(content)

    infodict = jsonpath.jsonpath(obj, '$..data')[0]
    # infostr = ''
    translate = {u'AV号'.encode('utf8'): aid,
                 u'标题'.encode('utf8'): infodict['title'],
                 u'分区名'.encode('utf8'): infodict['tname'],
                 u'投稿时间'.decode('utf8'): time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(infodict['ctime'])),
                 u'视频简介'.decode('utf8'): infodict["desc"],

                 u'Tags'.decode('utf8'): infodict["dynamic"],
                 u'Up主昵称'.decode('utf8'): infodict["owner"]['name'],
                 u'Up主头像'.decode('utf8'): infodict["owner"]['face'],
                 u'Up主mid(id)'.decode('utf8'): infodict["owner"]['mid'],
                 u'分P数'.decode('utf8'): infodict['videos'],

                 u'视频封面'.decode('utf8'): infodict["pic"],
                 u'是否允许下载'.decode('utf8'): infodict["rights"]['download'],
                 u'是否为共同创作'.decode('utf8'): infodict["rights"]['is_cooperation'],
                 u'是否自动播放'.decode('utf8'): infodict["rights"]['autoplay'],
                 u'投币数'.decode('utf8'): infodict["stat"]['coin'],

                 u'弹幕量'.decode('utf8'): infodict["stat"]['danmaku'],
                 u'踩'.decode('utf8'): infodict["stat"]['dislike'],
                 u'收藏数'.decode('utf8'): infodict["stat"]["favorite"],
                 u'点赞数'.decode('utf8'): infodict["stat"]["like"],
                 u'评论数'.decode('utf8'): infodict["stat"]["reply"],

                 u'分享数'.decode('utf8'): infodict["stat"]["share"],
                 u'播放量'.decode('utf8'): infodict["stat"]["view"],
                 }

    # for k, v in translate.items():
    #     infostr = infostr + k + ':' + str(v) + '\n'
    return translate


if __name__ == '__main__':
    print user_info('75470301')
