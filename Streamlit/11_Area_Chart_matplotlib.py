import streamlit as st
from snowflake.snowpark.context import get_active_session
import matplotlib.pyplot as plt

plt.switch_backend('agg')  # non-interactive backend
st.title("Orders Distribution by Status")

session = get_active_session()

df = session.sql("""
    SELECT  STATUS,
        COUNT(DISTINCT ORDER_ID) AS TOTAL_ORDERS  FROM ORDERS  GROUP BY STATUS
""").to_pandas()

fig, ax = plt.subplots(figsize=(3, 3))
ax.pie(
    df["TOTAL_ORDERS"],
    labels=df["STATUS"],
    autopct="%1.1f%%",
    startangle=90
)
ax.set_title("Orders by Status")
st.pyplot(fig)
