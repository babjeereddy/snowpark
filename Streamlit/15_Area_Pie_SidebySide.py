import streamlit as st
from snowflake.snowpark.context import get_active_session
import plotly.express as px

st.set_page_config(page_title="Orders Area Chart", layout="wide")
st.title("Orders Trend (Area Chart)")

session = get_active_session()


status_rows = session.sql("""
    SELECT DISTINCT STATUS
    FROM ORDERS
    WHERE STATUS IS NOT NULL
    ORDER BY STATUS
""").collect()

status_list = ["ALL"] + [r["STATUS"] for r in status_rows]

with st.sidebar:
    st.header("Filters")
    selected_status = st.selectbox("Select Status", status_list, index=0)

where_clause = "" if selected_status == "ALL" else f"WHERE STATUS = '{selected_status}'"


query = f"""
    SELECT
        ORDER_DATE,
        
        SUM(AMOUNT)* 1.2 AS PROFIT,
        SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM ORDERS
    {where_clause}
    GROUP BY ORDER_DATE
    ORDER BY ORDER_DATE
"""
df = session.sql(query).to_pandas()

query1 = f"""
    SELECT
        STATUS,
        SUM(AMOUNT) AS TOTAL_AMOUNT
    FROM ORDERS
    {where_clause}
    GROUP BY STATUS
    ORDER BY STATUS
"""
df1 = session.sql(query1).to_pandas()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Orders by Status")
    if df1.empty:
        st.info("No data for pie chart")
    else:
        fig = px.pie(
            df1,
            names="STATUS",
            values="TOTAL_AMOUNT",
            hole=0.35
        )
        st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Orders Trend")
    if df.empty:
        st.warning("No data found for the selected filter.")
    else:
        df = df.sort_values("ORDER_DATE").set_index("ORDER_DATE")
        st.area_chart(df[["TOTAL_AMOUNT", "PROFIT"]])