import datetime as dt
from decimal import Decimal
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

session = Session.builder.config("connection_name", "default").create()

orders_raw = session.table("ORDERS_RAW")

# # orders_filled = orders_raw.fillna({
# #     "CUSTOMER_ID": 0,
# #     "ORDER_DATE": dt.date(2023, 1, 1),   
# #     "AMOUNT": Decimal(0.0)
# # })
# orders_filled = orders_raw.fillna(0)
# orders_filled.show()

orders_unique = orders_raw.drop_duplicates();
orders_unique.show()

orders_unique = orders_raw.drop_duplicates()
orders_unique.show()