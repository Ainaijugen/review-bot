import jieba
from crawl.task import tasks
import json
from sklearn.externals import joblib
import numpy as np
import os

path = os.path.dirname(__file__)


def re_matching(words):
    for cate in tasks:
        for kind in cate[1]:
            if kind in words:
                return (cate[0], kind)
    return None


def svm_matching(words, modeltype):
    if modeltype == -1:
        feature = np.load(os.path.join(path, 'model/feature.npy'))
        # print(feature)
        feature = list(feature)
        clf = joblib.load(os.path.join(path, "model/model.m"))
    else:
        feature = np.load(os.path.join(path, 'model/feature%d.npy' % modeltype))
        # print(feature)
        feature = list(feature)
        clf = joblib.load(os.path.join(path, "model/submodel%d.m" % modeltype))
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
            print(ans)
            vec[i] += np.sum(ans) / 4
        return vec / 2


def parse_json(filename):
    f = open(filename, 'r')
    data = json.load(f)
    result = data['result']
    keyword = ' '.join(jieba.cut(result[1]['keyword']))
    print(keyword)
    # print(w2v_matching(keyword))


def query(item_name):
    print(item_name)
    wls = jieba.lcut(item_name)
    print(wls)
    ans = svm_matching(wls, -1)
    tier1 = np.argmax(ans)
    tier2 = 5
    max_proba = np.max(ans)
    for i in range(len(tasks)):
        ans1 = svm_matching(wls, i)
        t_tier2 = np.argmax(ans1)
        if ans1[t_tier2] > max_proba:
            max_proba = ans1[t_tier2]
            tier2 = t_tier2
            tier1 = i
    t_tier1 = np.argmax(ans)
    if np.max(svm_matching(wls, t_tier1)) >= max_proba:
        tans = svm_matching(wls, t_tier1)
        tier2 = np.argmax(tans)
        tier1 = t_tier1
        max_proba = np.max(tans)
    return "%d_%d" % (tier1, tier2), max_proba


print(query(""))
