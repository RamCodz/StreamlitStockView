import streamlit as st
from datetime import datetime, timedelta
from BackEnd import runreport
from BackEnd.Utils import globals
from FrontEnd.Utils import get_report_list

# ---Page setup
dashboard_page = st.Page(
    page="FrontEnd/dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)
cherries_page = st.Page(
    page="FrontEnd/cherries.py",
    title="Early Cherries",
    icon=":material/account_circle:"
)
gems_page = st.Page(
    page="FrontEnd/gems.py",
    title="Fallen Gems",
    icon=":material/account_circle:"
)
sectors_page = st.Page(
    page="FrontEnd/sectors.py",
    title="Sector Stars",
    icon=":material/account_circle:"
)
watchlist_page = st.Page(
    page="FrontEnd/watchlist.py",
    title="Watchlist",
    icon=":material/account_circle:"
)
st.set_page_config(layout="wide")

# --Navigation setup
pg = st.navigation(pages=[dashboard_page, cherries_page, gems_page, sectors_page, watchlist_page])

# Get today's date and calculate the range for the last 30 days
today = datetime.today()
thirty_days_ago = today - timedelta(days=30)

# Generate valid dates (last 30 days excluding Sundays and Mondays)
valid_dates = [
    thirty_days_ago + timedelta(days=i)
    for i in range(31)
    if (thirty_days_ago + timedelta(days=i)).weekday() not in (0, 6)  # Exclude Sunday (6) and Monday (0)
]

# Convert valid dates to strings for display
valid_date_strings = [date.strftime('%Y-%m-%d') for date in valid_dates]

# Streamlit dropdown
st.sidebar.title("Date Picker")
selected_date = st.sidebar.selectbox(
    "Pick a valid date:",
    valid_date_strings,
    help="Only dates within the last 30 days (excluding Sundays and Mondays) are selectable."
)

# Format the selected date as a string in the desired format
formatted_date = selected_date.strftime("%Y-%m-%d")

# Update the global variable with the selected report name
globals.current_report_name = f"StockView_{formatted_date}.csv"

# --Run navigation
pg.run()
