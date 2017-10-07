import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import operator
from sklearn import datasets,linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.svm.libsvm import fit

df=pd.read_excel('/Users/kddr/Desktop/蓝球.xlsx')
tdate_set =set(df['日期'])
tnum_set =set(df['蓝球'])
X_parameter=[]
Y_parameter=[]

for single_square_feet,single_price_value in zip(df['日期'],df['蓝球']):
    X_parameter.append([float(single_square_feet)])
    Y_parameter.append(float(single_price_value))
print(X_parameter)
print(Y_parameter)
regr = linear_model.LinearRegression()
    #regr = LogisticRegression()
regr.fit(X_parameter, Y_parameter)
for i in range(17113,17120):
    predict_outcome = regr.predict(i)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
#print("num "+ str(1) +" Intercept value " , predictions['intercept'])
#print("num "+ str(1) +" coefficient" , predictions['coefficient'])
    print("num "+ str(i) +" Predicted value: ",predictions['predicted_value'])
def show_linear_line(X_parameters,Y_parameters):
    # Create linear regression object
    regr = linear_model.LinearRegression()
    #regr = LogisticRegression()
    regr.fit(X_parameters, Y_parameters)
    plt.figure(figsize=(12,6),dpi=80)
    plt.legend(loc='best')
    plt.scatter(X_parameters,Y_parameters,color='blue')
    plt.plot(X_parameters,regr.predict(X_parameters),color='red',linewidth=4)
    plt.xticks(())
    plt.yticks(())
    plt.show()
show_linear_line(X_parameter,Y_parameter)