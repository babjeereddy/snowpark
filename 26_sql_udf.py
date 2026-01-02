from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()

session.sql("""
CREATE OR REPLACE FUNCTION STATUS_3CHAR_UDF(status STRING)
RETURNS STRING
LANGUAGE SQL
AS
$$
  CASE
    WHEN status IS NULL THEN NULL
    ELSE UPPER(SUBSTR(status, 1, 3))
  END
$$
""").collect()
df = session.table("orders1")
from snowflake.snowpark.functions import col, call_udf

df = session.table("ORDERS")

df.select(
    col("ORDER_ID"),
    col("STATUS"),
    call_udf("STATUS_3CHAR_UDF", col("STATUS")).alias("STATUS_3CHAR")
).show()
