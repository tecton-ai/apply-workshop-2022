from tecton import BatchSource, SnowflakeConfig
from datetime import datetime


predicted_ratings = BatchSource(
    name="predicted_ratings",
    batch_config=SnowflakeConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="USER_PREDICTED_RATINGS",
      timestamp_field="CREATED_AT",
    ),
)
