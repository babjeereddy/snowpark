from snowflake.snowpark import Session
from snowflake.snowpark.functions import when, col
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
df =session.table("orders")
df_clean = df.with_column( "order_type",
                          when( col("AMOUNT") >5000,"Excellent" )
                          .when(col("AMOUNT") >2000,"Good" )
                          .otherwise("Average") )
df_clean.write.save_as_table("orders_enhanced",mode="overwrite")    

orders_enhanced_df = session.table("orders_enhanced")
orders_enhanced_df.show()
