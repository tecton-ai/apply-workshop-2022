from tecton import batch_feature_view, FeatureAggregation
from entities import user
from data_sources.movies import movies
from data_sources.ratings import ratings
from datetime import datetime

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
        aggregation_slide_period='1d',
        aggregations=[
            FeatureAggregation(column='RATING', function='mean', time_windows=['730d']),
        ],
        feature_start_time=datetime(1997, 1, 1),
        owner='david@tecton.ai',
        description=f'Average rating user has given to {genre} movies in various time windows',
        name_override=f"user_{genre.replace('-','_')}_rating_history",
        family='Recommendations'
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
