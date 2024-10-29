import streamlit as st
from BackEnd import runreport
from datetime import datetime

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

# Sidebar calendar input
selected_date = st.sidebar.date_input("Pick a date", datetime.now())


if st.sidebar.button("Run Report"):
    st.sidebar.write("running report..")
    runreport.main(selected_date)
    st.sidebar.write(f"Report generated for:  {selected_date}")

# --Run navigation
pg.run()
