"""My Information."""

import streamlit as st
from supabase_utils.auth import SupabaseAuth
from supabase import create_client

st.set_page_config(
    page_title="My Information",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize Supabase client
supabase_url = st.secrets.supabase.PROJECT_URL
supabase_key = st.secrets.supabase.ANON_PUBLIC

supabase = create_client(supabase_url, supabase_key)

# Initialize the SupabaseAuth class
test_auth = SupabaseAuth(supabase)

# Retrieve the user ID from the session state
user_id = st.session_state.get("email", None)

if user_id is None:
    st.error("You must be logged in to add a book.")
    st.stop()  # Stop the script here if the user is not logged in

st.title("My Information 👤")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("User Information")
    # user_info = test_auth.get_user_info()
    user_info = test_auth.get_user_profile()
    st.write(user_info)
    # st.text_input(label="Email", value=user_info.get("email"), key="email", disabled=True)
