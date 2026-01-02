from snowflake.snowpark import Session
import streamlit as st
session = Session.builder.config("connection_name", "default").create()

st.title("Orders Dashboard")
df = session.table("ORDERS").to_pandas()
total_orders = df["ORDER_ID"].nunique()
total_amount = df["AMOUNT"].sum()
col1, col2 = st.columns(2)
col1.metric("Total Orders", total_orders)
col2.metric("Total Amount", f"{total_amount:,.0f}")
st.subheader("Order Details")
st.dataframe(df)
