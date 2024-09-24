import streamlit as st
from BackEnd import runreport

# ---Page setup
st.set_page_config(layout="wide")

# --Navigation setup
pages = {
    "Dashboard": "FrontEnd/dashboard.py",
    "Early Cherries": "FrontEnd/cherries.py",
    "Fallen Gems": "FrontEnd/gems.py",
    "Sector Stars": "FrontEnd/sectors.py"
}

# --Sidebar for navigation
selection = st.sidebar.selectbox("Select a page", list(pages.keys()))

# --Shared on all pages
if st.sidebar.button("Run Report"):
    st.sidebar.write("running report..")
    runreport.main()
    st.sidebar.write("Report generated")

# --Run selected page
page = pages[selection]
exec(open(page).read())
