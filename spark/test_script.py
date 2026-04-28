from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("AirflowSparkJob") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, columns)
df.show()

print(f"Total count: {df.count()}")

spark.stop()