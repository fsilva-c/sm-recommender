import tkinter as tk
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
        self.__videos  = [Video().get_from_id(randint(0, N_VIDEOS))]
        self.__n_items = 0

        # icons...
        self.icon_prev    = tk.PhotoImage(file='img/icons8-back-to-50.png')
        self.icon_like    = tk.PhotoImage(file='img/icons8-facebook-like-50.png')
        self.icon_next    = tk.PhotoImage(file='img/icons8-next-page-50.png')
        self.icon_comment = tk.PhotoImage(file='img/icons8-comments-50.png')
        self.icon_shared  = tk.PhotoImage(file='img/icons8-share-50.png')
        self.icon_saved   = tk.PhotoImage(file='img/icons8-save-50.png')

        # video label...
        self.label_video = tk.Label(width=15, text=self.__videos[0].name, font=('Arial bold', 20), pady=20)
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

        self.update_label_video()

    def update_label_video(self, click=False):
        if not self.__videos:
            print('Atualizando o feed...')
            self.__n_items += 5
            self.__videos = [Video().get_from_id(id) for id in self.__recommender.recommender(self.user.id, self.__n_items)]

        video = self.__videos.pop(0)

        self.label_video.config(text=video.name)
        
        if not click:
            self.after(video.duration * 1000, self.update_label_video)
        
        self.__active_buttons()
        self.rating.save(video, self.iteration)
        self.iteration = Iteration() # reseta as iterações...


    # onclicks...
    def __onclick_prev(self):
        if not self.iteration.iter_reps():
            self.__disable_button(self.button_prev)

    def __onclick_like(self):
        self.iteration.iter_like()
        self.__disable_button(self.button_like)

    def __onclick_next(self):
        self.update_label_video(click=True)

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

    def __active_buttons(self):
        self.button_like['state']    = 'active'
        self.button_comment['state'] = 'active'
        self.button_shared['state']  = 'active'
        self.button_saved['state']   = 'active'
        self.button_prev['state']    = 'active'
