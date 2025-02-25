"""View Reading Stats."""

import streamlit as st

st.set_page_config(
    page_title="My Reading Stats",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("My Reading Stats 📊")

# Retrieve the user ID from the session state
user_id = st.session_state.get("email", None)

if user_id is None:
    st.error("You must be logged in to add a book.")
    st.stop()  # Stop the script here if the user is not logged in
