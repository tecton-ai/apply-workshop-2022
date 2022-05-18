from tecton import batch_feature_view, FeatureAggregation, materialization_context
from entities import user
from data_sources.predicted_ratings import predicted_ratings
from datetime import datetime
#
#
@batch_feature_view(
    sources=[predicted_ratings],
    entities=[user],
    mode='snowflake_sql',
    online=True,
    batch_schedule='1d',
    ttl='9999d',
    feature_start_time=datetime(2022, 5, 1),
    owner='david@tecton.ai',
    description='Recommended movies for a user (batch predicted)'
)
def user_recommended_movies(predicted_ratings, context=materialization_context()):
    return f'''
        with most_recent_predictions as
            (
          select
            user_id,
            movie_id,
            predicted_rating,
            created_at,
            row_number() over (partition by user_id, movie_id order by created_at desc) as most_recent
          from
            {predicted_ratings}
          where created_at < '{context.feature_end_time_string}'),
        ranked_choices as
          (select
              user_id,
              movie_id,
              predicted_rating,
              created_at,
              row_number() over (partition by user_id order by predicted_rating desc) as row_number
          from
              most_recent_predictions
          where most_recent=1
          order by row_number asc)
        select
            user_id,
            ARRAY_TO_STRING(arrayagg(movie_id), ',') as recommended_movies,
            max(created_at) as timestamp
        from
            ranked_choices
        where row_number < 51
        group by
            user_id
        '''
