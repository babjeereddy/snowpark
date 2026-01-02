from snowflake.snowpark import Session
from snowflake.snowpark.functions import *
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
df =session.table("orders")
db_grouped = df.group_by("STATUS").agg(
    sum(col("AMOUNT")).alias("TOTAL_AMOUNT"),
    max(col("AMOUNT")).alias("MAX_AMOUNT"),
    min(col("AMOUNT")).alias("MIN_AMOUNT"),
    avg(col("AMOUNT")).alias("AVG_AMOUNT"),
    count(col("ORDER_ID")).alias("ORDER_COUNT")
)
db_grouped.write.save_as_table("orders_category_summary",mode="overwrite")  
orders_summary_df = session.table("orders_category_summary")
orders_summary_df.show()


