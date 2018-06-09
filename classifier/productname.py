from crawl.task import tasks
from sklearn.svm import LinearSVC
from crawl.crawl import getsource
import codecs
import re
import os
import jieba

# pagesize = 44
#
# titles = [dict() for _ in range(40)]
# for i in range(len(tasks)):
#     for j in range(len(tasks[i][1])):
#         if os.path.exists('./data/train%d_%d' % (i,j)):continue
#         kind = tasks[i][1][j]
#         print(kind)
#         trainij = codecs.open('./data/train%d_%d' % (i,j),'w','utf-8')
#         data = []
#         for k in range(5):
#             content = getsource('https://s.taobao.com/search?q=%s&sort=sale-desc&s=%d' % (tasks[i][0]+'+'+kind,k*pagesize),0,"../crawl/chromedriver")
#             for m in range(pagesize):
#                 content = content[re.search(',\"raw_title\":\"', content).end():]
#                 line = content[:re.search('\",\"', content).start()]+'\n'
#                 data.append(line)
#         trainij.writelines(data)
#         trainij.close()

for i in range(len(tasks)):
    for j in range(len(tasks[i][1])):
        print(i,j)
        trainij = codecs.open('./data/train%d_%d' % (i, j), 'r', 'utf-8')
        data = trainij.readlines()
        for k in range(len(data)):
            data[k] = ' '.join(jieba.cut(data[k]))
        trainijnew = codecs.open('./data/trainnew%d_%d' % (i, j), 'w', 'utf-8')
        trainijnew.writelines(data)
        trainij.close()
        trainijnew.close()