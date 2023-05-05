# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import plotly_express as px
import plotly.graph_objs as pgo
from streamlit_option_menu import option_menu
import base64 as b64

# Set the page title and icon
st.set_page_config(page_title="CyberHub App", page_icon="⛏️", 
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
    st.sidebar.image("resources/logo.png", use_column_width=True)
    selected_page = option_menu(
        menu_title = "", # Title of the menu
        options = ["Home","Cyber Statistics","CVE Data", "About", "Contact"], # List of options in the menu
        icons = ["house", "bi-bar-chart-line", "bi-shield-exclamation", "info-square", "envelope"], 
        menu_icon = "cast",
        default_index = 0, # Index of the default option ("Home" in this case)
    )
    
# Display the selected page    
if selected_page == "Home":
    st.title("Welcome to the CyberHub :wave:")
    st.subheader("*Your cyber statistics in one place* :bar_chart:")
    st.warning("The app is still in development and more features will be added in the future :wrench: \n\n Please check back later for updates :new: \n\n Thank you for your patience :pray: ")
    
if selected_page == "Cyber Statistics":
    
    @st.cache_data  # Caches the function output so that it doesn't have to be rerun everytime the page is refreshed
    # Fuction to scrape the data from the website
    def get_data(url):
        response = requests.get(url)
        soup = bs4(response.content, "html.parser")
        data_table = soup.find("table")
        
        # Convert the Tag object to a string
        data_table_str = str(data_table)
        
        return data_table_str

    url = "https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/"
    data_table_str = get_data(url) 

    # Convert the string to a Tag object using BeautifulSoup
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
                # Get the hacking methods
                methods = cells[0].text.strip()

                # Get the percentage of the hacking methods
                percentage = cells[1].text.strip()

                # Append the data to the lists
                methods_list.append(methods)
                percentage_list.append(percentage)

        # Hacking Methods Chart and Table
        st.title("Global Hacking Methods")
        st.markdown("""
            This chart/table shows the percentage of the leading global hacking methods.

            Source: [statista.com](https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/)
            """)
        
        # Create a dropdown menu for year selection
        data_year = st.selectbox("Select Year:", ["2019", "2018", "2017", "2016", "2015"])
        
        # Create dropdown menu for chart type
        view_type = st.selectbox("Select View Type:", ["Chart", "Table"])

        # Create a dataframe to store the data for the selected year
        chart_data = {"Methods": methods_list, "Percentage": percentage_list}
        chart_df = pd.DataFrame(chart_data)

        if data_year == "2019" and view_type == "Chart":
            # Createing the horizontal bar chart using Plotly
            hack_methods_2019 = pgo.Figure(pgo.Bar(
                x = chart_df['Percentage'],
                y = chart_df['Methods'],
                orientation = 'h',
                text = chart_df['Percentage'],
                textposition = 'auto',
                hovertemplate = 'Method: %{y}<br>Percentage: %{x}<extra></extra>',
                marker = dict(
                    color=['#0062AF'] * len(chart_df),
                    coloraxis=None,
                ),
            )) 
            # Update the layout of the chart to make it look better
            hack_methods_2019.update_layout(
                xaxis = dict(showgrid = True, gridwidth = 1, gridcolor = '#E5E5E5'),
                yaxis = dict(showgrid = False),
                xaxis_title = "Percentage",
                yaxis_title = "Methods",
                font = dict(size = 16),
                margin = dict(l = 0, r = 0, t = 60, b = 0),
            )
            # Display the chart using Plotly
            st.plotly_chart(hack_methods_2019)
            
            # Fuction to create a download buttons for the hacking methods chart
            def download_btns_hack_methods(methods_list, percentage_list):
                csv_column, json_column, html_column = st.columns(3, gap = "small")
                
                # Generate CSV download button
                with csv_column:
                    csv = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_csv(index=False)
                    csv_btn = st.download_button(
                        label="Download as CSV",
                        help="Click here to download the data as a CSV file",
                        data=bytes(csv, encoding='utf8'),
                        file_name="hacking-methods-cyberhub.csv",
                        mime="text/csv",
                    )
                
                # Generate JSON download button
                with json_column:
                    json = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_json(orient='records')
                    json_btn = st.download_button(
                        label="Download as JSON",
                        help="Click here to download the data as a JSON file",
                        data=bytes(json, encoding='utf8'),
                        file_name="hacking-methods-cyberhub.json",
                        mime="text/json",
                    )
                
                # Generate HTML download button
                with html_column:
                    html = pd.DataFrame({'Method': methods_list, 'Percentage': percentage_list}).to_html(index=False)
                    html_btn = st.download_button(
                        label="Download as HTML",
                        help="Click here to download the data as a HTML file",
                        data=bytes(html, encoding='utf8'),
                        file_name="hacking-methods-cyberhub.html",
                        mime="text/html",
                    )
    
                # Return the download buttons for the hacking methods chart
                return csv_btn, json_btn, html_btn
            
            # Display the download buttons for the hacking methods chart
            st.markdown("*Download the data:*\n\n")
            csv_hack, json_hack, html_hack = download_btns_hack_methods(methods_list, percentage_list)
            
        elif not data_year == "2019" and view_type == "Chart":
            st.warning("No data available for the selected year :warning:")
            
        if data_year == "2019" and view_type == "Table":
            st.table(chart_df)
            st.info("To download the data, please select the chart view.")
        elif not data_year == "2019" and view_type == "Table":
            st.warning("No data available for the selected year :warning:")
    
    # Custom devider            
    st.markdown(
        '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html=True,)

    # Legal Cases under Computer Misuse Act 1990 table
    st.title("Legal Cases under Computer Misuse Act 1990 (UK) as of 2021")
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
        '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html=True,)
    
    # Monetary Damages caused by Cybercrime
    st.title("Monetary Damages caused by Cybercrimes reported to IC3 form 2001 to 2022")
    st.subheader("*(in million U.S. dollars)*")
    st.markdown("""
        This chart/table shows the monetary damages caused by cybercrimes reported to IC3 from 2001 to 2022.
        
        Source: [statista.com](https://www.statista.com/statistics/267132/total-damage-caused-by-by-cyber-crime-in-the-us/) and  [ic3.gov](https://www.ic3.gov/)
        """)
    
    url = "https://www.statista.com/statistics/267132/total-damage-caused-by-by-cyber-crime-in-the-us/"
    damage_table_str = get_data(url)
    damage_table = bs4(damage_table_str, 'html.parser')
    
    def make_damages_df(damage_table):
        damages_list = []
        years_list = []
        for row in damage_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 1:
                damages = cells[1].text.strip()
                years = cells[0].text.strip()
                damages_list.append(damages)
                years_list.append(years)
        damages_df = pd.DataFrame({'Years': years_list, 'Damages': damages_list})
        
        return damages_df, damages_list, years_list
    
    damages_df = make_damages_df(damage_table)
    damages_list = damages_df[1]
    yeas_list = damages_df[2]
    
    @st.cache_data
    def create_damages_graph(damage_df):
        graph = px.line(damage_df, x="Years", y="Damages",markers=True)
        graph.update_layout(
            xaxis_title="Years",
            xaxis=dict(
                tickmode='linear',
                tickangle=45,
                tick0=2001,
                dtick=1,
                
            ),
            yaxis_title="Damages (in million U.S. dollars)",
            font=dict(size = 16),
            
        )
        return graph
    
    def download_btns_damages_data(damages_list, years_list):
        csv_column, json_column, html_column = st.columns(3, gap = "small")

        with csv_column:
            csv = pd.DataFrame({'Years': years_list, 'Damages': damages_list}).to_csv(index=False)
            csv_btn = st.download_button(
                label="Download as CSV",
                help="Click here to download the data as CSV file",
                data=bytes(csv, encoding='utf-8'),
                file_name="cybercrime-costs-ic3-cyberhub.csv",
                mime="text/csv"
            )
        with json_column:
            json = pd.DataFrame({'Years': years_list, 'Damages': damages_list}).to_json(orient='records')
            json_btn = st.download_button(
                label="Download as JSON",
                help="Click here to download the data as JSON file",
                data=bytes(json, encoding='utf-8'),
                file_name="cybercrime-costs-ic3-cyberhub.json",
                mime="application/json"
            )
        with html_column:
            html = pd.DataFrame({'Years': years_list, 'Damages': damages_list}).to_html(index=False)
            html_btn = st.download_button(
                label="Download as HTML",
                help="Click here to download the data as HTML file",
                data=bytes(html, encoding='utf-8'),
                file_name="cybercrime-costs-ic3-cyberhub.html",
                mime="text/html"
            )
        return csv_btn, json_btn, html_btn
    
    dmg_view = st.selectbox("Select View Type:", ["Line", "Table"])
    
    if dmg_view == "Line":
        st.plotly_chart(create_damages_graph(damages_df[0]))
        st.markdown("*Download the data:*\n\n")
        csv_dmg, json_dmg, html_dmg = download_btns_damages_data(damages_list, yeas_list)
        st.markdown(
            '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
            unsafe_allow_html=True,)
    elif dmg_view == "Table":
        st.dataframe(damages_df[0], height=500, width=1000)
        st.info("To download the data, please select the Line view type")
        st.markdown(
            '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
            unsafe_allow_html=True,)
        
if selected_page == "CVE Data":
    st.warning("This page is still in development and will be available soon... :warning:")
              
if selected_page == "About":
    st.title("About")
    st.write("This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future.")

if selected_page == "Contact":
    st.title("Contact")
    st.write("If you have any questions or suggestions, please contact me by [email](mailto:C00263263@itcarlow.ie).") 