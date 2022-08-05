from tecton import batch_feature_view, FilteredSource, materialization_context
from entities import user
from data_sources.ratings import ratings
from datetime import datetime, timedelta
#
#
@batch_feature_view(
    sources=[FilteredSource(ratings)],
    entities=[user],
    mode='snowflake_sql',
    online=True,
    batch_schedule=timedelta(days=1),
    ttl=timedelta(days=9999),
    feature_start_time=datetime(2022, 5, 1),
    owner='david@tecton.ai',
    description='List of movies watched by a user in the last 30 days'
)
def user_recently_watched(ratings, context=materialization_context()):
    return f'''
        select
            user_id,
            ARRAY_TO_STRING(arrayagg(movie_id), ',') as watched_movies,
            to_timestamp('{context.feature_end_time_string}') as timestamp
        from
            {ratings}
        where
            timestamp < '{context.feature_end_time_string}' and timestamp > DATEADD('day', -30, '{context.feature_end_time_string}')
        group by user_id
        '''
