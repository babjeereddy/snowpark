
from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
