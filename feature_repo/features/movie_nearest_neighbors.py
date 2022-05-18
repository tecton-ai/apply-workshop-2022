from tecton import batch_feature_view, FeatureAggregation, materialization_context
from entities import movie
from data_sources.movie_nearest_neighbors import movie_nearest_neighbors
from datetime import datetime
#
#
@batch_feature_view(
    sources=[movie_nearest_neighbors],
    entities=[movie],
    mode='snowflake_sql',
    online=True,
    batch_schedule='1d',
    ttl='9999d',
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
