import codecs
import random


def read_proxy():
    proxy_list = []
    with codecs.open("proxy_pool.txt", "r") as f:
        for line in f.readlines():
            proxy_list.append(line.strip('\n'))
    proxy = random.choice(proxy_list)
    return proxy
