from tecton import FeatureService
from features.movie_genre_info import movie_genre_info
from features.movie_release_year import movie_release_year
from features.user_genre_ratings import preference_features


batch_movie_recommendations_feature_service = FeatureService(
    name='batch_movie_recommendations_feature_service',
    online_serving_enabled=True,
    features=[
        movie_genre_info,
        movie_release_year,
    ] + preference_features
)
