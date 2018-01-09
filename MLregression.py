import pandas as pd
from sklearn.datasets import load_boston
boston=load_boston()
data=pd.DataFrame(boston["data"],columns=boston['feature_names'])
data.index.name="id"
data['target']=boston['target']
data.to_csv("/tmp/boston.csv",header=False)
