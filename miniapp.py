# -*- coding: utf-8 -*
import json
import vinfo
import sys
import vcomment
import analyseData
import getinfo_wide
import requests

reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()

APP_ID = 'wx51e9d5f55f550a61'  # 小程序id
APP_SECRET = '8e133e4607d13f5bb5e8d6bb5ed4fc98'  # 小程序独有的一个标志，可以在平台重置
ENV = 'microbiilii-fg40e'  # 云开发环境id
Collection_name = "User_info_test"  # 将要插入到的集合名
HEADER = {'content-type': 'application/json'}
WECHAT_URL = "https://api.weixin.qq.com/"


def get_access_token():
    url = '{0}cgi-bin/token?grant_type=client_credential&appid={1}&secret={2}'.format(WECHAT_URL, APP_ID, APP_SECRET)
    response = requests.get(url)
    result = response.json()
    return result['access_token']


def database_save(mid, accessToken_n):

    url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, accessToken_n)
    print 'Saving data...'
    print '-----------------------------------------------------------------------------'
    print 'Saving data...'

    userstr, userdict = getinfo_wide.get_user_info(mid)
    print userstr
    article_count = userdict[u'文章数'.decode('utf8')]
    name = userdict[u'昵称'.decode('utf8')].replace(' ', '_')
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
    all_comments, comments_count = vcomment.get_comments_mutiprocess(aid_list)
    vcomment.save_comments_result(all_comments, name)
    top_10_words = analyseData.countwords(name)
    formatted_top_10 = '{'
    for info_tuple in top_10_words:
        formatted_top_10 += '{}:{}, '.format(info_tuple[0], info_tuple[1])
    formatted_top_10 += '}'
    # add
    query = ""
    if url == '{0}tcb/databaseadd?access_token={1}'.format(WECHAT_URL, accessToken_n):
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
    elif url == '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, accessToken_n):
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
    data = {
        "env": ENV,
        "query": query
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    print response.text
    update_errorCatch(response.text, data)

    print '-----------------------------------------------------------------------------'
    print 'Saved!'


def update_errorCatch(text, data):
    errcode = json.loads(text)["errcode"]
    if errcode == 0:
        return
    while errcode != 0:
        print "load again"
        accessToken_n = get_access_token()
        url = '{0}tcb/databaseupdate?access_token={1}'.format(WECHAT_URL, accessToken_n)
        response = requests.post(url, data=json.dumps(data), headers=HEADER)
        print response.text


def pushed_count(accessToken_n):
    url = '{0}tcb/databasecount?access_token={1}'.format(WECHAT_URL, accessToken_n)
    query = "db.collection(\"{0}\").where({1}).count()".format(Collection_name, "{is_updated:\"true\"}")
    print query
    data = {
        "env": ENV,
        "query": query
    }
    response = requests.post(url, data=json.dumps(data), headers=HEADER)
    print response.text
    con = json.loads(response.content)
    process_num = int(con['count'])
    print process_num
    return process_num


if __name__ == '__main__':
    accessToken = get_access_token()
    c = pushed_count(accessToken)
    print "updated {}".format(c)
    uidlist = getinfo_wide.readinfo("uidtest.txt")
    uidlist = uidlist[c:]
    for uid in uidlist:
        getinfo_wide.sleep()
        database_save(uid, accessToken)
