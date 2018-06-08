# -*- coding:utf-8-*-
import argparse
import random
import re

punct = set(
    u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')


def read_file(input_fn):
    contents = []
    with open(input_fn) as f:
        for line in f:
            line = ''.join(line.split())  # remove space
            phrases = [p for p in re.split(u'[,.?!，。？！]', line) if p != '']
            contents.append(phrases)
    '''
    for p in contents:
        for w in p:
            print(w)
    '''
    return contents


def gen(contents, stop_length):
    answer = []
    while len(answer) < 5:
        sentence = []
        pnum = random.randint(1, 10)
        for i in range(pnum):
            s = contents[random.randint(0, len(contents) - 1)]
            sentence.append(s[random.randint(0, len(s) - 1)])
        ans = '，'.join(sentence)
        if stop_length * 0.75 <= len(ans) <= stop_length:
            answer.append(ans)
    return answer


def main(filename, stop_length=100):
    contents = read_file(filename)
    return gen(contents, stop_length)
