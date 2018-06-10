import jieba
from crawl.task import tasks
import json
from sklearn.externals import joblib
import numpy as np
import os

path = os.path.dirname(__file__)


def re_matching(words, modeltype):
    def check(ss1, s2):
        ans = 0
        for s1 in ss1:
            if s1.find(s2) != -1:
                ans += 1
                # print(s1, s2)
            if s2.find(s1) != -1:
                ans += 1
                # print(s1, s2)
        return ans

    print(words)
    if modeltype == -1:
        ans = np.ones(len(tasks), dtype=np.float32)
        for i in range(len(tasks)):
            ans[i] += check(words, tasks[i][0])
            for kind in tasks[i][1]:
                ans[i] += check(words, kind)
        ans /= np.sum(ans)
        return ans
    else:
        ans = np.ones(4, dtype=np.float32)
        ans += check(words, tasks[modeltype][0])
        for (i, kind) in enumerate(tasks[modeltype][1]):
            ans[i] += check(words, kind)
        ans /= np.sum(ans)
        return ans


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
        return (clf.predict_proba(x)[0] + re_matching(words, modeltype) * 10) / 11
    else:
        vec = clf.predict_proba(x)[0]
        for i in range(len(tasks)):
            ans = svm_matching(words, i)
            vec[i] += np.sum(ans) / 4
        return (vec / 2 + re_matching(words, modeltype) * 10) / 11


def parse_json(filename):
    f = open(filename, 'r')
    data = json.load(f)
    result = data['result']
    keyword = ' '.join(jieba.cut(result[1]['keyword']))
    print(keyword)
    # print(w2v_matching(keyword))


def query(item_name):
    item_name = item_name.strip()
    print(item_name)
    wls = jieba.lcut(item_name)
    ans = svm_matching(wls, -1)
    tier1 = np.argmax(ans)
    tier2 = 0
    max_proba = np.max(ans)
    for i in range(len(tasks)):
        ans1 = svm_matching(wls, i)
        print(ans1)
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
