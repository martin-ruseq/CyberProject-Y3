# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import plotly.graph_objs as go
from streamlit_option_menu import option_menu

# Set the page title and icon
st.set_page_config(page_title="Cyber Data Collector App", page_icon="📊", 
                   layout="centered", 
                   initial_sidebar_state="expanded",
                   )

# Hide the menu and footer of Streamlit Cloud deployments
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """ 
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Create a sidebar menu
with st.sidebar:
    selected_page = option_menu(
        menu_title = "MAIN MENU", # Title of the menu
        options = ["Home","Data", "About", "Contact"], # List of options in the menu
        icons = ["house", "bi-clipboard-data", "info-square", "envelope"], # Use any of the Bootstrap Icons
        menu_icon = "cast", 
        default_index = 0, # Index of the default option ("Home" in this case)
        
    )
    
# Display the selected page    
if selected_page == "Home":
    st.title("Welcome to the Cyber Data Collector")
    st.header("*Your cyber statistics hub*")
    st.warning("The app is still in development and more features will be added in the future :wrench: \n\n Please check back later for updates :new: \n\n Thank you for your patience :pray: ")
    
if selected_page == "Data":
    st.title("Cyber Data")
    st.warning("Page under construction :construction:")

if selected_page == "About":
    st.title("About")
    st.write("This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future.")

if selected_page == "Contact":
    st.title("Contact")
    st.write("If you have any questions or suggestions, please contact me by [email](mailto:C00263263@itcarlow.ie).")
    

