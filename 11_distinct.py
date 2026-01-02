from snowflake.snowpark import Session
session = Session.builder \
                 .config("connection_name", "default") \
                 .create()
orders = session.table("orders")
distinct_orders_status = orders.select("status").distinct()
distinct_orders_status.show()


