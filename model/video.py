from spark import Spark
from make_dataset import INPUT_PATH


class Video(Spark):

    def get_from_id(self, id):
        df_videos = super().spark.read.csv(INPUT_PATH + 'videos.csv', header=True)
        video = df_videos.filter(f'video_id = {id}').select(['video_id', 'name', 'duration']).collect()[0]
        self.__id = video.video_id
        self.__name = video.name
        self.__duration = int(video.duration)
        return self

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def duration(self):
        return self.__duration
