from tecton import batch_feature_view, Aggregation
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
        sources=[ratings, movies],
        entities=[user],
        mode='snowflake_sql',
        online=True,
        aggregation_interval=timedelta(days=1),
        aggregations=[
            Aggregation(column='RATING', function='mean', time_window=timedelta(days=730)),
        ],
        feature_start_time=datetime(1997, 1, 1),
        owner='david@tecton.ai',
        description=f'Average rating user has given to {genre} movies in various time windows',
        name=f"user_{genre.replace('-','_')}_rating_history",
    )
    def fv(ratings, movies):
        return f'''
            SELECT
                {ratings}.USER_ID as USER_ID,
                RATING,
                TIMESTAMP
            FROM
                {ratings} inner join {movies} on {ratings}.MOVIE_ID = {movies}.MOVIE_ID
            WHERE
                contains(genres, '{genre}')
            '''
    return fv

preference_features = [gen_preference_feature(genre) for genre in genres]
