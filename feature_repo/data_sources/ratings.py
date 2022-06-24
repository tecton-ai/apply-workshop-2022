from tecton import BatchSource, HiveConfig, DatetimePartitionColumn
from datetime import datetime


partition_columns = [
    DatetimePartitionColumn(column_name="year", datepart="year", zero_padded=True),
]

ratings = BatchSource(
    name="ratings",
    batch_config=HiveConfig(
      database="demo_recsys",
      table="ratings",
      timestamp_field="timestamp",
      datetime_partition_columns=partition_columns
    ),
)
