import pandas as pd
from model import Video
from recommender import Recommender

# users parecidos: 50, 51, 52...

n_items = 10
r = Recommender()

def get_recommendations(user_id):
    return [(Video().get_by_id(video_id).name, rating) for video_id, rating in r.recommender(user_id, n_items, col_rating=True)]

df = pd.DataFrame(
    {
        'User 50': get_recommendations(user_id=50),
        'User 51': get_recommendations(user_id=51),
        'User 52': get_recommendations(user_id=52),
        'User 93': get_recommendations(user_id=93)
    }
)

print()
print('Recomendações geradas para os usuários 50, 51, 52 e 93')
print()
print(df)
print()
