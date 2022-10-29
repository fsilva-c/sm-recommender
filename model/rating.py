from make_dataset import W_COMMENTED, W_LIKE, W_REPS, W_SAVED, W_SHARED, INPUT_PATH


class Rating():

    def __init__(self, user):
        self.__user = user

    def save(self, video, iteration):
        rating = iteration.like * W_LIKE +                             \
                 iteration.shared * W_SHARED +                         \
                 iteration.reps * W_REPS + iteration.saved * W_SAVED + \
                 iteration.commented * W_COMMENTED

        with open(INPUT_PATH + 'ratings.csv', 'a') as f_rating:
            f_rating.write(f'{self.__user.id},{video.id},{rating}' + '\n')

        print(f'{self.__user.id},{video.id},{rating}')
