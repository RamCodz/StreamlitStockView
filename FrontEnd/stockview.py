from BackEnd import runreport

# ---Page setup
dashboard_page = st.Page(
    page="dashboard.py",
    title="Dashboard",
    icon=":material/dashboard:",
    default=True
)
cherries_page = st.Page(
    page="cherries.py",
    title="Early Cherries",
    icon=":material/account_circle:"
)
gems_page = st.Page(
    page="gems.py",
    title="Fallen Gems",
    icon=":material/account_circle:"
)
sectors_page = st.Page(
    page="sectors.py",
    title="Sector Stars",
    icon=":material/account_circle:"
)
st.set_page_config(layout="wide")

# --Navigation setup
pg = st.navigation(pages=[dashboard_page, cherries_page, gems_page, sectors_page])

# --Shared on all pages

if st.sidebar.button("Run Report"):
    st.write("running report..")
    runreport.main()
    st.write("Report generated")
# --Run navigation
pg.run()
