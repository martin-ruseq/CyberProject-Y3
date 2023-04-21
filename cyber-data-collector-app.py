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
        menu_title = "App Menu",
        options = ["Home","Data", "About", "Contact"], # List of options in the menu
        icons = ["house", "bi-clipboard-data", "info-square", "envelope"], # Use any of the Bootstrap Icons
        menu_icon = "cast", 
        default_index = 0, # Index of the default option ("Home" in this case)
        
    )
    
# Display the selected page    
if selected_page == "Home":
    st.title("Welcome to the Cyber Data Collector App!")
    st.header("*Your cyber statistics hub*")
    st.warning("The app is still in development and more features will be added in the future :wrench: \n\n Please check back later for updates :new: \n\n Thank you for your patience :pray: ")
    
if selected_page == "Data":

   """ # Define the URL to scrape
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
        st.header("Leading global hacking methods in 2019")
        st.write("Source: [*Statista.com*](https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/)", unsafe_allow_html=True)

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
                color=['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1', '#FFC7E5'],
                coloraxis=None,
            ),
        ))

        fig.update_layout(
            title={
                'text': 'Global Hacking Methods in 2019',
                'font': {'size': 24},
                'x': 0.5,
                'xanchor': 'center',
            },
            xaxis={
                'title': 'Percentage',
                'range': [0, 100],
                'dtick': 5,
                'tickmode': 'linear',
                'tick0': 5,
                'tickwidth': 1,
                'ticklen': 5,
                'tickfont': {'size': 11},
                'showgrid': True,
                'gridcolor': 'lightgray',
                'griddash': 'dot',
                'linecolor': 'gray',
                'linewidth': 1,
                'type': 'linear'
                
            },
            yaxis={
                'title': 'Methods',
                'tickfont': {'size': 14},
            },
            hoverlabel={'font': {'size': 16}},
        )

        st.plotly_chart(fig)

    else:
        print("Data table not found on page.")"""

if selected_page == "About":
    st.write(""" # About""")
    st.write("This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future.")

if selected_page == "Contact":
    st.write(""" # Contact""")
    st.write("If you have any questions or suggestions, please contact me by [email](mailto:C00263263@itcarlow.ie).")
    

