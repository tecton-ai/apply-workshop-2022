from tecton import batch_feature_view, FeatureAggregation
from entities import movie
from data_sources.movies import movies
from datetime import datetime
#
#
@batch_feature_view(
    sources=[movies],
    entities=[movie],
    mode='snowflake_sql',
    online=True,
    batch_schedule='1d',
    ttl='9999d',
    feature_start_time=datetime(1997, 1, 1),
    owner='david@tecton.ai',
    description='A movies release date',
    family='Recommendations'
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
