# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st
from streamlit_option_menu import option_menu


# ----------------------------------------------- START SETUP ------------------------------------------------- #
# Set the page title and icon
st.set_page_config(
    page_title = "CyberHub App",
    page_icon = "⛏️",
    layout = "wide",
    initial_sidebar_state = "expanded",
)

# Hide the menu and footer of Streamlit Cloud deployments
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            .css-17es36v {visibility: hidden;}
            .stActionButton {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html = True) # unsafe_allow_html disable the html tags escaping from the body

# Create a sidebar menu
with st.sidebar:
    st.sidebar.image("resources/logo.png", use_column_width = True)

    selected_page = option_menu(
        menu_title = "",  # Title of the menu
        options = [
            "Latest Cyber News",
            "Cyber Statistics",
            "CVE & Related Data",
            "About",
            "Contact",
        ],  # List of options in the menu
        icons=[
            "bi-newspaper",
            "bi-bar-chart-line",
            "bi-shield-exclamation",
            "info-square",
            "envelope",
        ],  # Icons for each option, displayed before the text
        default_index = 0,  # Index of the default option ("Home" in this case)
    )

    # Add a custom footer to the sidebar
    custom_footer = """
    <footer style = "font-family: 'Segoe UI'; font-size: 14px; color: #6C757D; text-align: center; padding: 125px 0px 10px 0px;"><img src="https://cdn-icons-png.flaticon.com/512/4486/4486819.png" width="16" height="16">&nbsp;&nbsp;with ❤️ by 
    <a href = "https://github.com/martin-ruseq" target = "_blank">Marcin Rusiecki</a>"""
    st.markdown(custom_footer, unsafe_allow_html = True)
# --------------------------------------------------- END SETUP ------------------------------------------------ #
   
   
# ----------------------------------------------- START PAGES ------------------------------------------------- #   
if selected_page == "Latest Cyber News":
    exec(open("news.py").read())

elif selected_page == "Cyber Statistics":
    exec(open("cyber-stats.py").read())

elif selected_page == "CVE & Related Data":
    exec(open("cve-data.py").read())

elif selected_page == "About":
    exec(open("about.py").read())

else:
    exec(open("contact.py").read())
# --------------------------------------------------- END PAGES ------------------------------------------------ #
