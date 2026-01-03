import streamlit as st

st.set_page_config(page_title="Text Input Demo")

st.title("Name Input Example")

# Text input
name = st.text_input(
    "Enter your name",
    placeholder="Type your name here"
)

# Print only the name
if name:
    st.success(f"Hello {name} 👋")
