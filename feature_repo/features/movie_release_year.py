from tecton import batch_feature_view, FilteredSource
from entities import movie
from data_sources.movies import movies
from datetime import datetime, timedelta
#
#
@batch_feature_view(
    sources=[FilteredSource(movies)],
    entities=[movie],
    mode='snowflake_sql',
    online=True,
    batch_schedule=timedelta(days=1),
    ttl=timedelta(days=9999),
    feature_start_time=datetime(1997, 1, 1),
    owner='david@tecton.ai',
    description='A movies release date',
)
def movie_release_year(movies):
    return f'''
        SELECT
            MOVIE_ID,
            YEAR,
            CREATED_AT as TIMESTAMP
        FROM
            {movies}
        '''
