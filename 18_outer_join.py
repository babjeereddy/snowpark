from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
orders = session.table("orders")
customers = session.table("customers")
joined_data = customers.join(orders, 
                             orders["customer_id"] == customers["customer_id"],
                             how="left")      
joined_data.select("customer_name","order_id", "amount","status").show() 

