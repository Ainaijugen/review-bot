# -*- coding:utf-8-*-
import argparse
import random
import re

parser = argparse.ArgumentParser()
parser.add_argument("--input_file", "-i", type=str)
args = parser.parse_args()

punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')

def read_file(input_fn):
    contents = []
    with open(input_fn) as f:
        for line in f:
            line = ''.join(line.split()) #remove space
            phrases = [p for p in re.split(u'[,.?!，。？！]', line) if p != '']
            contents.append(phrases)
    '''
    for p in contents:
        for w in p:
            print(w)
    '''
    return contents

def gen(contents):
    sentence = []
    pnum = random.randint(1, 10)
    for i in range(pnum):
        s = contents[random.randint(0, len(contents) - 1)]
        sentence.append(s[random.randint(0, len(s) - 1)])
    return ','.join(sentence)
        
contents = read_file(args.input_file)
sentence = gen(contents)
print(sentence)