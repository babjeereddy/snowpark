import streamlit as st
from snowflake.snowpark.context import get_active_session
import plotly.express as px

st.set_page_config(page_title="Orders by Status", layout="wide")
st.title("Orders Distribution by Status")

session = get_active_session()

df = session.sql("""
    SELECT
        STATUS,
        COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS    FROM ORDERS
    GROUP BY STATUS
""").to_pandas()

fig = px.pie(
    df,
    names="STATUS",
    values="TOTAL_ORDERS",
    title="Orders by Status",
    hole=0.35   
)

st.plotly_chart(fig)
