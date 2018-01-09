from sklearn.cross_validation import  train_test_split
from sklearn.datasets import load_iris
from sklearn.feature_extraction import DictVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np
#iris=load_iris()
iris=pd.read_csv("/Users/kddr/bigdate/datasummary/iris.csv")
iris.replace(to_replace='? ',value=np.nan)
iris.dropna(how='any')
column_names=['sepal_length','sepal_width','petal_length','petal_width','class']
X_train,X_test,y_train,y_test=train_test_split(iris[column_names[0:4]],iris[column_names[4]],test_size=0.25,random_state=33)
ss=StandardScaler()
X_train=ss.fit_transform(X_train)
X_test=ss.transform(X_test)
knc=KNeighborsClassifier()
knc.fit(X_train,y_train)
y_predict=knc.predict(X_test)
print(y_predict)
print(knc.score(X_test,y_test))
print(classification_report(y_test,y_predict,target_names=['Iris-setosa','Iris-versicolor','Iris-virginica']))
X_train,X_test,y_train,y_test=train_test_split(iris[column_names[0:4]],iris[column_names[4]],test_size=0.25,random_state=33)
vec=DictVectorizer(sparse=False)
X_train=vec.fit_transform(X_train.to_dict(orient='record'))
print(vec.feature_names_)
X_test=vec.transform(X_test.to_dict(orient='record'))
dtc=DecisionTreeClassifier()
dtc.fit(X_train,y_train)
y_predict=dtc.predict(X_test)
print(classification_report(y_predict,y_test,target_names=['Iris-setosa','Iris-versicolor','Iris-virginica']))