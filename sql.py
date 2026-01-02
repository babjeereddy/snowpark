from snowflake.snowpark import Session
from snowflake.snowpark.functions import when, col
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()

orders = session.sql("""
                      select order_id, order_date, amount 
                     from orders where amount > 1000
                     order by amount desc 
                     """)
orders.show()

orders_grouped = session.sql("""
                             select status , 
                                   sum(amount ) as total_amout,
                                   max(amount) max_amount,
                                   min(amount) min_amount,
                                   avg(amount)  avg_amount
                             from orders
                             group by status       
                             """)
orders_grouped.show()    

orders_rank = session.sql(""" select order_id, amount, 
                                rank() over(order by amount) order_rank                   
                             from orders """)
orders_rank.show()
