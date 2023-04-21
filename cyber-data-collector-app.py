# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import plotly.graph_objs as go
from streamlit_option_menu import option_menu
import base64 as b64

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
        menu_title = "MENU", # Title of the menu
        options = ["Home","Data", "About", "Contact"], # List of options in the menu
        icons = ["house", "bi-clipboard-data", "info-square", "envelope"], # Use any of the Bootstrap Icons
        menu_icon = "cast",
        default_index = 0, # Index of the default option ("Home" in this case)
    )
    
# Display the selected page    
if selected_page == "Home":
    st.title("Welcome to the Cyber Data Collector")
    st.subheader("*Your cyber statistics hub*")
    st.warning("The app is still in development and more features will be added in the future :wrench: \n\n Please check back later for updates :new: \n\n Thank you for your patience :pray: ")
    
if selected_page == "Data":
    
    # st.warning("Page under construction :construction:")
    
    # Define the URL to scrape
    url = "https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/"

    # Send a request to the URL and get the response
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = bs4(response.content, "html.parser")

    # Find the data table on the page
    data_table = soup.find("table")

    # Check if the data table exists
    if data_table is not None:
        # Find all the rows in the table
        rows = data_table.find_all("tr")

        # Create empty lists to store data
        methods_list = []
        percentage_list = []

        # Loop through the rows and extract the data
        for row in rows:
            # Get the cells in the row
            cells = row.find_all("td")

            # Check if the row contains data
            if len(cells) > 0:
                # Get the method name
                methods = cells[0].text.strip()

                # Get the percentage
                percentage = cells[1].text.strip()

                # Add the data to the lists
                methods_list.append(methods)
                percentage_list.append(percentage)

        # Visualize the data using Streamlit
        st.title("Global Hacking Methods in 2019")

        st.markdown("""
        This chart shows the percentage of the leading global hacking methods in 2019.

        Source: [Statista.com](https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/)
        """)

        # Create a horizontal bar chart of the data
        chart_data = {"Methods": methods_list, "Percentage": percentage_list}
        chart_df = pd.DataFrame(chart_data)

        fig = go.Figure(go.Bar(
            x=chart_df['Percentage'],
            y=chart_df['Methods'],
            orientation='h',
            text=chart_df['Percentage'],
            textposition='auto',
            hovertemplate='%{x}%<extra></extra>',
            marker=dict(
                color=['#FCCA3A'] * len(chart_df),
                coloraxis=None,
            ),
        ))

        fig.update_layout(
            xaxis=dict(showgrid = True, gridwidth = 1, gridcolor = '#E5E5E5'),
            yaxis=dict(showgrid = False),
            
            xaxis_title="Percentage",
            yaxis_title="Methods",
            font=dict(size=16),
            margin=dict(l=0, r=0, t=60, b=0),
        )

        st.plotly_chart(fig)

        csvColumn, jsonColumn, htmlColumn = st.columns(3, gap="small")

        with csvColumn:
            
            # Add a download button for the data as CSV
            cvs = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_csv(index=False)
            bs64_cvs = b64.b64encode(cvs.encode()).decode()
            st.download_button(
                label="Download as CSV",
                data=bytes(cvs, encoding='utf8'),
                file_name="hacking-methods.csv",
                mime="text/csv",
            )
        with jsonColumn:
            
            # Add a download button for the data as JSON
            json = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_json(orient='records')
            bs64_json = b64.b64encode(json.encode()).decode()
            st.download_button(
                label="Download as JSON",
                data=bytes(json, encoding='utf8'),
                file_name="hacking-methods.json",
                mime="text/json",
            )
        with htmlColumn:
            
            # Add a download button for the data as HTML
            html = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_html(index=False)
            bs64_html = b64.b64encode(html.encode()).decode()
            st.download_button(
                label="Download as HTML",
                data=bytes(html, encoding='utf8'),
                file_name="hacking-methods.html",
                mime="text/html",
            ) 
    else:
        st.write("Data table not found on page.")
        
    st.divider()


if selected_page == "About":
    st.title("About")
    st.write("This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future.")

if selected_page == "Contact":
    st.title("Contact")
    st.write("If you have any questions or suggestions, please contact me by [email](mailto:C00263263@itcarlow.ie).")
    