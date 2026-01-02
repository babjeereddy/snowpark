from snowflake.snowpark.functions import udf, col
from snowflake.snowpark.types import StringType
from snowflake.snowpark import Session
# Create session
session = Session.builder.config("connection_name", "default").create()


def status_prefix_py(status):
    if status is None:
        return None
    return status[:3]

status_prefix_udf = udf(
    func=status_prefix_py,
    return_type=StringType(),
    input_types=[StringType()],
    name="STATUS_PREFIX_UDF"
)
# Use UDF
df = session.table("orders1")
df.select("STATAUS", status_prefix_udf(col("STATAUS")).alias("STATAUS_PREFIX")).show()
