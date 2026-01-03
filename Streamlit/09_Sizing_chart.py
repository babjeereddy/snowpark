import streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session


st.set_page_config(page_title="Orders Dashboard", layout="wide")
session = get_active_session()

ALL_OPTION = "ALL"

st.title("Orders Dashboard")

with st.sidebar:
    st.header("Filters")

    status_list = session.sql("""
        SELECT DISTINCT STATUS
        FROM ORDERS
        WHERE STATUS IS NOT NULL
        ORDER BY STATUS
    """).to_pandas()["STATUS"].tolist()

    options = [ALL_OPTION] + status_list

    selected_statuses = st.multiselect(
        "Order Status",
        options=options,
        default=[ALL_OPTION]
    )

    st.divider()
    st.header("Chart Size")
    chart_width = st.slider("Chart width (px)", 400, 1400, 800, 50)
    chart_height = st.slider("Chart height (px)", 250, 900, 400, 50)


if not selected_statuses:
    where_clause = "WHERE 1=0"

elif ALL_OPTION in selected_statuses:
    # If ALL is selected (even with others), treat as ALL
    where_clause = ""

else:
    status_values = ", ".join(f"'{s}'" for s in selected_statuses)
    where_clause = f"WHERE STATUS IN ({status_values})"

# KPI
kpi = session.sql(f"""
    SELECT
        COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS,
        COALESCE(SUM(AMOUNT), 0) AS TOTAL_AMOUNT,
        COUNT(DISTINCT CUSTOMER_ID) AS UNIQUE_CUSTOMERS
    FROM ORDERS
    {where_clause}
""").collect()[0]

k1, k2, k3 = st.columns(3)
k1.metric("Total Orders", f"{int(kpi['TOTAL_ORDERS'] or 0):,}")
k2.metric("Total Amount", f"₹{float(kpi['TOTAL_AMOUNT'] or 0):,.0f}")
k3.metric("Unique Customers", f"{int(kpi['UNIQUE_CUSTOMERS'] or 0):,}")

st.divider()

# HORIZONTAL BAR CHART
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
    st.info("No data available for selected filter.")
else:
    hbar = (
    alt.Chart(bar_df)
    .mark_bar()
    .encode(
        y=alt.Y("STATUS:N", sort="-x", title="Status"),
        x=alt.X(
            "ORDERS_COUNT:Q",
            title="Orders",
            axis=alt.Axis(format="d")   # 👈 FIX HERE
        ),
        tooltip=[
            "STATUS:N",
            alt.Tooltip("ORDERS_COUNT:Q", format="d")
        ]
    )
    .properties(
        width=chart_width,
        height=chart_height
    )
)


    st.altair_chart(hbar, use_container_width=False)

