# -*- coding:utf-8-*-
import jieba
from collections import defaultdict
import os
import numpy as np


def clean_string(s):
    # 上面输入字符串到s
    len_str = len(s)
    sta_str = 0
    flag = 0
    while True:
        for i in range(sta_str, len_str):

            if s[i] == '<' and i + 3 < len_str - 1 and i != len_str - 1:
                if s[i + 1] == 'e' and s[i + 2] == 'm' and s[i + 3] == '>':
                    s = s[:i] + s[i + 4:]
                    len_str = len_str - 4
                    sta_str = i
                    break
            if s[i] == '<' and i + 3 == len_str - 1 and i != len_str - 1:
                if s[i + 1] == 'e' and s[i + 2] == 'm' and s[i + 3] == '>':
                    s = s[:i]
                    flag = 1
                    break

            if s[i] == '&' and i + 11 < len_str - 1 and i != len_str - 1:
                if s[i + 1] == 'l' and s[i + 2] == 't':
                    s = s[:i] + s[i + 12:]
                    len_str = len_str - 12
                    sta_str = i
                    break

            if s[i] == '&' and i + 11 == len_str - 1 and i != len_str - 1:
                if s[i + 1] == 'l' and s[i + 2] == 't':
                    s = s[:i]
                    flag = 1
                    break

            if i == len_str - 1:
                flag = 1
                break
        if flag == 1:
            break
    return s


class GetToken:
    def __init__(self):
        self.word2id_dict = dict()
        self.vocab = set()
        self.word_cnt = 0

    def tokenlize(self, s):
        seg_list = jieba.cut(s)
        result = list()
        result.extend(seg_list)
        for each_seg in result:
            self.update_dict(each_seg)
        return result

    def update_dict(self, seg):
        if seg not in self.vocab:
            self.word2id_dict[seg] = self.word_cnt
            self.word_cnt += 1
            self.vocab.add(seg)

    def get_id(self, seg):
        if seg not in self.vocab:
            return -1
        return self.word2id_dict[seg]

    def print_dict(self):
        for seg in self.vocab:
            print(seg + " id =", self.word2id_dict[seg])


# if __name__ == "__main__":
#     get = GetToken()
#     seg_list = get.tokenlize("天安门上太阳升")
#     print("Default Mode: " + " / ".join(seg_list))
#     get.print_dict()
#     print(get.vocab)

def save(x, subpath, filename, force_recover = False):
    subpath = "./data/" + subpath
    if not os.path.exists(subpath):
        os.makedirs(subpath)
    file = subpath + '/' + filename
    if not force_recover:
        while os.path.exists(file + '.npy') == True:
            file += '-new'
            print('Warning: The file name have been used. Saved as ' + file)
    file += '.npy'
    np.save(file, x)


def load(subpath, filename):
    file = "./data/" + subpath + '/' + filename + '.npy'
    if not os.path.exists(file):
        print('The file does not exist')
        return
    x = np.load(file)
    return dict(x.item())
