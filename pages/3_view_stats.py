import streamlit as st
import pandas as pd
import time
from datetime import datetime
from utils.database_funcs import BookDatabase

st.set_page_config(
    page_title="My Reading Stats",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("My Reading Stats 📊")