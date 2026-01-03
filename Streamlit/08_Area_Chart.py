import streamlit as st
import altair as alt
from snowflake.snowpark.context import get_active_session

# CONFIG
st.set_page_config(page_title="Orders Area Chart", layout="wide")
session = get_active_session()

ALL_OPTION = "ALL"

st.title("Orders Trend – Area Chart")

# SIDEBAR: FILTERS + SIZE
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
    chart_width = st.slider("Chart width (px)", 500, 1400, 900, 50)
    chart_height = st.slider("Chart height (px)", 250, 800, 400, 50)

# -----------------------------
# WHERE CLAUSE
# -----------------------------
if not selected_statuses:
    where_clause = "WHERE 1=0"
elif ALL_OPTION in selected_statuses:
    where_clause = ""
else:
    safe_vals = [s.replace("'", "''") for s in selected_statuses]
    status_values = ", ".join(f"'{s}'" for s in safe_vals)
    where_clause = f"WHERE STATUS IN ({status_values})"

# KPI
kpi = session.sql(f"""
    SELECT
        COUNT(DISTINCT ORDER_DADTE) AS TOTAL_ORDERS,
        COALESCE(SUM(AMOUNT), 0) AS TOTAL_AMOUNT
    FROM ORDERS
    {where_clause}
""").collect()[0]

k1, k2 = st.columns(2)
k1.metric("Total Orders", f"{int(kpi['TOTAL_ORDERS'] or 0):,}")
k2.metric("Total Amount", f"₹{float(kpi['TOTAL_AMOUNT'] or 0):,.0f}")

st.divider()

# DATA FOR AREA CHART
area_df = session.sql(f"""
    SELECT
        ORDER_DATE::date AS ORDER_DATE,
        COUNT(DISTINCT ORDER_ID) AS ORDERS_COUNT
    FROM ORDERS
    {where_clause}
    GROUP BY ORDER_DATE::date
    ORDER BY ORDER_DATE::date
""").to_pandas()

st.subheader("Orders Trend Over Time")

# AREA CHART
if area_df.empty:
    st.info("No data available for the selected filter.")
else:
    area_chart = (
        alt.Chart(area_df)
        .mark_area(opacity=0.6, interpolate="monotone")
        .encode(
            x=alt.X("ORDER_DATE:T", title="Order Date"),
            y=alt.Y(
                "ORDERS_COUNT:Q",
                title="Orders",
                axis=alt.Axis(format="d")
            ),
            tooltip=[
                alt.Tooltip("ORDER_DATE:T", title="Date"),
                alt.Tooltip("ORDERS_COUNT:Q", format="d", title="Orders")
            ]
        )
        .properties(
            width=chart_width,
            height=chart_height
        )
    )

    st.altair_chart(area_chart, use_container_width=False)

st.success("Area chart loaded successfully ✅")
