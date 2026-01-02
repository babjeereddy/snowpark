from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_

session = Session.builder \
    .config("connection_name", "default") \
    .create()

customers = session.table("orders")
customers_sorted = customers.order_by( col("status").asc(), col("amount").desc())
customers_sorted.show()