from snowflake.snowpark import Session
session = Session.builder \
    .config("connection_name", "default") \
    .create()

customers = session.table("CUSTOMERS")
customers.show()
print(f"Total number of customers: {customers.count()}")

print(type(customers ))
