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

    def recommender(self, user_id, n_items, col_rating=False):
        model = self.train()
        user = self.__users.filter(f'user_id = {user_id}')
        recommendations = model.recommendForUserSubset(user, numItems=n_items)

        cols = 'rec_exp.video_id' if not col_rating else ['rec_exp.video_id', 'rec_exp.rating']

        rows = recommendations \
                .withColumn('rec_exp', explode('recommendations')) \
                .select(cols).collect()

        if col_rating:
            return [(row.video_id, row.rating) for row in rows]

        return [row.video_id for row in rows]