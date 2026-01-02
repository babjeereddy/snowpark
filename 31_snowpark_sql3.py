from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
df = session.sql("""
SELECT order_id,
       customer_id,
       amount ,
       rank() over(order by amount) as order_rank,
       dense_rank() over(order by amount) as dense_rank,
       row_number() over(order by amount) as row_number,
               
FROM orders 
""")
df.show() 
