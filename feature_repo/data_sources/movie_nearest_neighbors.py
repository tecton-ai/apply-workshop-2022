from tecton import BatchSource, SnowflakeConfig
from datetime import datetime


movie_nearest_neighbors = BatchSource(
    name="movie_nearest_neighbors",
    batch_config=SnowflakeConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="MOVIE_NEAREST_NEIGHBORS",
      timestamp_field="CREATED_AT",
    ),
)
