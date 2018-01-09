from pyspark.shell import sc
from pyspark.sql import HiveContext
from pyspark.ml import Pipeline
from pyspark.ml.feature import OneHotEncoder,StringIndexer,VectorAssembler
hc=HiveContext(sc)
hc.sql("use default")
data=hc.sql("select * from default.desc_stat")
data.show()
fruit_str_index=StringIndexer(inputCol="fruit",outputCol="fruit_index")
fruit_one_hot=OneHotEncoder(inputCol="fruit_index",outputCol="fruit_cont")
condit_str_index=StringIndexer(inputCol="condit",outputCol="condit_index")
condit_one_hot=OneHotEncoder(inputCol="condit_index",outputCol="condit_cont")
assembler=VectorAssembler(inputCols=["fruit_cont","condit_cont","price","sale"],outputCol="features")
pl=Pipeline(stages=[fruit_str_index,fruit_one_hot,condit_str_index,condit_one_hot,assembler])
data=pl.fit(data).transform(data)
data.show(truncate=False)