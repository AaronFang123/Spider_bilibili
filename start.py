# -*- coding: utf-8 -*
import vinfo
import sys
import userid
import vcomment
import visualization

reload(sys)
sys.setdefaultencoding('utf-8')
sysencoding = sys.getfilesystemencoding()


def main():
    up_name_to_define = raw_input('input the keyword(up name):').decode(sysencoding).encode(sysencoding)
    uid, name = userid.search_ID(up_name_to_define)
    aid_list, length_dict = vinfo.get_aid_list_and_length(uid)
    vinfo.get_main_info(aid_list, name, length_dict)

    all_comments = vcomment.get_comments_mutiprocess(aid_list)
    vcomment.save_comments_result(all_comments, name)

    visualization.comments_worldcloud(name)


if __name__ == '__main__':
    main()
