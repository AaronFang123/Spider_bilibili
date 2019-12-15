# -*- coding: utf-8 -*
import codecs
import os
import jieba
import numpy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import time
import sys


def comments_worldcloud(name):
    with codecs.open(unicode(r'Detail_video_comments_result/{}.txt').format(name), 'r', encoding='utf-16') as f:
        f = f.read()
    cut_text = ' '.join(jieba.cut(f))
    background_image = numpy.array(Image.open('background.jpg'))
    word_cloud = WordCloud(scale=3, font_path='font.ttf',
                           background_color='white', width=1920, height=1080, mask=background_image)
    word_cloud_ = word_cloud.generate(cut_text)

    plt.imshow(word_cloud_)
    plt.axis("off")
    plt.show()
    if not os.path.exists('wordcloud'):
        os.makedirs('wordcloud')
    word_cloud.to_file(unicode('wordcloud/{}-comments-wordcloud.jpg'.format(name)))
    time.sleep(5)
    sys.exit()


def countwords(name):
    with codecs.open(unicode(r'Detail_video_comments_result/{}.txt').format(name), 'r', encoding='utf-16') as f:
        f = f.read()
    words = jieba.lcut(f)
    counts = {}
    for word in words:
        if len(word) == 1 or word == 'EOC' or not is_all_zh(word):
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    item = list(counts.items())
    item.sort(key=lambda x: x[1], reverse=True)

    if len(item) == 0:
        empty_list = []
        return empty_list

    if len(item) >= 20:
        for i in range(20):
            word, count = item[i]
            print "{} : {}".format(word.encode("utf8"), count)
        return item[0:19]

    else:
        count_top = len(item)
        for i in range(count_top):
            word, count = item[i]
            print "{} : {}".format(word.encode("utf8"), count)
        return item[0:count_top-1]


def is_all_zh(string):
    for ch in string:
        if not (ur'\u4e00' <= ch <= ur'\u9fa5'):
            return False
    return True


if __name__ == '__main__':
    countwords("哔哩哔哩弹幕网".decode("utf8"))