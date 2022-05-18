from tecton import BatchDataSource, SnowflakeDSConfig
from datetime import datetime


movies = BatchDataSource(
    name="movies",
    batch_ds_config=SnowflakeDSConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="MOVIES",
      timestamp_key="CREATED_AT",
    ),
)
