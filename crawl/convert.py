from task import tasks
import os
import numpy as np

for i in range(len(tasks)):
    for j in range(len(tasks[i][1])):
        if os.path.exists("./data/%d_%d" % (i, j)) and not os.path.exists("./data/%d_%d/all.txt" % (i, j)):
            all = open("./data/%d_%d/all.txt" % (i, j), "w")
            attr2feedback = dict(np.load("./data/%d_%d/attr2feedback.npy" % (i, j)).item())
            for x in attr2feedback:
                for y in attr2feedback[x]:
                    def filter(y):
                        yy = [y[0], y[1]]
                        for i in range(2, len(y)):
                            if y[i] == '>' and y[i - 1] == 'b':
                                if y[i - 2] == '<':
                                    yy = yy[:-2]
                                else:
                                    yy = yy[:-3]
                            else:
                                yy.append(y[i])
                        return yy


                    all.write("%s\n" % " ".join(filter(y)))
            all.close()
