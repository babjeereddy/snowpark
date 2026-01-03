import streamlit as st
from snowflake.snowpark.context import get_active_session

# Snowflake session (native inside Snowflake Streamlit)
session = get_active_session()

st.title("Orders Dashboard")

with st.sidebar:
    st.header("Filters")

    status_list = session.sql("""
        SELECT DISTINCT STATUS
        FROM ORDERS
        WHERE STATUS IS NOT NULL
        ORDER BY STATUS
    """).to_pandas()["STATUS"].tolist()

    selected_statuses = st.multiselect(
        "Order Status",
        options=status_list,
        default= status_list # ALL selected by default
    )

if selected_statuses:
    status_values = ", ".join([f"'{s}'" for s in selected_statuses])
    where_clause = f"WHERE STATUS IN ({status_values})"
else:
    # If user deselects everything → show nothing
    where_clause = "WHERE 1 = 0"

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
        COUNT(DISTINCT ORDER_ID) AS ORDERS_COUNT
    FROM ORDERS
    {where_clause}
    GROUP BY STATUS
    ORDER BY ORDERS_COUNT DESC
""").to_pandas()

st.subheader("Orders Count by Status")

if bar_df.empty:
    st.info("No data available for selected status.")
else:
    st.bar_chart(bar_df.set_index("STATUS")["ORDERS_COUNT"])


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
    LIMIT 500
""").to_pandas()

st.subheader("Orders (Filtered)")
st.dataframe(orders_df, use_container_width=True)

st.success("Dashboard loaded successfully")
