from tecton import BatchSource, SnowflakeConfig
from datetime import datetime


ratings = BatchSource(
    name="ratings",
    batch_config=SnowflakeConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="RATINGS",
      timestamp_field="TIMESTAMP",
    ),
)
