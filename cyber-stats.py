import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import plotly_express as px
import plotly.graph_objs as pgo

st.markdown(
    "<h1 style = 'text-align: center; color: #0062AF;'>Cyber Statistics</h1>",
    unsafe_allow_html = True,)

st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html = True,)

@st.cache_data  # Caches the function output so that it doesn't have to be rerun everytime the page is refreshed
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
            methods = cells[0].text.strip()     # Get the hacking methods
            percentage = cells[1].text.strip()  # Get the percentage of the hacking methods
            methods_list.append(methods)        # Append the methods to the list
            percentage_list.append(percentage)


    # ------------------------------------- START OF GLOBAL HACKING METHODS -------------------------------- #
    st.title("Global Hacking Methods")
    st.markdown(
        """
        This chart/table shows the percentage of the leading global hacking methods.

        Source: [statista.com](https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/)
        """
    )

    # Create a dropdown menu for year selection
    data_year = st.selectbox(
        "Select Year:", ["2019", "2018", "2017", "2016", "2015"]
    )

    # Create dropdown menu for chart type
    view_type = st.selectbox("Select View Type:", ["Horizontal Bar Chart", "Table"])

    # Create a dataframe to store the data for the selected year
    chart_data = {"Methods": methods_list, "Percentage": percentage_list}
    chart_df = pd.DataFrame(chart_data)

    # Createing the horizontal bar chart using Plotly
    if data_year == "2019" and view_type == "Horizontal Bar Chart":
        hack_methods_2019 = pgo.Figure(
            pgo.Bar(
                x = chart_df["Percentage"],     # Set the x-axis to the percentage
                y = chart_df["Methods"],        # Set the y-axis to the methods
                orientation = "h",              # Horizontal Bar Chart
                text = chart_df["Percentage"],  # Display the percentage on the chart
                textposition = "auto",
                hovertemplate = "Method: %{y}<br>Percentage: %{x}<extra></extra>",
                marker = dict(
                    color = ["#0062AF"] * len(chart_df)) # Set the color of the bars
            )
        )

        # Update the layout of the chart to make it look better
        hack_methods_2019.update_layout(
            xaxis = dict(showgrid = True, gridwidth = 1, gridcolor = "#E5E5E5"), # Set the x-axis grid color
            yaxis = dict(showgrid = False), # Hide the y-axis grid
            xaxis_title = "Percentage",
            yaxis_title = "Methods",
            font = dict(size = 16),
            width = 1000,
            margin = dict(l=0, r=0, t=60, b=0), # Set the margins of the chart to make it look better
        )

        st.plotly_chart(hack_methods_2019)  # Display the chart on the page using Streamlit and Plotly

        # Fuction to create a download buttons for the hacking methods chart
        def download_btns_hack_methods(methods_list, percentage_list):
            csv_column, json_column, html_column = st.columns(3, gap = "small")

            # Generate CSV download button
            with csv_column:
                csv = pd.DataFrame(
                    {"Method": methods_list,
                        "Percentage": percentage_list}
                    ).to_csv(index=False)  # Convert the dataframe to a CSV file

                csv_btn = st.download_button(
                    label = "Download as CSV",
                    help = "Click here to download the data as a CSV file", # Display a toolti when hovering
                    data = bytes(csv, encoding="utf8"),  # csv must be encoded to bytes for download btn to work
                    file_name = "hacking-methods-cyberhub.csv",
                    mime = "text/csv",  # Indicates the nature of file (type/subtype) so the system knows how to handles it
                )

            # Generate JSON download button
            with json_column:
                json = pd.DataFrame(
                    {"Method": methods_list,
                        "Percentage": percentage_list}).to_json(orient="records")

                json_btn = st.download_button(
                    label="Download as JSON",
                    help="Click here to download the data as a JSON file",
                    data=bytes(json, encoding="utf8"),
                    file_name="hacking-methods-cyberhub.json",
                    mime="text/json",  
                )

            # Generate HTML download button
            with html_column:
                html = pd.DataFrame(
                    {"Method": methods_list, "Percentage": percentage_list}
                ).to_html(
                    index=False
                )  # Convert the dataframe to a HTML file

                html_btn = st.download_button(
                    label = "Download as HTML",
                    help = "Click here to download the data as a HTML file",
                    data = bytes(html, encoding="utf8"),
                    file_name = "hacking-methods-cyberhub.html",
                    mime = "text/html",
                )

            return csv_btn, json_btn, html_btn

        # Display the download buttons for the hacking methods chart
        st.markdown("*Download the data:*\n\n")
        csv_hack, json_hack, html_hack = download_btns_hack_methods(
            methods_list, percentage_list
        )
    elif not data_year == "2019" and view_type == "Horizontal Bar Chart":
        st.warning("No data available for the selected year :warning:")
        
    if data_year == "2019" and view_type == "Table":
        st.table(chart_df)
        st.info("To download the data, please select the chart view.")  
    elif not data_year == "2019" and view_type == "Table":
        st.warning("No data available for the selected year :warning:")

# Custom devider
st.markdown(
    '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)
# -------------------------------------- END GLOBAL HACKING METHODS DATA ------------------------------------ #


# --------------------------- START OF LEGAL CASES UNDER COMPUTER MISUSE ACT 1990 --------------------------- #
st.title("Legal Cases under Computer Misuse Act 1990 (UK) as of 2021")
st.markdown(
    """
    This table shows the number of legal cases under the Computer Misuse Act 1990 in different years.

    Source: [web.archive.org](https://web.archive.org/web/20210321200020/https://www.computerevidence.co.uk/Cases/CMA.htm)
    """
)

@st.cache_data
def case_table(url, selected_year):
    response = requests.get(url)
    soup = bs4(response.content, "html.parser")
    table = soup.find("table", attrs =  {"dir": "LTR"})

    if table:
        rows = table.find_all("tr")
        if rows:
            cases_list = []
            year_list = []
            case_description_list = []
            for row in rows[1:]:
                cells = row.find_all("td")
                if len(cells) > 1:
                    cases = cells[0].text.strip()
                    year = cells[1].text.strip()
                    case_description = cells[3].text.strip()
                    if str(selected_year) in year:
                        cases_list.append(cases)
                        year_list.append(year)
                        case_description_list.append(case_description)

            cases_df = pd.DataFrame(
                {
                    "Case": cases_list,
                    "Year": year_list,
                    "Description": case_description_list,
                }
            )
            cases_df.index = cases_df.index + 1 # Start index from 1

            return cases_df

url = "https://web.archive.org/web/20210321200020/https://www.computerevidence.co.uk/Cases/CMA.htm"
cases_year = st.selectbox(
    "Select Year:", ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014"]
)
selected_year = int(cases_year)

cma_cases_table = case_table(url, selected_year)

st.table(cma_cases_table)
st.info("This data table can not be downloaded")
st.markdown(
    '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)
# ------------------------ END LEGAL CASES UNDER COMPUTER MISUSE ACT 1990 (UK) DATA ------------------------- #


# ----------------------------- START OF MONETARY DAMAGES CAUSED BY CYBERCRIMES ----------------------------- #
st.title("Monetary Damages caused by Cybercrimes reported to IC3 form 2001 to 2022")
st.subheader("*(in million U.S. dollars)*")
st.markdown(
    """
    This chart/table shows the monetary damages caused by cybercrimes reported to IC3 from 2001 to 2022.
    
    Source: [statista.com](https://www.statista.com/statistics/267132/total-damage-caused-by-by-cyber-crime-in-the-us/) and  [ic3.gov](https://www.ic3.gov/)
    """
)

url = "https://www.statista.com/statistics/267132/total-damage-caused-by-by-cyber-crime-in-the-us/"
damage_table_str = get_data(url)
damage_table = bs4(damage_table_str, "html.parser")

def make_damages_df(damage_table):
    damages_list = []
    years_list = []
    for row in damage_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 1:
            damages = cells[1].text.strip()
            years = cells[0].text.strip()
            damages_list.append(damages)
            years_list.append(years)
    damages_df = pd.DataFrame({"Years": years_list, "Damages": damages_list})

    return damages_df, damages_list, years_list

damages_df = make_damages_df(damage_table)
damages_list = damages_df[1]
yeas_list = damages_df[2]

@st.cache_data
def create_damages_graph(damage_df):
    graph = px.line(
        damage_df,
        x = "Years",
        y = "Damages",
        markers = True, # Displays dots on the line (markers)
        )
    
    graph.update_layout(
        xaxis_title = "Years",
        width = 1000,
        xaxis = dict(
            tickmode = "linear",    # Sets the x-axis to a linear scale
            tickangle = 45,         # Rotates the x-axis labels by 45 degrees
            tick0 = 2001,           # Sets the starting point of the x-axis to 2001
            dtick = 1,              # Sets the interval between ticks to 1
        ),
        yaxis_title = "Damages (in million U.S. dollars)",
        font = dict(size = 16),
    )

    return graph

def download_btns_damages_data(damages_list, years_list):
    csv_column, json_column, html_column = st.columns(3, gap = "small")

    with csv_column:
        csv = pd.DataFrame({
            "Years": years_list,
            "Damages": damages_list}).to_csv(
            index = False   # Removes the index column
        )

        csv_btn = st.download_button(
            label = "Download as CSV",
            help = "Click here to download the data as CSV file",
            data = bytes(csv, encoding = "utf-8"),
            file_name = "cybercrime-costs-ic3-cyberhub.csv",
            mime = "text/csv",
        )

    with json_column:
        json = pd.DataFrame({
            "Years": years_list,
            "Damages": damages_list
            }).to_json(orient = "records") # Sets the JSON file to be in a record format (one record per line)

        json_btn = st.download_button(
            label = "Download as JSON",
            help = "Click here to download the data as JSON file",
            data = bytes(json, encoding = "utf-8"),
            file_name = "cybercrime-costs-ic3-cyberhub.json",
            mime = "application/json", 
        )

    with html_column:
        html = pd.DataFrame({
            "Years": years_list,
            "Damages": damages_list
            }).to_html(index = False)

        html_btn = st.download_button(
            label = "Download as HTML",
            help = "Click here to download the data as HTML file",
            data = bytes(html, encoding = "utf-8"),
            file_name = "cybercrime-costs-ic3-cyberhub.html",
            mime = "text/html",
        )

    return csv_btn, json_btn, html_btn

dmg_view = st.selectbox("Select View Type:", ["Line", "Table"])

if dmg_view == "Line":
    st.plotly_chart(create_damages_graph(damages_df[0]))

    st.markdown("*Download the data:*\n\n")
    csv_dmg, json_dmg, html_dmg = download_btns_damages_data(
        damages_list, yeas_list
    )

    st.markdown(
        '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html=True,
    )

elif dmg_view == "Table":
    st.dataframe(damages_df[0], height = 500, width = 1000)

    st.info("To download the data, please select the Line view type")

    st.markdown(
        '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html = True,
    )
# --------------------- END MONETARY DAMAGES CAUSED BY CYBERCRIMES REPORTED TO IC3 DATA --------------------- #


# --------------------- START OF CYBERSECURITY MARKET SIZE WORLDWIDE 2019-2030 DATA ------------------------- #
st.title("Cybersecurity market size worldwide 2019-2030")
st.subheader("*(in billion U.S. dollars)*")
st.markdown(
    """
    The statistic shows the size of the cybersecurity market worldwide, from 2019 to 2030 acording to the data
    from [Next Move Strategy Consulting](https://www.nextmsc.com/). The global cybersecurity market is 
    projected to reach 657.02 billion U.S. dollars by 2030.
    
    Source: [statista.com](https://www.statista.com/statistics/1256346/worldwide-cyber-security-market-revenues/) and [nextmsc.com](https://www.nextmsc.com/])
    """
)

url = "https://www.statista.com/statistics/1256346/worldwide-cyber-security-market-revenues/"
cyber_market_table_str = get_data(url)
cyber_market_table = bs4(cyber_market_table_str, "html.parser")

def make_cyber_market_df(cyber_market_table):
    cyber_market_list = []
    years_list = []

    for row in cyber_market_table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) > 1:
            cyber_market = cells[1].text.strip()
            years = cells[0].text.strip()
            cyber_market_list.append(cyber_market)
            years_list.append(years)

    cyber_market_df = pd.DataFrame({
            "Years": years_list,
            "Cyber Market": cyber_market_list
            })

    return cyber_market_df, cyber_market_list, years_list

cyber_market_df = make_cyber_market_df(cyber_market_table)
cyber_market_list = cyber_market_df[1]
years_list = cyber_market_df[2]

@st.cache_data
def create_cyber_market_barchart(cyber_market_df):
    barchart = px.bar(
        cyber_market_df,
        x = "Years",
        y = "Cyber Market",
        orientation = "v",  # Sets the orientation of the bars to vertical
        color = "Cyber Market", # Sets the color of the bars to the "Cyber Market" column
        color_discrete_sequence = px.colors.cmocean.thermal_r,  # Sets the color scheme of the bars
        labels = {"Cyber Market": "Cyber Market (in billion U.S. dollars)"}, # Sets the label of the y-axis
    )

    barchart.update_layout(
        showlegend = False, # Hides the legend
        width = 1000,
    )

    return barchart

def download_btns_cyber_market_data(cyber_market_list, years_list):
    cvs_column, json_column, html_column = st.columns(3, gap = "small")

    with cvs_column:
        csv = pd.DataFrame({
            "Years": years_list,
            "Cyber Market": cyber_market_list
            }).to_csv(index = False)

        csv_btn = st.download_button(
            label ="Download as CSV",
            help = "Click here to download the data as CSV file",
            data = bytes(csv, encoding = "utf-8"),
            file_name = "cybersecurity-market-size.csv",
            mime = "text/csv",
        )
    with json_column:
        json = pd.DataFrame({
            "Years": years_list,
            "Cyber Market": cyber_market_list
            }).to_json(orient = "records")

        json_btn = st.download_button(
            label = "Download as JSON",
            help = "Click here to download the data as JSON file",
            data = bytes(json, encoding = "utf-8"),
            file_name = "cybersecurity-market-size.json",
            mime = "application/json",
        )
    with html_column:
        html = pd.DataFrame({
            "Years": years_list,
            "Cyber Market": cyber_market_list
            }).to_html(index = False)

        html_btn = st.download_button(
            label = "Download as HTML",
            help = "Click here to download the data as HTML file",
            data = bytes(html, encoding = "utf-8"),
            file_name = "cybersecurity-market-size.html",
            mime = "text/html",
        )
    return csv_btn, json_btn, html_btn

cyber_marker_view = st.selectbox(
    "Select View Type:", ["Vertical Bar Chart", "Table"]
)

if cyber_marker_view == "Vertical Bar Chart":
    st.write(create_cyber_market_barchart(cyber_market_df[0]))

    st.info("The dates with asterisk (*) are the projected dates")

    st.markdown("*Download the data:*\n\n")
    (csv_cyber_market,
    json_cyber_market,
    html_cyber_market,) = download_btns_cyber_market_data(cyber_market_list, years_list)

    st.markdown(
        '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html = True,
    )

elif cyber_marker_view == "Table":
    st.dataframe(cyber_market_df[0], height = 400, width = 1000)

    st.info("The dates with asterisk (*) are the projected dates")
    st.info("To download the data, please select the Vertical Bar Chart view type")

    st.markdown(
        '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html = True,
    )