from model import Video
from recommender import Recommender

# users parecidos: 50, 51, 52...

def show(videos):
    for video in videos:
        print(video.name, end=', ')

n_items = 10
r = Recommender()

print('Videos recomendados para o usuário 50')
show([Video().get_from_id(id) for id in r.recommender(50, n_items)])
print('#' * 15)

print('Videos recomendados para o usuário 51')
show([Video().get_from_id(id) for id in r.recommender(51, n_items)])
print('#' * 15)

print('Videos recomendados para o usuário 52')
show([Video().get_from_id(id) for id in r.recommender(52, n_items)])
print('#' * 15)
