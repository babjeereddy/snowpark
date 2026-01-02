from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default").create()


orders_raw = session.table("orders_raw")
orders_raw.show()


# orders_cleared = orders_raw.dropna(subset=["customer_id","order_date"])
# orders_cleared.show()


#drop the duplicate rows based on all columns    
orders_clean = orders_raw.dropna(how="all")
orders_clean.show()

#drop row if specific column has null value
# orders_clean2 = orders_raw.dropna(subset=["customer_id"])


#drop duplicate rows based on specific clumns
# orders_clear3 = orders_raw.dropna(subset=["order_id","customer_id"])

# orders_clear3.show()