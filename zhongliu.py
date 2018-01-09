import numpy as np
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression,SGDClassifier
from sklearn.metrics import classification_report
column_names = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
                        'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin',
                        'Normal Nucleoli', 'Mitoses', 'Class']
data=pd.read_csv('/Users/kddr/bigdate/datasummary/123456.csv',names=column_names)
#data.replace(to_replace='-1',value='?')
data.dropna(how='any')
print(data.shape)
X_train,X_test,y_train,y_test=train_test_split(data[column_names[1:10]],data[column_names[10]],test_size=0.25,random_state=33)
print(y_train.value_counts())
print(y_test.value_counts())
ss=StandardScaler()
X_train=ss.fit_transform(X_train)
X_test=ss.transform(X_test)
lr=LogisticRegression()
sgdc=SGDClassifier()
lr.fit(X_train,y_train)
lr_y_predict=lr.predict(X_test)
#print(lr_y_predict)
sgdc.fit(X_train,y_train)
sgdc_y_predict=sgdc.predict(X_test)
#print(sgdc_y_predict)
dataframe=pd.DataFrame({'origin':y_test,'predict':lr_y_predict})
#print(dataframe)
#print(lr.score(X_test,y_test))
print(classification_report(y_test,lr_y_predict,target_names=['Benign','Maligant']))
print(classification_report(y_test,sgdc_y_predict,target_names=['Benign','Maligant']))
