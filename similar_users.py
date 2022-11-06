import pandas as pd
from model import Video
from recommender import Recommender

# users parecidos: 50, 51, 52...

n_items = 10
r = Recommender()

df = pd.DataFrame(
    {
        'User 50' : [Video().get_by_id(id).name for id in r.recommender(50, n_items)],
        'User 51' : [Video().get_by_id(id).name for id in r.recommender(51, n_items)],
        'User 52' : [Video().get_by_id(id).name for id in r.recommender(52, n_items)],
        'User 93': [Video().get_by_id(id).name for id in r.recommender(93, n_items)]
    }
)

print(df)
