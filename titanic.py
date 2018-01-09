import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
titanic=pd.read_csv('/Users/kddr/bigdate/datasummary/titanic_dataset.csv')
#print(titanic.info())
X=titanic[['pclass','age','sex']]
y=titanic[['survived']]
#print(X.info())
X['age'].fillna(X['age'].mean(),inplace=True)
#print(X.info())
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=33)
vec=DictVectorizer(sparse=False)
X_train=vec.fit_transform(X_train.to_dict(orient='record'))
#print(vec.feature_names_)
X_test=vec.transform(X_test.to_dict(orient='record'))
dtc=DecisionTreeClassifier()#决策树
dtc.fit(X_train,y_train)
y_predict=dtc.predict(X_test)
#print(y_predict)
rfc=RandomForestClassifier()#随即森林
rfc.fit(X_train,np.ravel(y_train))
rfc_y_predict=rfc.predict(X_test)
gbc=GradientBoostingClassifier()#梯度上升
gbc.fit(X_train,y_train)
gbc_y_test=gbc.predict(X_test)

lr=LogisticRegression()
lr.fit(X_train,y_train)
lr_y_predict=lr.predict(X_test)

print(classification_report(y_predict,y_test,target_names=['died','survived']))#决策树
print(classification_report(rfc_y_predict,y_test,target_names=['died','survived']))#随即森林
print(classification_report(gbc_y_test,y_test,target_names=['died','survived']))#梯度上升
print(classification_report(lr_y_predict,y_test,target_names=['died','survived']))#逻辑斯蒂