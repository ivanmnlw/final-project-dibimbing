import pyspark
from pyspark.sql import DataFrame
import pyspark.sql.functions as F

# Spark Initialization
spark_host = "spark://dibimbing-dataeng-spark-master:7077"

sparkcontext = pyspark.SparkContext.getOrCreate(conf=(
        pyspark
        .SparkConf()
        .setAppName('Dibimbing')
        .setMaster(spark_host)
        .set("spark.jars", "/opt/bitnami/spark/jars/postgresql-42.2.18.jar")
    ))
sparkcontext.setLogLevel("WARN")

spark = pyspark.sql.SparkSession(sparkcontext.getOrCreate())

# JDBC connection properties
jdbc_url = "jdbc:postgresql://dataeng-postgres:5432/warehouse"
jdbc_properties = {
    "user": 'user',
    "password": 'password',
    "driver": "org.postgresql.Driver"
}

# Read data from PostgreSQL
df = spark.read.jdbc(url=jdbc_url, table="public.retail", properties=jdbc_properties)
# Show the data
df.show(5)
df.printSchema()

# Change Column Name
from pyspark.sql.types import *
schema = StructType([
    StructField("invoice_no", StringType(), True),
    StructField("stock_code", StringType(), True),
    StructField("description", StringType(), True),
    StructField("quantity", IntegerType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("unit_price", DoubleType(), True),
    StructField("customer_id", StringType(), True),
    StructField("country", StringType(), True),
])
df = spark.createDataFrame(df.rdd, schema=schema)
df.printSchema()

# Cleaning duplicate invoice_no and null values
print(f'Count_before: {df.count()}')
df_clean = df.dropDuplicates(subset=['invoice_no'])
df = df_clean.na.drop(subset=['invoice_no', 'customer_id'])
df.show()
print(f'Count_after: {df.count()}')

# Analysis total price each month
df = df.withColumn('subtotal', F.round(df.quantity * df.unit_price, 2))
df.show(5)

df_total_per_day = df.groupBy('invoice_date')\
                              .agg(F.round(F.sum('subtotal'),2).alias('total_per_day'))\
                              .orderBy('invoice_date')
df_total_per_day.show()

# Show total_quantity and unit_price average for each country
df_quantity_per_country = df.groupBy('country')\
                            .agg(
                                F.sum('quantity').alias('total_quantity'), 
                                F.round(F.avg('unit_price'), 2).alias('average_price')
                                ).orderBy('country')
df_quantity_per_country.show()

