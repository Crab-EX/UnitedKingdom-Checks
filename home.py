import streamlit as st

st.set_page_config(
    page_title="UK Checks",
    page_icon="🔍",
    initial_sidebar_state="expanded",
)

def main_page():
    st.title("UK Checks")

main_page = st.Page(main_page, title="Home page", icon="🏠") 
officer_page = st.Page("pages/1_officer.py", title="Officers", icon="📊")

pages = {
    "UK Checks": [
        main_page,
        officer_page,
    ]
}

pg = st.navigation(pages)
pg.run()