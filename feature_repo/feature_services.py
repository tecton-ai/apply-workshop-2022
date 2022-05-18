from tecton import FeatureService
from features.movie_genre_info import movie_genre_info
from features.movie_release_year import movie_release_year
from features.user_genre_ratings import preference_features
from features.user_batch_movie_recommendations import user_recommended_movies
from features.movie_nearest_neighbors import movie_nearest_neighbors

batch_movie_recommendations_feature_service = FeatureService(
    name='batch_movie_recommendations_feature_service',
    online_serving_enabled=True,
    features=[
        movie_genre_info,
        movie_release_year,
    ] + preference_features
)
