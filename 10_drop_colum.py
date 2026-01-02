from snowflake.snowpark import Session
session = Session.builder \
                 .config("connection_name", "default") \
                 .create()
orders = session.table("orders")
orders_dropped = orders.drop("status")\
                        .drop("amount")

