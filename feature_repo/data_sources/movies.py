from tecton import BatchSource, HiveConfig
from datetime import datetime


# partition_columns = [
#     DatetimePartitionColumn(column_name="partition_0", datepart="year", zero_padded=True),
#     DatetimePartitionColumn(column_name="partition_1", datepart="month", zero_padded=True),
#     DatetimePartitionColumn(column_name="partition_2", datepart="day", zero_padded=True),
# ]

movies = BatchSource(
    name="movies",
    batch_config=HiveConfig(
      database="demo_recsys",
      table="movies",
      timestamp_field="created_at",
    ),
)
