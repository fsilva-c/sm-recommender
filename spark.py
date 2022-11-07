from pyspark.sql import SparkSession

class Spark:

    @property
    def spark(self):
        return SparkSession.builder.appName('fj_recommender').getOrCreate()
        