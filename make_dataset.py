from faker import Faker
from random import randint, sample
from faker.providers import DynamicProvider


# constantes...
INPUT_PATH = 'input/'

HEADER_VIDEO      = 'video_id,name,duration\n'
HEADER_ITERATIONS = 'user_id,video_id,liked,shared,reps,saved,commented\n'
HEADER_RATING     = 'user_id,video_id,rating\n'
HEADER_USER       = 'user_id,name\n'

N_USERS        = 100
N_VIDEOS       = 100
MAX_ITERATIONS = 20
MAX_REPS       = 5
VIDEO_DURATION = (15, 30) # segundos...

W_LIKE      = 0.5
W_SHARED    = 1.0
W_REPS      = 0.5
W_SAVED     = 1.0
W_COMMENTED = 1.0
# rating máximo: 0.5 + 1.0 + 5 * 0.5 + 1.0 + 1.0 => 6.0

fake = Faker()

def run():
    with open(INPUT_PATH + 'video_names.txt', 'r') as f_video_names:
        video_names = DynamicProvider(
            provider_name="video_name",
            elements=f_video_names.read().splitlines(),
        )
        fake.add_provider(video_names)

    # make dataset
    with open(INPUT_PATH + 'videos.csv', 'w') as f_videos,         \
         open(INPUT_PATH + 'iterations.csv', 'w') as f_iterations, \
         open(INPUT_PATH + 'ratings.csv', 'w') as f_ratings,       \
         open(INPUT_PATH + 'users.csv', 'w') as f_users:
            def randboolean():
                return randint(0, 1)

            # make headers...
            f_videos.write(HEADER_VIDEO)
            f_iterations.write(HEADER_ITERATIONS)
            f_ratings.write(HEADER_RATING)
            f_users.write(HEADER_USER)

            # make videos.csv...
            for video_id in range(1, N_VIDEOS + 1):
                f_videos.write(f'{video_id},{fake.video_name()},{randint(VIDEO_DURATION[0], VIDEO_DURATION[1])}' + '\n')

            for user_id in range(1, N_USERS + 1):
                f_users.write(f'{user_id},{fake.name()}' + '\n')
            
                # videos...
                video_sample = sample(
                    population=range(1, N_VIDEOS + 1), 
                    k=randint(1, MAX_ITERATIONS)
                )

                for video_id in video_sample:
                    like   = randboolean()
                    shared = randboolean()
                    reps   = randint(1, MAX_REPS)
                    saved  = randboolean()
                    commented = randboolean()
                    
                    f_iterations.write(f'{user_id},{video_id},{like},{shared},{reps},{saved},{commented}' + '\n')
                    f_ratings.write(f'{user_id},{video_id},{like*W_LIKE + shared*W_SHARED + reps*W_REPS + saved*W_SAVED + commented*W_COMMENTED}' + '\n')

# run()
if __name__ == 'main':
    run()