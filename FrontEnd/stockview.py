import streamlit as st
import base64

from altair.utils import display
from fontTools.cffLib import width

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

# Load your image
image_path = "F:\Python_projects\StreamlitStockView\FrontEnd\logo_1.jpg"
with open(image_path, "rb") as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

# Embed the image in HTML
st.sidebar.markdown(
    f"""
    <style>

    </style>
    <div class="logo-container">
        <img src="data:image/png;base64,{base64_image}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# --Navigation setup
pg = st.navigation(pages=[dashboard_page, cherries_page, gems_page, sectors_page])

# --Shared on all pages

if st.sidebar.button("Run Report"):
    st.write("running report..")

# --Run navigation
pg.run()
