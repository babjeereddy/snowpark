from snowflake.snowpark import Session

session = Session.builder \
    .config("connection_name", "default") \
    .create()

print(session.sql("SELECT CURRENT_USER(), CURRENT_ROLE()").collect())
