# create or replace stage my_csv_stage;
# snowsql -q "PUT file://c:/data/orders1 @my_csv_stage AUTO_COMPRESS=FALSE;"


from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default") \
                    .create()
df = session.read.option("PARSE_HEADER", True).csv("@my_csv_stage")
df.show()

