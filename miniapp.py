# -*- coding: utf-8 -*
import json
import vinfo
import sys
import vcomment
import analyseData
import getinfo_wide
import requests
import time

reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()

APP_ID = # 小程序id
APP_SECRET =  # 小程序独有的一个标志，可以在平台重置
ENV = # 云开发环境id
Collection_name = "User_info"  # 将要插入到的集合名
HEADER = {'content-type': 'application/json'}
WECHAT_URL = "https://api.weixin.qq.com/"
ACCESS_TOKEN = ""
ACCESS_TOKENZ_LOAD = 0
UPDATED_COUNT = 5971


def get_access_token():
    global ACCESS_TOKEN, ACCESS_TOKENZ_LOAD
    url = '{0}cgi-bin/token?grant_type=client_credential&appid={1}&secret={2}'.format(WECHAT_URL, APP_ID, APP_SECRET)
    response = requests.get(url)
    result = response.json()
    ACCESS_TOKENZ_LOAD += 1
    ACCESS_TOKEN = result['access_token']


def database_save(mid):
    global UPDATED_COUNT
    url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN)
    print 'Saving data...'
    print '-----------------------------------------------------------------------------'
    print 'Saving data...'

    userstr, userdict = getinfo_wide.get_user_info(mid)
    print userstr
    article_count = userdict[u'文章数'.decode('utf8')]
    name = userdict[u'昵称'.decode('utf8')].replace(' ', '_').replace('/', '_')
    face = userdict[u'头像'.decode('utf8')]
    archive_count = userdict[u'投稿总数'.decode('utf8')]
    fans = userdict[u'粉丝数'.decode('utf8')]
    friend = userdict[u'朋友数'.decode('utf8')]
    current_level = userdict[u'等级'.decode('utf8')]
    mid = userdict[u'Up主mid(id)'.decode('utf8')]
    desc = userdict[u'官方认证'.decode('utf8')]
    sign = userdict[u'签名'.decode('utf8')].replace('\n', ' ').replace('\r', ' ')
    vipStatus = userdict[u'是否为vip'.decode('utf8')]
    follower = userdict[u'粉丝数'.decode('utf8')]
    sex = userdict[u'性别'.decode('utf8')]

    aid_list, length_dict = vinfo.get_aid_list_and_length(mid)

    if len(aid_list) >= 30:
        aid_list = aid_list[0:29]
    elif len(aid_list) == 0:
        return
    all_comments, comments_count = vcomment.get_comments_mutiprocess(aid_list)
    vcomment.save_comments_result(all_comments, name)
    top_10_words = analyseData.countwords(name)
    formatted_top_10 = '{'
    for info_tuple in top_10_words:
        formatted_top_10 += '{}:{}, '.format(info_tuple[0], info_tuple[1])
    formatted_top_10 += '}'
    # add
    query = ""
    if url == '{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN):
        query = "db.collection(\"{0}\").add(" \
                "{{data:{{" \
                "_id: \'{1}\', " \
                "article_count: \'{2}\', " \
                "face_url: \'{3}\'," \
                "archive_count: \'{4}\'," \
                "fans: \'{5}\'," \
                "friends: \'{6}\'," \
                "current_level: \'{7}\'," \
                "mid: \'{8}\'," \
                "name: \'{9}\'," \
                "official_verify: \'{10}\'," \
                "sign: \'{11}\'," \
                "vipStatus: \'{12}\'," \
                "followers: \'{13}\'," \
                "sex: \'{14}\'," \
                "is_updated: \'{15}\'," \
                "top_10_comments_words: {16}," \
                "comments_count: {17}" \
                "}}}})" \
            .format(Collection_name, name, article_count, face, archive_count, fans, friend, current_level, mid, name,
                    desc, sign, vipStatus, follower, sex, 'true', formatted_top_10, comments_count)

    # update
    elif url == '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN):
        query = "db.collection(\"{0}\").doc(\"{1}\").update(" \
                "{{data:{{" \
                "article_count: \'{2}\', " \
                "face_url: \'{3}\'," \
                "archive_count: \'{4}\'," \
                "fans: \'{5}\'," \
                "friends: \'{6}\'," \
                "current_level: \'{7}\'," \
                "mid: \'{8}\'," \
                "name: \'{9}\'," \
                "official_verify: \'{10}\'," \
                "sign: \'{11}\'," \
                "vipStatus: \'{12}\'," \
                "followers: \'{13}\'," \
                "sex: \'{14}\'," \
                "is_updated: \'{15}\'," \
                "top_10_comments_words: {16}," \
                "comments_count: \'{17}\'," \
                "}}}})" \
            .format(Collection_name, name, article_count, face, archive_count, fans, friend, current_level, mid,
                    name, desc, sign, vipStatus, follower, sex, 'true', formatted_top_10, comments_count)
    print query
    data = {
        "env": ENV,
        "query": query
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    print response.text
    update_errorCatch(response.text, data, name)

    print '-----------------------------------------------------------------------------'
    print "access token load times  {}".format(ACCESS_TOKENZ_LOAD)
    print 'Saved!'
    UPDATED_COUNT += 1


def update_errorCatch(text, data,  name):
    coun = 0
    try:
        errcode = json.loads(text)["errcode"]
    except ValueError as ve:
        print ve.message
        return
    if errcode == 0:
        return
    elif errcode == 45009:
        raise Exception  # 到次数了
    elif errcode == -605101:
        url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN)
        query = "db.collection(\"{0}\").doc(\"{1}\").update(" \
                "{{data:{{" \
                "is_updated: \'{2}\'," \
                "}}}})" \
            .format(Collection_name, name, 'false',)
        data_inside = {
            "env": ENV,
            "query": query
        }
        response = requests.post(url, data=json.dumps(data_inside), headers=HEADER)
        print 'Query false'
        print response.text
        return

    else:
        while True:
            if coun >= 3:
                break
            coun += 1
            print "load again"
            get_access_token()
            url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN)
            response_inside = requests.post(url, data=json.dumps(data), headers=HEADER)
            errcode_inside = json.loads(response_inside.text)["errcode"]
            print response_inside.text
            if errcode_inside == 0:
                break
            time.sleep(5)


def pushed_count():
    url = '{0}tcb/databasecount?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN)
    query = "db.collection(\"{0}\").where({1}).count()".format(Collection_name, "{updated:true}")
    print query
    data = {
        "env": ENV,
        "query": query
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    print response.text
    con = json.loads(response.content)
    pushed_num = int(con['count'])

    url = '{0}tcb/databasecount?access_token={1}'.format(WECHAT_URL, ACCESS_TOKEN)
    query = "db.collection(\"{0}\").where({1}).count()".format(Collection_name, "{is_updated:\"false\"}")
    print query
    data = {
        "env": ENV,
        "query": query
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    print response.text
    con = json.loads(response.content)
    unpushed_num = int(con['count'])
    print "***********************************************************"
    print "updated : {} , updated false : {}".format(pushed_num, unpushed_num)
    print "***********************************************************"

    return 62179 + unpushed_num + pushed_num


if __name__ == '__main__':
    get_access_token()
    c = pushed_count()
    uidlist = getinfo_wide.readinfo("all_uid_list.txt")
    uidlist = uidlist[c:]
    for uid in uidlist:
        print "updated {}".format(c)
        getinfo_wide.sleep()
        database_save(uid)
