from snowflake.snowpark import Session
from snowflake.snowpark.functions import *
session = Session.builder\
    .config("connection_name", "default") \
    .create()   
customers = session.table("CUSTOMERS")
# customers.select(concat(col("customer_name"), lit(" - VIP")).alias("CUSTOMER_NAME_VIP")).show()
# customers.select(concat_ws(lit(" | "), "customer_name",\
#                          "city").alias("CUSTOMER_INFO")).show()

# customers.select("customer_name",length("customer_name").alias("CUSTOMER_NAME_LENGTH"))\
#             .order_by(length( col("CUSTOMER_NAME")).desc()).show()
        
# customers.select(trim("CUSTOMER_NAME").alias("CUSTOMER_NAME_TRIMMED")).show()   

# customers.filter(trim(col("CUSTOMER_NAME"))== "Ravi Kumar").show()

# customers.select("customer_name", \
                #  substr("customer_name", 1, 4).alias("CUSTOMER_NAME_SUBSTR")).show()


customers.select("CUSTOMER_NAME",\
                 instr("customer_name", 'n').alias("CUSTOMER_NAME_instr")).show()



customers.select("CUSTOMER_NAME",\
    substr("CUSTOMER_NAME",1 , instr("CUSTOMER_NAME"," ")-1).alias("First_Name"),\
    substr("CUSTOMER_NAME", instr("CUSTOMER_NAME"," ")+1, length("CUSTOMER_NAME"))\
      .alias("Last_Name")).show()



customers.select("CUSTOMER_NAME",\
                 lpad(col("CUSTOMER_NAME"),20,lit('*')).alias("CUSTOMER_NAME_LPAD"),\
                 rpad(col("CUSTOMER_NAME"),20,lit('_')).alias("CUSTOMER_NAME_RPAD")).show()

customers.select("CUSTOMER_NAME",\
                 repeat(col("CUSTOMER_NAME"),2).alias("CUSTOMER_NAME_REPEAT")).show()

from snowflake.snowpark.functions import col, regexp_replace

customers.select(
    "CUSTOMER_NAME",
    regexp_replace(col("CUSTOMER_NAME"), " ", "_").alias("CUSTOMER_NAME_REPLACE")
).show()

customers.select(
    "CUSTOMER_NAME",    
    regexp_replace(col("CUSTOMER_NAME"), "[aeiouAEIOU]", "").alias("CUSTOMER_NAME_NO_VOWELS")
).show()

    