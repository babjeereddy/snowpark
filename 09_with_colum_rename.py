from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
session = Session.builder \
    .config("connection_name", "default") \
    .create()
orders = session.table("orders")
orders_renamed = orders.with_column_renamed("amount", "total_amount")\
                       .with_column_renamed("status", "order_status")

orders.select(col("ORDER_ID"), col("AMOUNT").alias("total_amount"), 
                col("STATUS").alias("order_status")).show()

orders_renamed.show()
