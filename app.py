import tkinter as tk, time
from threading import Thread
from random import randint
from faker import Faker
from make_dataset import N_VIDEOS
from model import Iteration, Rating, Video, User
from recommender import Recommender

faker = Faker()

class App(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)

        self.iteration = Iteration()
        self.user      = User(name=faker.name())
        self.rating    = Rating(self.user)
        self.__recommender = Recommender()
        self.__n_items = 5
        self.__videos  = self.random_videos()
        self.__video   = self.__videos.pop(0)

        # icons...
        self.icon_prev    = tk.PhotoImage(file='img/icons8-replace-50.png')
        self.icon_like    = tk.PhotoImage(file='img/icons8-facebook-like-50.png')
        self.icon_next    = tk.PhotoImage(file='img/icons8-next-page-50.png')
        self.icon_comment = tk.PhotoImage(file='img/icons8-comments-50.png')
        self.icon_shared  = tk.PhotoImage(file='img/icons8-share-50.png')
        self.icon_saved   = tk.PhotoImage(file='img/icons8-save-50.png')

        # video label...
        self.label_video = tk.Label(width=15, text=self.__video.name, font=('Arial bold', 20), pady=20)
        self.label_video.grid(row=0, column=2)

        # prev button...
        self.button_prev = tk.Button(image=self.icon_prev, command=self.__onclick_prev)
        self.button_prev.grid(row=1, column=1)

        # like button...
        self.button_like = tk.Button(image=self.icon_like, command=self.__onclick_like)
        self.button_like.grid(row=1, column=2)

        # next button...
        self.button_next = tk.Button(image=self.icon_next, command=self.__onclick_next).grid(row=1, column=3)

        # comment button...
        self.button_comment = tk.Button(image=self.icon_comment, command=self.__onclick_comment)
        self.button_comment.grid(row=2, column=1)

        # shared button...
        self.button_shared = tk.Button(image=self.icon_shared, command=self.__onclick_shared)
        self.button_shared.grid(row=2, column=2)

        # saved button...
        self.button_saved = tk.Button(image=self.icon_saved, command=self.__onclick_saved,)
        self.button_saved.grid(row=2, column=3)

        self.thread = Thread()

    def recommender(self):
        self.__videos.extend([Video().get_by_id(id) for id in self.__recommender.recommender(self.user.id, self.__n_items)])
    
    def random_videos(self):
        return [Video().get_by_id(id) for id in [randint(0, N_VIDEOS) for _ in range(self.__n_items)]]

    def save_iteration(self):
        self.rating.save(self.__video, self.iteration)
        self.iteration.reset()

    def update_video(self):
        self.__manager_buttons('active')
        
        # print videos...
        print('Vídeos na lista...')
        print('(')
        for video in self.__videos:
            print(video.name)
        print(')', '\n')

        if len(self.__videos) < 5 and not self.thread.is_alive():
            print('Atualizando o feed...')
            self.thread = Thread(target=self.recommender)
            self.thread.start()
            self.__n_items += 5 if self.__n_items < 15 else 0

        if not self.__videos: # evita que a lista de videos fique vazia...
            self.__videos = self.random_videos()

        self.__video = self.__videos.pop(0)
        self.label_video.config(text=self.__video.name)

    # onclicks...
    def __onclick_prev(self):
        if not self.iteration.iter_reps():
            self.__disable_button(self.button_prev)

    def __onclick_like(self):
        self.iteration.iter_like()
        self.__disable_button(self.button_like)

    def __onclick_next(self):
        self.save_iteration()
        self.update_video()

    def __onclick_comment(self):
        self.iteration.iter_commented()
        self.__disable_button(self.button_comment)

    def __onclick_shared(self):
        self.iteration.iter_shared()
        self.__disable_button(self.button_shared)

    def __onclick_saved(self):
        self.iteration.iter_saved()
        self.__disable_button(self.button_saved)

    def __disable_button(self, button):
        button['state'] = 'disabled'

    def __manager_buttons(self, mode):
        self.button_like['state']    = mode
        self.button_comment['state'] = mode
        self.button_shared['state']  = mode
        self.button_saved['state']   = mode
        self.button_prev['state']    = mode
