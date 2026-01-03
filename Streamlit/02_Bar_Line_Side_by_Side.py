import streamlit as st

from snowflake.snowpark.context import get_active_session

# Get Snowflake session
session = get_active_session()

st.title("Orders Dashboard")

kpi_result = session.sql("""
    SELECT
        COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS,
        SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM ORDERS
""").collect()

total_orders = kpi_result[0]["TOTAL_ORDERS"]
total_amount = kpi_result[0]["TOTAL_AMOUNT"]

col1, col2 = st.columns(2)

col1.metric("Total Orders", total_orders)
col2.metric("Total Amount", f"₹{total_amount:,.0f}")


# CHART DATA

# Line chart – daily sales trend
trend_df = session.sql("""
    SELECT
        ORDER_DATE,
        SUM(AMOUNT) AS DAILY_AMOUNT
    FROM ORDERS
    GROUP BY ORDER_DATE
    ORDER BY ORDER_DATE
""").to_pandas()

# Bar chart – amount by status
status_df = session.sql("""
    select CUSTOMER_NAME,sum(amount) TOTAL_AMOUNT
    from customers c join orders o on c.customer_id = o.customer_id
    group by customer_name
""").to_pandas()

# CHART SECTION (SIDE BY SIDE)
st.subheader("Order Analytics")

col3, col4 = st.columns(2)


with col3:
    st.write("Daily Sales Trend")
    st.line_chart(
        trend_df.set_index("ORDER_DATE")["DAILY_AMOUNT"]
    )

with col4:
    st.write("Amount by Order Status")
    st.bar_chart(
        status_df.set_index("CUSTOMER_NAME")["TOTAL_AMOUNT"]
    )

cust_df = session.sql("""
with emp_group as (
   select customer_name,sum(amount) total_amount
   from customers c join orders o on c.customer_id = o.customer_id
   group by customer_name)

select customer_name,total_amount, rank() over(order by total_amount desc ) customer_rank
from emp_group

""").to_pandas()

st.dataframe(cust_df)
