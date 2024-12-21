import streamlit as st
from datetime import datetime, timedelta
from BackEnd import runreport
from BackEnd.Utils import globals
from FrontEnd.Utils import get_report_list

# Page configuration
st.set_page_config(page_title="Stock Dashboard", layout="wide")

# Sidebar for navigation
pages = {
    "Dashboard": "dashboard",
    "Early Cherries": "cherries",
    "Fallen Gems": "gems",
    "Sector Stars": "sectors",
    "Watchlist": "watchlist",
}

selected_page = st.sidebar.radio("Navigation", list(pages.keys()))

# Sidebar for date selection (last 30 days)
today = datetime.today()
min_date = today - timedelta(days=30)
max_date = today

selected_date = st.sidebar.date_input(
    "Select a date",
    min_value=min_date,
    max_value=max_date,
    value=today,
    help="Select a date within the last 30 days"
)

# Pass the selected date to the global variable or session state
globals.current_report_date = selected_date

# Render selected page
if selected_page == "Dashboard":
    # Include dashboard logic here
elif selected_page == "Early Cherries":
    # Include Early Cherries logic here
elif selected_page == "Fallen Gems":
    # Include Fallen Gems logic here
elif selected_page == "Sector Stars":
    # Include Sector Stars logic here
elif selected_page == "Watchlist":
    # Include Watchlist logic here
