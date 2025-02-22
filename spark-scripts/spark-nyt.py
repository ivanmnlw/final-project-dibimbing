import pyspark
from pyspark.sql import DataFrame
import pyspark.sql.functions as F
import pandas as pd

sparkcontext = pyspark.SparkContext.getOrCreate(
    conf=(pyspark.SparkConf().setAppName("FinalProject_1"))
)
sparkcontext.setLogLevel("WARN")

spark = pyspark.sql.SparkSession(sparkcontext.getOrCreate())


# Change Column Name
from pyspark.sql.types import *
schema = StructType([
    StructField("id", IntegerType(), True),
    StructField("url", StringType(), True),
    StructField("datetime", StringType(), True),
    StructField("title", StringType(), True),
    StructField("text", StringType(), True),
    StructField("source", StringType(), True),
])
df = spark.read.csv('/opt/bitnami/spark/data/nyt.csv', schema=schema, header=True)

df = df.withColumn('datetime', F.to_timestamp('datetime'))
df = df.drop("id")
print(df.count())
df = df.dropDuplicates(["url"])
df.show(5)
df.printSchema()
print(df.count())
df.dropna()
print(df.count())

# df.toPandas().to_csv('/opt/bitnami/spark/data/nyt_spark.csv', index=False)

# NLTK Sentiment Analysis
from transformers import pipeline

classifier = pipeline('sentiment-analysis', truncation=True)

text_values = df.select("text").rdd.flatMap(lambda x: x).collect()
# print(text_values)

df_s = spark.createDataFrame(classifier(text_values))
df_s_pd = df_s.toPandas()
print(df_s_pd)

df = df.withColumn('datetime', F.col('datetime').cast('string'))
pdf = df.toPandas()
pdf['datetime'] = pd.to_datetime(pdf['datetime'], errors='coerce')
print(pdf)

merged_df = pd.concat([pdf, df_s_pd], axis=1)
print(merged_df)
merged_df.to_csv('/opt/bitnami/spark/data/nyt_spark.csv', index=False)


