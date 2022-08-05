from tecton import BatchSource, SnowflakeConfig
from datetime import datetime


tags = BatchSource(
    name="tags",
    batch_config=SnowflakeConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="TAGS",
      timestamp_field="CREATED_AT",
    ),
)
