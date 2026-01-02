from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
df =session.sql("SELECT * FROM orders")
df.show()
