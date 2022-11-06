from make_dataset import MAX_REPS


class Iteration:

    def __init__(self):
        self.__like = 0
        self.__shared = 0
        self.__reps = 1
        self.__saved = 0
        self.__commented = 0


    def reset(self):
        self.__init__()

    def iter_like(self):
        self.__like = 1

    def iter_shared(self):
        self.__shared = 1

    def iter_reps(self):
        if self.__reps < MAX_REPS:
            self.__reps += 1
            return True

        return False

    def iter_saved(self):
        self.__saved = 1

    def iter_commented(self):
        self.__commented = 1

    @property
    def like(self):
        return self.__like

    @property
    def shared(self):
        return self.__shared
    
    @property
    def reps(self):
        return self.__reps

    @property
    def saved(self):
        return self.__saved

    @property
    def commented(self):
        return self.__commented
