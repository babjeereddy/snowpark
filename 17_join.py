from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
orders = session.table("orders")
customers = session.table("customers")
joined_data = orders.join(customers, orders["customer_id"] == customers["customer_id"],
                          join_type="full" )        
joined_data.select("order_id", "customer_name", "amount","status").show() 


