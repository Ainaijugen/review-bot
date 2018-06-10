import codecs
import jieba
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from crawl.task import tasks
from sklearn.externals import joblib
from sklearn.calibration import CalibratedClassifierCV
import os

path = os.path.dirname(__file__)


def main(isTrain):
    all = []
    yall = []
    for i in range(len(tasks)):
        print(i)
        corpus = []
        y = []
        for j in range(len(tasks[i][1])):
            print(i, j)
            trainij = codecs.open(os.path.join(path, 'data/trainnew%d_%d' % (i, j)), 'r', 'utf-8')
            dataij = trainij.readlines()
            corpus.extend(dataij)
            all.extend(dataij)
            for k in range(len(dataij)):
                y.append(j)
                yall.append(i)

        vectorizer = TfidfVectorizer(min_df=5)
        x = vectorizer.fit_transform(corpus).toarray()
        np.save(os.path.join(path, 'model/feature%d.npy' % i), vectorizer.get_feature_names())
        x = np.array(x)
        x = x.reshape(len(x), len(x[0]))

        X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.10, random_state=33)
        ss = StandardScaler()
        X_train = ss.fit_transform(X_train)
        X_test = ss.transform(X_test)

        X_shuf, Y_shuf = shuffle(X_train, Y_train)

        if isTrain:
            lsvc = LinearSVC()
            lsvc = CalibratedClassifierCV(lsvc)
            lsvc.fit(X_shuf, Y_shuf)
            joblib.dump(lsvc, os.path.join(path, "model/submodel%d.m" % i))
        else:
            lsvc = joblib.load(os.path.join(path, "model/submodel%d.m" % i))

        Y_predict = lsvc.predict(X_test)
        print(classification_report(Y_test, Y_predict))

    # vectorizer = TfidfVectorizer(min_df=5)
    # x = vectorizer.fit_transform(all).toarray()
    # print(vectorizer.get_feature_names())
    # x = np.array(x)
    # x = x.reshape(len(x), len(x[0]))
    #
    # X_train, X_test, Y_train, Y_test = train_test_split(x, yall, test_size=0.10, random_state=33)
    # ss = StandardScaler()
    # X_train = ss.fit_transform(X_train)
    # X_test = ss.transform(X_test)
    #
    # X_shuf, Y_shuf = shuffle(X_train, Y_train)
    # if isTrain:
    #     lsvc = LinearSVC()
    #     lsvc = CalibratedClassifierCV(lsvc)
    #     lsvc.fit(X_shuf, Y_shuf)
    #     joblib.dump(lsvc, os.path.join(path, "model/model.m"))
    # else:
    #     lsvc = joblib.load(os.path.join(path, "model/model.m"))
    #
    # Y_predict = lsvc.predict(X_test)
    #
    # print(classification_report(Y_test, Y_predict))


main(True)
