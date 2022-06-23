from tecton import FeatureService
from features.movie_release_year import movie_release_year
from features.user_genre_ratings import preference_features
from features.user_batch_movie_recommendations import user_recommended_movies
from features.movie_nearest_neighbors import movie_nearest_neighbors
from features.user_recently_watched import user_recently_watched


batch_recommendations_prediction_service = FeatureService(
    name='batch_recommendations_prediction_service',
    online_serving_enabled=True,
    features=[user_recommended_movies]
)


movie_nearest_neighbors_service = FeatureService(
    name='movie_nearest_neighbors_service',
    online_serving_enabled=True,
    features=[movie_nearest_neighbors]
)

user_recently_watched_service = FeatureService(
    name='user_recently_watched_service',
    online_serving_enabled=True,
    features=[user_recently_watched]
)
