from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
session = Session.builder.config("connection_name","default").create()
session.sql(" show tables").select(col('"name"')).show()
session.sql("show schemas").select(col('"name"')).show()
session.sql("show databases").select(col('"name"')).show()
session.sql("show stages").select(col('"name"')).show()
session.sql("desc table orders1").select(col('"name"')).show()