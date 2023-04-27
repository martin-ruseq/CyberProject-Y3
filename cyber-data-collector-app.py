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
    
    @st.cache_data
    def get_data(url):
        response = requests.get(url)
        soup = bs4(response.content, "html.parser")
        data_table = soup.find("table")
        
        # Convert the Tag object to a string
        data_table_str = str(data_table)
        
        return data_table_str

    url = "https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/"
    data_table_str = get_data(url)

    # Convert the string back to a Tag object if needed
    data_table = bs4(data_table_str, "html.parser")

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
        st.title("Global Hacking Methods")

        st.markdown("""
        This chart/table shows the percentage of the leading global hacking methods.

        Source: [statista.com](https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/)
        """)
        
        # Create a dropdown menu for year selection
        data_year = st.selectbox("Select Year:", ["2019", "2018", "2017", "2016", "2015"])
        
        # Create dropdown menu for chart type
        view_type = st.selectbox("Select View Type:", ["Chart", "Table"])

        # Create a horizontal bar chart of the data
        chart_data = {"Methods": methods_list, "Percentage": percentage_list}
        chart_df = pd.DataFrame(chart_data)

        if data_year == "2019" and view_type == "Chart":
            # Create a horizontal bar chart of the data
            hack_methods_2019 = go.Figure(go.Bar(
                x=chart_df['Percentage'],
                y=chart_df['Methods'],
                orientation='h',
                text=chart_df['Percentage'],
                textposition='auto',
                hovertemplate='Method: %{y}<br>Percentage: %{x}<extra></extra>',
                marker=dict(
                    color=['#FCCA3A'] * len(chart_df),
                    coloraxis=None,
                ),
            ))

            hack_methods_2019.update_layout(
                xaxis=dict(showgrid = True, gridwidth = 1, gridcolor = '#E5E5E5'),
                yaxis=dict(showgrid = False),
                xaxis_title="Percentage",
                yaxis_title="Methods",
                font=dict(size=16),
                margin=dict(l=0, r=0, t=60, b=0),
            )
            
            st.plotly_chart(hack_methods_2019)
            
            def download_buttons_4_hack_methods_chart(methods_list, percentage_list):
                csv_column, json_column, html_column = st.columns(3, gap="small")
                
                # Generate CSV download button
                with csv_column:
                    csv = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_csv(index=False)
                    bs64_csv = b64.b64encode(csv.encode()).decode()
                    csv_button = st.download_button(
                        label="Download as CSV",
                        data=bytes(csv, encoding='utf8'),
                        file_name="hacking-methods.csv",
                        mime="text/csv",
                    )
                
                # Generate JSON download button
                with json_column:
                    json = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_json(orient='records')
                    bs64_json = b64.b64encode(json.encode()).decode()
                    json_button = st.download_button(
                        label="Download as JSON",
                        data=bytes(json, encoding='utf8'),
                        file_name="hacking-methods.json",
                        mime="text/json",
                    )
                
                # Generate HTML download button
                with html_column:
                    html = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_html(index=False)
                    bs64_html = b64.b64encode(html.encode()).decode()
                    html_button = st.download_button(
                        label="Download as HTML",
                        data=bytes(html, encoding='utf8'),
                        file_name="hacking-methods.html",
                        mime="text/html",
                    )
    
                # Return the base64-encoded CSV, JSON, and HTML strings
                return bs64_csv, bs64_json, bs64_html
            st.markdown("*Download the data:*\n\n")
            csv_data_, json_data, html_data = download_buttons_4_hack_methods_chart(methods_list, percentage_list)
            
        elif not data_year == "2019" and view_type == "Chart":
            st.warning("No data available for the selected year :warning:")
            
        if data_year == "2019" and view_type == "Table":
            st.table(chart_df)
            st.info("To download the data, please select the chart view.")
        elif not data_year == "2019" and view_type == "Table":
            st.warning("No data available for the selected year :warning:")
    
    # Custom devider            
    st.markdown(
        '<hr style="border-top: 4px solid #0062AF; border-radius: 5px">',
        unsafe_allow_html=True,)

    st.title("Legal Cases under Computer Misuse Act 1990")

    st.markdown("""
    This table shows the number of legal cases under the Computer Misuse Act 1990 in different years.

    Source: [web.archive.org](https://web.archive.org/web/20210321200020/https://www.computerevidence.co.uk/Cases/CMA.htm)
    """)
    
    @st.cache_data
    # Fuction to scrapes data from website and creates a table with Coputer Misuse Act cases
    def case_table(url, selected_year):
        response = requests.get(url)
        soup = bs4(response.content, 'html.parser')
        table = soup.find('table', attrs={'dir': 'LTR'})
        if table:
            rows = table.find_all('tr')
            if rows:
                cases_list = []
                year_list = []
                case_description_list = []
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        cases = cells[0].text.strip()
                        year = cells[1].text.strip()
                        case_description = cells[3].text.strip()
                        if str(selected_year) in year:
                            cases_list.append(cases)
                            year_list.append(year)
                            case_description_list.append(case_description)
                cases_df = pd.DataFrame({'Case': cases_list, 'Year': year_list, 'Description': case_description_list})
                cases_df.index = cases_df.index + 1
                
                return cases_df

    url = "https://web.archive.org/web/20210321200020/https://www.computerevidence.co.uk/Cases/CMA.htm"
    cases_year = st.selectbox("Select Year:", ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"])
    selected_year = int(cases_year)

    cma_cases_table = case_table(url, selected_year)

    st.table(cma_cases_table)
    st.info("This data table can not be downloaded")
    st.markdown(
    '<hr style="border-top: 4px solid #0062AF; border-radius: 5px">',
    unsafe_allow_html=True,)
    
if selected_page == "About":
    st.title("About")
    st.write("This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future.")

if selected_page == "Contact":
    st.title("Contact")
    st.write("If you have any questions or suggestions, please contact me by [email](mailto:C00263263@itcarlow.ie).")
    