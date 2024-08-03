from pyspark.sql import SparkSession

conf = SparkConf().setAppName("MyApp")
sc = SparkContext(conf=conf)

data = [1, 2, 3, 4, 5]
rdd = sc.parallelize(data)

mapped_rdd = rdd.map(lambda x: x * 2)
print(mapped_rdd.collect())  # Output: [2, 4, 6, 8, 10]

filtered_rdd = rdd.filter(lambda x: x % 2 == 0)
print(filtered_rdd.collect())  # Output: [2, 4]

sc.stop()