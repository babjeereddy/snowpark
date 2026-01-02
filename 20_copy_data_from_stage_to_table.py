# create table if not exists orders1(order_id INT, order_date timestamp ,
# customer_id INT, stataus STRING );

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, year

session = Session.builder.config("connection_name","default").create()
session.sql("""
    COPY INTO orders1
    FROM @my_csv_stage/orders1
    FILE_FORMAT = (TYPE = 'CSV'  SKIP_HEADER = 1);
""").collect()

print("Data copied from stage to table successfully.")
orders1 = session.table("orders1")
orders1_grouped = orders1.group_by(["status", year(col("order_date"))\
                        .alias("order_year")]).count()\
                        .sort("status")

orders1_grouped.show()
