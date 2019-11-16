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
