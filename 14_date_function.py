from ast import mod
from matplotlib.pylab import power
from snowflake.snowpark import Session
from snowflake.snowpark.functions import *
session = Session.builder\
    .config("connection_name", "default") \
    .create()   

df =session.range(1).to_df("dummy")
# df.show()
# df.select(current_date().alias("current_date"),
#             current_timestamp().alias("current_timestamp"),
#             current_time().alias("current_time")
#              ).show()



orders = session.table("orders")
orders.select( "order_date",
               date_add(col("order_date"), 10).alias("order_date_plus_10_days"),
               date_sub(col("order_date"), 5).alias("order_date_minus_5_days"),
               datediff("day", col("order_date"), current_date()).alias("days_since_order"),
).show()   

# orders.select( "order_date",
#                 year(col("order_date")).alias("order_year"),
#                 quarter(col("order_date")).alias("order_quarter"),
#                 month(col("order_date")).alias("order_month"),
#                 last_day(col("order_date")).alias("order_last_day_of_month"),
#                 dayofmonth(col("order_date")).alias("order_day_of_month"),\\
#                 dayofweek(col("order_date")).alias("order_day_of_week"),
#                 dayofyear(col("order_date")).alias("order_day_of_year")

                
               
# ).show()        


# orders.select( "order_date",
#                 to_char(col("order_date"), 'YYYY-MM-DD').alias("order_date_yyyy_mm_dd"),
#                 to_char(col("order_date"), 'MM/DD/YYYY').alias("order_date_mm_dd_yyyy"),
#                 to_char(col("order_date"), 'Month DD, YYYY').alias("order_date_month_dd_yyyy")              
               
# ).show()    

df.select(to_char(current_timestamp(), 'YYYY/MM/DD HH24:MI:SS AM').alias("current_timestamp_formatted")).show( )

orders.select( "order_date",
              next_day("order_date",'FRIDAY').alias("next_friday_after_order_date")              
).show()

df.select(next_day(current_date(),'MONDAY').alias("next_monday_from_today")).show() 

df.select(abs(-1).alias("absolute_value")).show()  
df.selelct(ceil(2.3).alias("ceiling_value")).show()  
df.select(floor(2.7).alias("floor_value")).show()
df.select(round(2.5678,2).alias("rounded_value")).show()
df.select(trunc(2.9876,2).alias("truncated_value")).show()
df.select(sign(-15).alias("sign_value")).show()
df.select(mod(29, 9).alias("modulus_value")).show()
df.select(power(2, 5).alias("power_value")).show()

df.select(to_char(10000, '9,999,999' ).alias("formatted_number")).show()
df.select(to_date('2024-06-15 14:30:00', 'YYYY-MM-DD HH24:MI:SS').alias("converted_date")).show()




) 
