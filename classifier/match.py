import jieba
import gensim
from crawl.task import tasks
import json
from sklearn.externals import joblib
import numpy as np


def re_matching(words):
    for cate in tasks:
        for kind in cate[1]:
            if kind in words:
                return (cate[0], kind)
    return None


def svm_matching(words, modeltype):
    if modeltype == -1:
        feature = np.load('./model/feature.npy')
        # print(feature)
        feature = list(feature)
        clf = joblib.load("./model/model.m")
    else:
        feature = np.load('./model/feature%d.npy' % modeltype)
        # print(feature)
        feature = list(feature)
        clf = joblib.load("./model/submodel%d.m" % modeltype)
    x = np.zeros((1, len(feature)))
    for i in range(len(words)):
        if words[i] in feature:
            pos = feature.index(words[i])
            x[0][pos] = 1
    if modeltype != -1:
        return clf.predict_proba(x)[0]
    else:
        vec = clf.predict_proba(x)[0]
        for i in range(len(tasks)):
            ans = svm_matching(words, i)
            vec[i] += np.max(ans) / 4
        return vec


def parse_json(filename):
    f = open(filename, 'r')
    data = json.load(f)
    result = data['result']
    keyword = ' '.join(jieba.cut(result[1]['keyword']))
    print(keyword)
    # print(w2v_matching(keyword))


def query(item_name):
    tier1 = np.argmax(svm_matching(jieba.lcut(item_name), -1))
    if np.max(svm_matching(jieba.lcut(item_name), tier1)) >= 0.5:
        tier2 = np.argmax(svm_matching(jieba.lcut(item_name), tier1))
        return "%d_%d" % (int(tier1), int(tier2))
    return "%d_x" % tier1
