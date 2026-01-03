import streamlit as st
from snowflake.snowpark.context import get_active_session


session = get_active_session()

st.title("Cortex Chat")


if "result" not in st.session_state:
    st.session_state.result = ""

prompt = st.text_input("Ask something")

if prompt:
    sql = "SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', ?)"
    
    with st.spinner("Thinking..."):
      
        response = session.sql(sql, params=[prompt]).collect()
        st.session_state.result = response[0][0]

if st.session_state.result:
    st.write(st.session_state.result)