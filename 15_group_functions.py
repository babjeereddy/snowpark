from snowflake.snowpark import Session
from snowflake.snowpark.functions import *
session = Session.builder \
    .config("connection_name", "default") \
    .create()
orders = session.table("orders")
grouped_orders = orders.group_by("status").\
        agg( sum("amount").alias("total_amount"),\
            avg("amount").alias("average_amount"),\
            count("*").alias("order_count"),\
            min("amount").alias("min_amount"),\
            max("amount").alias("max_amount") )
grouped_orders.show()

grouped_orders = orders.group_by(year(col("order_date")).alias("order_year")).\
        agg( sum("amount").alias("total_amount"),\
            avg("amount").alias("average_amount"),\
            count("*").alias("order_count"),\
            min("amount").alias("min_amount"),\
            max("amount").alias("max_amount") )
grouped_orders.show()

                