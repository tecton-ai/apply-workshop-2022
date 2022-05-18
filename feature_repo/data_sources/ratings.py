from tecton import BatchDataSource, SnowflakeDSConfig
from datetime import datetime


ratings = BatchDataSource(
    name="ratings",
    batch_ds_config=SnowflakeDSConfig(
      database="DEV_DAVID",
      schema="MOVIELENS_25M",
      table="RATINGS",
      timestamp_key="TIMESTAMP",
    ),
)
