import streamlit as st
from snowflake.snowpark.context import get_active_session

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

    ALL_OPTION = "ALL"

    # Dropdown options include ALL + actual statuses
    options = [ALL_OPTION] + status_list

    # Default: ALL
    selected_statuses = st.multiselect(
        "Order Status (Multi-select)",
        options=options,
        default=[ALL_OPTION]
    )

  
    # If ALL is selected along with others, keep only ALL
    if ALL_OPTION in selected_statuses and len(selected_statuses) > 1:
        selected_statuses = [ALL_OPTION]
        st.session_state["Order Status (Multi-select)"] = selected_statuses  # optional helper

if not selected_statuses:
    where_clause = "WHERE 1=0"
elif ALL_OPTION in selected_statuses:
    where_clause = ""
else:
    # Escape single quotes just in case
    safe_vals = [s.replace("'", "''") for s in selected_statuses]
    status_values = ", ".join([f"'{s}'" for s in safe_vals])
    where_clause = f"WHERE STATUS IN ({status_values})"


kpi = session.sql(f"""
    SELECT
        COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS,
        COALESCE(SUM(AMOUNT), 0) AS TOTAL_AMOUNT
    FROM ORDERS
    {where_clause}
""").collect()

c1, c2 = st.columns(2)
c1.metric("Total Orders", kpi[0]["TOTAL_ORDERS"])
c2.metric("Total Amount", f"₹{kpi[0]['TOTAL_AMOUNT']:,.0f}")


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
    st.info("No data available for the selected filter.")
else:
    st.bar_chart(bar_df.set_index("STATUS")["ORDERS_COUNT"])


orders_df = session.sql(f"""
    SELECT
        ORDER_ID, CUSTOMER_ID, ORDER_DATE, AMOUNT, STATUS
    FROM ORDERS
    {where_clause}
    ORDER BY ORDER_DATE DESC
    LIMIT 500
""").to_pandas()

st.subheader("Orders (Filtered)")
st.dataframe(orders_df, use_container_width=True)

st.success("Dashboard loaded successfully")
