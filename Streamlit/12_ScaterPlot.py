import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Orders Scatter Plot", layout="wide")
st.title("Orders Scatter Plot (Amount vs Discount)")

# Get active Snowflake session
session = get_active_session()

# Query data
df = session.sql("""
    SELECT
        sum(AMOUNT) AMOUNT,
        SUM(DISCOUNT) DISCOUNT,
        status
               
    FROM ORDERS1
    group by status 
 
    
""").to_pandas()


# Scatter plot
st.subheader("Scatter Plot: Amount vs Discount")

st.scatter_chart(
    df,
    x="AMOUNT",
    y="DISCOUNT",
    color="STATUS",
    size="DISCOUNT"
)

