from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

session = Session.builder \
    .config("connection_name", "default") \
    .create()

customers = session.table("CUSTOMERS")
customers.print_schema()
filtered_customers = customers.filter(col("CITY") == "Chennai")
filtered_customers.show()