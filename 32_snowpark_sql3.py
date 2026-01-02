from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default")\
                    .create()

df = session.sql("""SELECT order_id,
       amount,
         max(amount) over() as max_amount,
         min(amount) over() as min_amount,
         avg(amount) over() as avg_mount,
         count(amount) over() as total_orders,
         sum(amount) over() as sum_amount,
         sum(amount) over(order by amount 
                 rows between unbounded preceding and  current row )
                 as running_sum                 
FROM orders 
""")
df.show()

