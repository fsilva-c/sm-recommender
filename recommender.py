from pyspark.sql.functions import col, explode
from pyspark.ml.recommendation import ALS
from spark import Spark
from make_dataset import INPUT_PATH


class Recommender(Spark):

    def __init__(self):
        self.__ratings = None
        self.__users = super().spark.read.csv(INPUT_PATH + 'users.csv', header=True)

        self.__als = ALS(
            rank=50,
            maxIter=5,
            regParam=0.15,
            userCol='user_id',
            itemCol='video_id',
            ratingCol='rating',
            nonnegative = True,
            implicitPrefs = False,
            coldStartStrategy='drop'
        )

    def train(self):
        self.__ratings = super().spark.read.csv(INPUT_PATH + 'ratings.csv', header=True)
        self.__ratings = self.__ratings. \
            withColumn('user_id', col('user_id').cast('integer')).  \
            withColumn('video_id', col('video_id').cast('integer')).\
            withColumn('rating', col('rating').cast('float'))
        return self.__als.fit(self.__ratings)

    def recommender(self, user_id, n_items):
        model = self.train()
        user = self.__users.filter(f'user_id = {user_id}')
        recommendations = model.recommendForUserSubset(user, numItems=n_items)

        return list(
                recommendations \
                .withColumn('rec_exp', explode('recommendations')) \
                .select(col('rec_exp.video_id')).toPandas()['video_id']
            )
            