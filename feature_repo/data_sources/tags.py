from tecton import BatchDataSource, SnowflakeDSConfig
from datetime import datetime


tags = BatchDataSource(
    name="tags",
    batch_ds_config=SnowflakeDSConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="TAGS",
      timestamp_key="CREATED_AT",
    ),
)
