from tecton import batch_feature_view, FilteredSource
from entities import movie
from data_sources.movie_nearest_neighbors import movie_nearest_neighbors
from datetime import datetime, timedelta
#
#
@batch_feature_view(
    sources=[FilteredSource(movie_nearest_neighbors)],
    entities=[movie],
    mode='snowflake_sql',
    online=True,
    batch_schedule=timedelta(days=1),
    ttl=timedelta(days=9999),
    feature_start_time=datetime(2022, 5, 1),
    owner='david@tecton.ai',
    description='Nearest neighbors of a given movie'
)
def movie_nearest_neighbors(movie_nearest_neighbors):
    return f'''
        select
            movie_id,
            ARRAY_TO_STRING(NEAREST_NEIGHBORS, ',') as nearest_neighbors,
            created_at
        from
            {movie_nearest_neighbors}
        '''
