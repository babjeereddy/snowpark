from snowflake.snowpark import Session
from snowflake.snowpark.functions import *

session = Session.builder \
    .config("connection_name", "default") \
    .create()
orders = session.table("orders")
orders_with_discount = orders.with_column("DIS10%", col("amount") * 0.9)\
                            .with_column("DIS20%", col("amount") * 0.8)\
                            .with_column("DIS30%", col("amount") * 0.7)
orders_with_discount.select\
    ("ORDER_ID", "amount", "DIS10%", "DIS20%", "DIS30%").show()

