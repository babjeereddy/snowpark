from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, sum as sum_

session = Session.builder \
    .config("connection_name", "default") \
    .create()

customers = session.table("CUSTOMERS")
customers.print_schema()
projected_customers = customers.select("CUSTOMER_ID", "CUSTOMER_NAME", "CITY")    
projected_customers.show()