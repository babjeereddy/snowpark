from snowflake.snowpark import Session
session = Session.builder \
                    .config("connection_name", "default")\
                    .create()

df = session.sql("""
SELECT
  order_id,
  amount,

  /* Running total by order_id */
  SUM(amount) OVER (
    ORDER BY order_id
    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
  ) AS running_total,

  /* 3-row moving average (prev, current, next) */
  SUM(amount) OVER (
    ORDER BY order_id
    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
  ) AS moving_sum_3_rows

FROM orders
                 
ORDER BY order_id
""")

df.show()

