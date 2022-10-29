from tkinter import Tk
from app import App


root = Tk()
root.title('SM Recommender')
root.geometry('400x200')
app = App(root)
root.mainloop()
