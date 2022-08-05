from tecton import BatchSource, SnowflakeConfig
from datetime import datetime


movies = BatchSource(
    name="movies",
    batch_config=SnowflakeConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="MOVIES",
      timestamp_field="CREATED_AT",
    ),
)
