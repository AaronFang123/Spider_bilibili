# -*- coding: utf-8 -*
import codecs
import json
import multiprocessing
import os
import sys
import time
import singleVinfo
import jsonpath
import requests
from fake_useragent import UserAgent


reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()


# the return of the function is the list of video infomation(part 1),the list have four nesting struct
def get_aid_list_and_length(Uid):
    print 'get aid list and length'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}

    # pre-loan,to get total pages
    url_json = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + str(Uid) + '&page=1'
    html = requests.get(url_json, headers=headers).content
    obj = json.loads(html)
    last_page = jsonpath.jsonpath(obj, '$..pages')[0]
    # all the video of a user
    id_list = []
    # a dictionary of all the aids and length
    lendict = {}
    for i in range(1, last_page + 1):
        url_json = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=' + str(Uid) + '&page=' + str(i)
        html = requests.get(url_json, headers=headers).content
        obj = json.loads(html)
        vlist = jsonpath.jsonpath(obj, '$..vlist')
        for vinfo_pages in vlist:
            for vinfo_single_page in vinfo_pages:
                id_list.append(vinfo_single_page['aid'])
                lendict[vinfo_single_page['aid']] = vinfo_single_page['length']

    return id_list, lendict


def get_main_info(aidlist, vname, lengthdict):
    pool = multiprocessing.Pool(multiprocessing.cpu_count())
    main_info_list = pool.map(singleVinfo.user_info, aidlist)
    pool.terminate()
    for dict1 in main_info_list:
        dict1[u'视频长度'] = lengthdict[dict1[u'AV号'.encode('utf8')]]

    video_info_string1 = ''
    video_info_string2 = ''
    for dic in main_info_list:
        for k, v in dic.items():
            video_info_string1 = video_info_string1 + k + ':' + str(v) + '\n'
        video_info_string1 = video_info_string1 + '\n\n'
    video_info_string2 = video_info_string2 + video_info_string1
    print 'save_video_info'
    if not os.path.exists('Video_information'):
        os.makedirs('Video_information')
    with codecs.open(unicode(r'Video_information/{}.txt').format(vname), 'w', encoding='utf-16') as f:
        f.write(video_info_string2)

