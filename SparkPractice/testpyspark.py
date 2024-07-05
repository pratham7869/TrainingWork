import findspark
findspark.init()
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("testpyspark").getOrCreate()

print("print the spark object")
print(spark)

# Read the CSV file
df = spark.read.csv("gods.csv", header=True, inferSchema=True)

# Showing the DataFrame
df.show()

# Print the schema of the DataFrame
df.printSchema()

# Stop the SparkSession
spark.stop()
