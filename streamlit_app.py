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

# Date selection logic
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

# Format the selected date as a string in the desired format
formatted_date = selected_date.strftime("%Y-%m-%d")

# Update the global variable with the selected report name
globals.current_report_name = f"StockView_{formatted_date}.csv"

# Check if the selected date is Sunday (6) or Monday (0)
if selected_date.weekday() in (0, 6):  # 0 is Monday, 6 is Sunday
    st.sidebar.error("Invalid date: Sundays and Mondays are not allowed. Please select another date.")
else:
    # --Run navigation
    pg.run()
