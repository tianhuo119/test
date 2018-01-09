from pprint import pprint
from pyspark import SparkContext, SQLContext
from pyspark.ml import Pipeline
from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorIndexer
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.regression import RandomForestRegressor,GBTRegressor
from pyspark.ml.tuning import ParamGridBuilder,CrossValidator
from sklearn.datasets import load_boston
import pandas as pd
boston=load_boston()
data=pd.DataFrame(boston["data"],columns=boston['feature_names'])
data.index.name="id"
data['target']=boston['target']
data.to_csv("/tmp/boston.csv",header=False)
sc = SparkContext()
sqlContext = SQLContext(sc)
data=sc.textFile('/tmp/boston.csv').map(lambda l:l.split(',')).map(lambda v:(int(v[0]),float(v[-1]),Vectors.dense([_ for _ in v[1:-1]]))).toDF(["id","label","features"])
print(type(data))
data.show(5,truncate=False)
to_care=VectorIndexer(inputCol="features",outputCol="indexedFeatures",maxCategories=10)
(train,test)=data.randomSplit([0.8,0.2])
#rf=GBTRegressor(featuresCol="indexedFeatures",maxIter=100)
rf=RandomForestRegressor(featuresCol="indexedFeatures",numTrees=100)

pl=Pipeline(stages=[to_care,rf])
#print(type(rf),rf)
#print(type(pl),pl)

model=pl.fit(train)
pred=model.transform(test)
pred.show(3)
evaluator=RegressionEvaluator(labelCol="label",predictionCol="prediction",metricName="rmse")
rmse=evaluator.evaluate(pred)
print("Root Mean Squared Error(RMSE:均方根误差):{}".format(rmse))
rfModel=model.stages[1]
#print(rfModel)

evator=RegressionEvaluator(labelCol="label",predictionCol="prediction",metricName="rmse")
grid=ParamGridBuilder().addGrid(rf.numTrees,[5,10]
                                #rf.maxIter,[5,10,20]
                                ).addGrid(rf.maxDepth,[4,5]).build()
cv=CrossValidator(estimator=pl,estimatorParamMaps=grid,evaluator=evator,numFolds=5)
cv_model=cv.fit(train)
print('最好的模型:',cv_model.bestModel)
rmse=evator.evaluate(cv_model.transform(train))
print("Root Mean Squared Error(RMSE:均方根误差):{}".format(rmse))