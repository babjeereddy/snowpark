import streamlit as st
from snowflake.snowpark.context import get_active_session

# Snowflake session (no credentials needed inside Snowflake Streamlit)
session = get_active_session()

st.title("Orders Dashboard")

status_list = session.sql("""
    SELECT DISTINCT STATUS
    FROM ORDERS
    WHERE STATUS IS NOT NULL
    ORDER BY STATUS
""").to_pandas()["STATUS"].tolist()

status_options = ["ALL"] + status_list
selected_status = st.selectbox("Filter by Order Status", status_options)


where_clause = "" if selected_status == "ALL" else f"WHERE STATUS = '{selected_status}'"

kpi = session.sql(f"""
    SELECT
        COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS,
        COALESCE(SUM(AMOUNT), 0) AS TOTAL_AMOUNT
    FROM ORDERS
    {where_clause}
""").collect()

total_orders = kpi[0]["TOTAL_ORDERS"]
total_amount = kpi[0]["TOTAL_AMOUNT"]

c1, c2 = st.columns(2)
c1.metric("Total Orders", total_orders)
c2.metric("Total Amount", f"₹{total_amount:,.0f}")

bar_df = session.sql(f"""
    SELECT
        STATUS,
        SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM ORDERS
    {where_clause}
    GROUP BY STATUS
    ORDER BY TOTAL_AMOUNT DESC
""").to_pandas()

st.subheader("Amount by Status")
if bar_df.empty:
    st.info("No data available for the selected status.")
else:
    st.bar_chart(bar_df.set_index("STATUS")["TOTAL_AMOUNT"])


orders_df = session.sql(f"""
    SELECT
        ORDER_ID,
        CUSTOMER_ID,
        ORDER_DATE,
        AMOUNT,
        STATUS
    FROM ORDERS
    {where_clause}
    ORDER BY ORDER_DATE DESC
  
""").to_pandas()

st.subheader("Orders (Filtered)")
st.dataframe(orders_df, use_container_width=True)

st.success("Dashboard loaded successfully")
