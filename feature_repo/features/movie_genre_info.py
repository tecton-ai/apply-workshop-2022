from tecton import batch_feature_view, FilteredSource
from entities import movie
from data_sources.movies import movies
from datetime import datetime, timedelta


@batch_feature_view(
    sources=[FilteredSource(movies)],
    entities=[movie],
    mode='spark_sql',
    online=True,
    offline=True,
    batch_schedule=timedelta(days=1),
    ttl=timedelta(days=9999),
    feature_start_time=datetime(1997, 1, 1),
    owner='david@tecton.ai',
    description='Static information about movie genres',
)
def movie_genre_info(movies):
    return f'''
        SELECT
            movie_id,
            cast(genres like '%Action%' as int) as is_action,
            cast(genres like '%Animation%' as int) as is_animation,
            cast(genres like '%Adventure%' as int) as is_adventure,
            cast(genres like '%Children%' as int) as is_children,
            cast(genres like '%Comedy%' as int) as is_comedy,
            cast(genres like '%Crime%' as int) as is_crime,
            cast(genres like '%Documentary%' as int) as is_documentary,
            cast(genres like '%Drama%' as int) as is_drama,
            cast(genres like '%Fantasy%' as int) as is_fantasy,
            cast(genres like '%Film-Noir%' as int) as is_film_noir,
            cast(genres like '%Horror%' as int) as is_horror,
            cast(genres like '%Musical%' as int) as is_musical,
            cast(genres like '%Mystery%' as int) as is_mystery,
            cast(genres like '%Romance%' as int) as is_romance,
            cast(genres like '%Sci-Fi%' as int) as is_scifi,
            cast(genres like '%Thriller%' as int) as is_thriller,
            cast(genres like '%War%' as int) as is_war,
            cast(genres like '%Western%' as int) as is_western,
            created_at as timestamp
        FROM
            {movies}
        '''
