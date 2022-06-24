from tecton import batch_feature_view, Aggregation, FilteredSource
from entities import user
from data_sources.movies import movies
from data_sources.ratings import ratings
from datetime import datetime, timedelta

genres = [
    "Action",
    "Adventure",
    "Animation",
    "Children",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Fantasy",
    "Film-Noir",
    "Horror",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Thriller",
    "War",
    "Western"
]

def gen_preference_feature(genre):
    @batch_feature_view(
        sources=[FilteredSource(ratings), movies],
        entities=[user],
        mode='spark_sql',
        online=True,
        offline=True,
        aggregation_interval=timedelta(days=1),
        aggregations=[
            Aggregation(column='rating', function='mean', time_window=timedelta(days=365))
        ],
        feature_start_time=datetime(1997, 1, 1),
        owner='david@tecton.ai',
        description=f'Average rating user has given to {genre} movies in various time windows',
        name=f"user_{genre.replace('-','_').lower()}_rating_history",
    )
    def fv(ratings, movies):
        return f'''
            SELECT
                {ratings}.user_id as user_id,
                rating,
                timestamp
            FROM
                {ratings} inner join {movies} on {ratings}.movie_id = {movies}.movie_id
            WHERE
                genres like '%{genre}%'
            '''
    return fv

preference_features = [gen_preference_feature(genre) for genre in genres]
