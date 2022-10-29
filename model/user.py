from spark import Spark
from pyspark.sql.functions import col, max
from make_dataset import INPUT_PATH


class User(Spark):

    def __init__(self, name, id=None):
        self.__id = id if id != None else self.next_id()
        self.__name = name

        if id is None:
            self.__save()

    def next_id(self):
        df_users = super().spark.read.csv(INPUT_PATH + 'users.csv', header=True)
        df_users = df_users.withColumn('user_id', col('user_id').cast('integer'))
        return df_users.agg(max('user_id')).collect()[0][0] + 1

    def __save(self):
        with open(INPUT_PATH + 'users.csv', 'a') as f_users:
            f_users.write(f'{self.__id},{self.__name}' + '\n')

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name
