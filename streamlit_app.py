import streamlit as st
from BackEnd import runreport

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


st.set_page_config(layout="wide")

# --Add logo to the sidebar
st.image("FrontEnd/logo_2.jpg")

# --Navigation setup
pg = st.navigation(pages=[dashboard_page, cherries_page, gems_page, sectors_page])

# --Shared on all pages

if st.sidebar.button("Run Report"):
    st.sidebar.write("running report..")
    runreport.main()
    st.sidebar.write("Report generated")
# --Run navigation
pg.run()
