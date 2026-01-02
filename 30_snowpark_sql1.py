from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()

df =session.sql("SELECT order_id,customer_id,amount FROM orders WHERE amount >3000")
df.show()