from tecton import BatchDataSource, SnowflakeDSConfig
from datetime import datetime


predicted_ratings = BatchDataSource(
    name="predicted_ratings",
    batch_ds_config=SnowflakeDSConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="USER_PREDICTED_RATINGS",
      timestamp_key="CREATED_AT",
    ),
)
