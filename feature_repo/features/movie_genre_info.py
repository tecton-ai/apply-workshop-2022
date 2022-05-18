from tecton import batch_feature_view, FeatureAggregation
from entities import movie
from data_sources.movies import movies
from datetime import datetime


@batch_feature_view(
    sources=[movies],
    entities=[movie],
    mode='snowflake_sql',
    online=True,
    batch_schedule='1d',
    ttl='9999d',
    feature_start_time=datetime(1997, 1, 1),
    owner='david@tecton.ai',
    description='Static information about movie genres',
    family='Recommendations'
)
def movie_genre_info(movies):
    return f'''
        SELECT
            MOVIE_ID,
            cast(contains(genres, 'Action') as int) as is_action,
            cast(contains(genres, 'Animation') as int) as is_animation,
            cast(contains(genres, 'Adventure') as int) as is_adventure,
            cast(contains(genres, 'Children') as int) as is_children,
            cast(contains(genres, 'Comedy') as int) as is_comedy,
            cast(contains(genres, 'Crime') as int) as is_crime,
            cast(contains(genres, 'Documentary') as int) as is_documentary,
            cast(contains(genres, 'Drama') as int) as is_drama,
            cast(contains(genres, 'Fantasy') as int) as is_fantasy,
            cast(contains(genres, 'Film-Noir') as int) as is_film_noir,
            cast(contains(genres, 'Horror') as int) as is_horror,
            cast(contains(genres, 'Musical') as int) as is_musical,
            cast(contains(genres, 'Mystery') as int) as is_mystery,
            cast(contains(genres, 'Romance') as int) as is_romance,
            cast(contains(genres, 'Sci-Fi') as int) as is_scifi,
            cast(contains(genres, 'Thriller') as int) as is_thriller,
            cast(contains(genres, 'War') as int) as is_war,
            cast(contains(genres, 'Western') as int) as is_western,
            CREATED_AT as TIMESTAMP
        FROM
            {movies}
        '''
