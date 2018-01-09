import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
class breastOrcancerWisconsin:
    def __init__(self,url):
        self.column_names = column_names = ['Sample code number','Clump Thickness','Uniformity of Cell Size','Uniformity of Cell Shape','Marginal Adhesion','Single Epithelial Cell Size','Bare Nuclei','Bland Chromatin','Normal Nucleoli','Mitoses','Class']
        self.data=pd.read_csv(url,names=self.column_names)
        self.data=self.data.replace(to_replace='?',value=np.nan)
        self.data=self.data.dropna(how='any')
    def trainandtestsplit(self,test_size):
        X_train, X_test, y_train, y_test = train_test_split(self.data[self.column_names[1:10]], self.data[self.column_names[10]],test_size=test_size, random_state=33)
        ss = StandardScaler()
        X_train=ss.fit_transform(X_train)
        X_test=ss.transform(X_test)
        return X_train, X_test, y_train, y_test
    def LogisticRegressionPredict(self,X_train, X_test, y_train, y_test):
        lr=LogisticRegression()
        lr.fit(X_train,y_train)
        lraccurary=lr.score(X_train,y_train)
        lr_y_predict = lr.predict(X_test)
        return lr_y_predict,lraccurary
    def SGDClassifierPredict(self,X_train, X_test, y_train, y_test):
        sdgc=SGDClassifier()
        sdgc.fit(X_train,y_train)
        sdgcaccurary=sdgc.score(X_train,y_train)
        sdgc_y_predict=sdgc.predict(X_test)
        return sdgc_y_predict,sdgcaccurary

a=breastOrcancerWisconsin("/Users/kddr/bigdate/datasummary/breast-cancer-wisconsin.csv")
X_train, X_test, y_train, y_test=a.trainandtestsplit(0.25)
j=0
for i in range(1,100):
    lr_y_predict, lraccurary = a.LogisticRegressionPredict(X_train, X_test, y_train, y_test)
    print('Accuracy of LR Classifier:', lraccurary)
    sdgc_y_predict, sdgcaccurary = a.SGDClassifierPredict(X_train, X_test, y_train, y_test)
    print('Accuarcy of SGD Classifier:', sdgcaccurary)
    if lraccurary>sdgcaccurary:
        j+=1
print(j)