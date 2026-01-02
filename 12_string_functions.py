from snowflake.snowpark import Session
from snowflake.snowpark.functions import *
session = Session.builder\
    .config("connection_name", "default") \
    .create()   
customers = session.table("CUSTOMERS")
customers.select(col("customer_name"),\
                upper("CUSTOMER_NAME").alias("CUSTOMER_NAME_UPPER"),\
                lower("CUSTOMER_NAME").alias("CUSTOMER_NAME_LOWER"),\
                initcap("CUSTOMER_NAME").alias("CUSTOMER_NAME_INITCAP")).show()


customers.select("customer_name",\
                 lit("USA").alias("COUNTRY")).show()

customers.select(concat(lit("Hello "), "customer_name").alias("GREETING")).show()

customers.select(concat("customer_id", lit("|"),"customer_name", lit("|"), "city")\
        .alias("CUSTOMER_INFO")).show()



customers.select(concat_ws( lit("|"),"customer_id","customer_name", "city")\
        .alias("CUSTOMER_INFO")).show()

