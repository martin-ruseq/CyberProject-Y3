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

# Set the page title and icon
st.set_page_config(page_title="CyberHub App", page_icon="⛏️", 
                   layout="wide", 
                   initial_sidebar_state="expanded",
                   )

# Hide the menu and footer of Streamlit Cloud deployments
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stActionButton {visibility: hidden;}
            .viewerBadge_container__1QSob {display: none;}
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

        # START OF THE GLOBAL HACKING METHODS DATA
        st.title("Global Hacking Methods")
        st.markdown("""
            This chart/table shows the percentage of the leading global hacking methods.

            Source: [statista.com](https://www.statista.com/statistics/221390/share-of-hacking-methods-across-organizations/)
            """)
        
        # Create a dropdown menu for year selection
        data_year = st.selectbox("Select Year:", ["2019", "2018", "2017", "2016", "2015"])
        
        # Create dropdown menu for chart type
        view_type = st.selectbox("Select View Type:", ["Horizontal Bar Chart", "Table"])

        # Create a dataframe to store the data for the selected year
        chart_data = {"Methods": methods_list, "Percentage": percentage_list}
        chart_df = pd.DataFrame(chart_data)

        # Createing the horizontal bar chart using Plotly
        if data_year == "2019" and view_type == "Horizontal Bar Chart":
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
                width = 1000,
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
        unsafe_allow_html=True,)
    # END OF THE GLOBAL HACKING METHODS DATA

    # START OF THE LEGAL CASES UNDER COMPUTER MISUSE ACT 1990 (UK) DATA
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
    # END OF LEGAL CASES DATA
    
    # START OF CYBERCRIME DAMAGES DATA
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
            width=1000,
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
    # END OF CYBERCRIME DAMAGES DATA
        
    # START OF CYBERSECURITY MARKET SIZE DATA
    st.title("Cybersecurity market size worldwide 2019-2030")
    st.subheader("*(in billion U.S. dollars)*")
    st.markdown("""
        The statistic shows the size of the cybersecurity market worldwide, from 2019 to 2030 acording to the data
        from [Next Move Strategy Consulting](https://www.nextmsc.com/). The global cybersecurity market is 
        projected to reach 657.02 billion U.S. dollars by 2030.
        
        Source: [statista.com](https://www.statista.com/statistics/1256346/worldwide-cyber-security-market-revenues/) and [nextmsc.com](https://www.nextmsc.com/])
        """)
    
    url = "https://www.statista.com/statistics/1256346/worldwide-cyber-security-market-revenues/"
    cyber_market_table_str = get_data(url)
    cyber_market_table = bs4(cyber_market_table_str, 'html.parser')
    
    def make_cyber_market_df(cyber_market_table):
        cyber_market_list = []
        years_list = []
        for row in cyber_market_table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) > 1:
                cyber_market = cells[1].text.strip()
                years = cells[0].text.strip()
                cyber_market_list.append(cyber_market)
                years_list.append(years)
        cyber_market_df = pd.DataFrame({'Years': years_list, 'Cyber Market': cyber_market_list})
        
        return cyber_market_df, cyber_market_list, years_list
    
    cyber_market_df = make_cyber_market_df(cyber_market_table)
    cyber_market_list = cyber_market_df[1]
    years_list = cyber_market_df[2]
    
    @st.cache_data
    def create_cyber_market_barchart(cyber_market_df):
        barchart = px.bar(
            cyber_market_df, x="Years", 
            y="Cyber Market", orientation='v', 
            color="Cyber Market", 
            color_discrete_sequence=px.colors.cmocean.thermal_r, 
            labels={"Cyber Market": "Cyber Market (in billion U.S. dollars)"}
            )
        
        barchart.update_layout(
            showlegend=False,
            width=1000,
        )
        
        return barchart
    
    def download_btns_cyber_market_data(cyber_market_list, years_list):
        cvs_column, json_column, html_column = st.columns(3, gap = "small")
        
        with cvs_column:
            csv = pd.DataFrame({'Years': years_list, 'Cyber Market': cyber_market_list}).to_csv(index=False)
            csv_btn = st.download_button(
                label="Download as CSV",
                help="Click here to download the data as CSV file",
                data=bytes(csv, encoding='utf-8'),
                file_name="cybersecurity-market-size.csv",
                mime="text/csv"
            )
        with json_column:
            json = pd.DataFrame({'Years': years_list, 'Cyber Market': cyber_market_list}).to_json(orient='records')
            json_btn = st.download_button(
                label="Download as JSON",
                help="Click here to download the data as JSON file",
                data=bytes(json, encoding='utf-8'),
                file_name="cybersecurity-market-size.json",
                mime="application/json"
            )
        with html_column:
            html = pd.DataFrame({'Years': years_list, 'Cyber Market': cyber_market_list}).to_html(index=False)
            html_btn = st.download_button(
                label="Download as HTML",
                help="Click here to download the data as HTML file",
                data=bytes(html, encoding='utf-8'),
                file_name="cybersecurity-market-size.html",
                mime="text/html"
            )
        return csv_btn, json_btn, html_btn
        

    cyber_marker_view = st.selectbox("Select View Type:", ["Vertical Bar Chart", "Table"])
    
    if cyber_marker_view == "Vertical Bar Chart":
        st.write(create_cyber_market_barchart(cyber_market_df[0]))
        st.info("The dates with asterisk (*) are the projected dates")
        st.markdown("*Download the data:*\n\n")
        csv_cyber_market, json_cyber_market, html_cyber_market = download_btns_cyber_market_data(cyber_market_list, years_list)
        st.markdown(
            '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
            unsafe_allow_html=True,)
    elif cyber_marker_view == "Table":
        st.dataframe(cyber_market_df[0], height=400, width=1000)
        st.info("The dates with asterisk (*) are the projected dates")
        st.info("To download the data, please select the Vertical Bar Chart view type")
        st.markdown(
            '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
            unsafe_allow_html=True,)
    # END OF CYBERSECURITY MARKET SIZE
    
if selected_page == "CVE Data":
    def get_latest_vulns():
        url = "https://nvd.nist.gov/general/nvd-dashboard"
        response = requests.get(url)
        soup = bs4(response.content, 'html.parser')
        ul = soup.find('ul', {'id': 'latestVulns'})

        if ul is None:
            st.error('Could not find CVE data.')
            return []

        latest_20_vulns = []
        for li in ul.find_all('li'):
            vuln = {
                'CVE ID': li.div.find('a').text.strip(),
                'Description': li.div.find('strong').next_sibling.strip().strip(' - '),
                'Severity': li.select_one('span', {'id': 'cvss*'}).text.strip()[5:],
                'Published': li.select_one('strong:contains("Published")').next_sibling.strip().split(';')[0].strip(),
                'CVE URL': 'https://nvd.nist.gov' + li.div.find('a')['href'],
            }
            latest_20_vulns.append(vuln)
            latest_20_vulns_df = pd.DataFrame(latest_20_vulns).set_index('CVE ID')

        return latest_20_vulns_df
    
    @st.cache_data
    def colors_4_severity_scores(severity):
        if "CRITICAL" in severity:
            return 'background-color: black; color: white'
        elif "HIGH" in severity:
            return 'background-color: red; color: white'
        elif "MEDIUM" in severity:
            return 'background-color: orange; color: black'
        elif "LOW" in severity:
            return 'background-color: yellow; color: black'
        else:
            return 'background-color: #AAAAAA; color: white'
    
    latest_20_vulns_df = get_latest_vulns()
    styled_latest_20_vulns_df = latest_20_vulns_df.style.applymap(colors_4_severity_scores, subset=['Severity'])
    
    st.markdown("<h1 style='text-align: center; color: #0062AF;'>Common Vulnerabilities and Exposures (CVE) Dashboard</h1>", unsafe_allow_html=True)
    st.markdown(
        '<hr style="border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html=True,)
    
    cve_explenation = st.expander("What is a CVE?")
    cve_explenation.write("""
        Common Vulnerabilities and Exposures (CVE®) is a list of records — each containing an identification number,
        a description, and at least one public reference — for publicly known cybersecurity vulnerabilities. 
        CVE Entries are used in numerous cybersecurity products and services from around the world, including the
        U.S. National Vulnerability Database (NVD).""")
    
    cve_score_explenation = st.expander("What is a CVSS Score?")
    cve_score_explenation.write("""
        The Common Vulnerability Scoring System (CVSS) is a free and open industry standard for assessing the 
        severity of computer system security vulnerabilities. CVSS attempts to assign severity scores to 
        vulnerabilities,allowing responders to prioritize responses and resources according to threat. 
        Scores are calculated based on a formula that depends on several metrics that approximate ease of 
        exploit and the impact of exploit. Scores range from 0 to 10, with 10 being the most severe.
        Visit the [Vulnerability Metrics](https://nvd.nist.gov/vuln-metrics/cvss#) to learn more.""")
    
    st.subheader("Latest 20 Scored Vulnerabilities")
    st.markdown("""
        Source: [National Vulnerability Database (NVD)](https://nvd.nist.gov/)
        """)
    st.dataframe(styled_latest_20_vulns_df, height=400, width=1000)

    # Streamlit Tabs for CVE Data Page 
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["| Top 50 CVSS by Product |", " | CVSS Score Distribution |"," | CVEs by Type / Year |", "| CWE Types |", "| CAPECs: ATT&AT Patters |"])
    
    # st. markdown is used to diplay text in markdown format, and manipulate the style.
    st.markdown("""<style>
                .css-b218v0 p {
                    word-break: break-word;
                    margin-bottom: 0px;
                    font-size: 14px;
                    font-size: large;
                    font-weight: 700;
                }
                .st-dq{
                    gap: 120px;
                }
                <style>""", unsafe_allow_html=True)
    with tab1:
        def get_cvss_product_table():
            url = "https://www.cvedetails.com/top-50-product-cvssscore-distribution.php"
            response = requests.get(url)
            soup = bs4(response.content, 'html.parser')
            table = soup.find('table', {'class': 'grid'})
            if table:
                rows = table.find_all('tr')
                products = []
                vendors = []
                no_of_vulns = []
                average_cvss = []
                for row in rows[1:]:
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        products.append(cells[1].text.strip())  # strip() is used to remove starting and trailing spaces 
                        vendors.append(cells[2].text.strip())
                        no_of_vulns.append(cells[3].text.strip())
                        average_cvss.append(cells[14].text.strip())
                df = pd.DataFrame({'Product': products, 'Vendor': vendors, 'No. of Vulns': no_of_vulns, 'Average CVSS': average_cvss})
                df = df.set_index('Product')
                
            return df
        
        df = get_cvss_product_table()
        
        tableCol, pieCol = st.columns([1, 1])   # Create two columns for table and pie chart
        with tableCol:
            st.subheader("Table of Top 50 CVSS by Product")
            st.markdown("""
                Source: [CVE Details](https://www.cvedetails.com/top-50-product-cvssscore-distribution.php)
                """)
            st.dataframe(df, height=350, width=1000)
            
        with pieCol:
            st.subheader("Total No. Of Vulnerabilities By Vendor")
            pieChatr = px.pie(df, values='No. of Vulns', hole=.3, names=df.columns[0], hover_data=['Average CVSS'])
            pieChatr.update_traces(textposition='inside', textinfo = 'label+percent')
            pieChatr.update_layout(uniformtext_minsize=12)
            st.plotly_chart(pieChatr, use_container_width=True)
    with tab2:
        def get_cve_score_distrbution():
            url = "https://www.cvedetails.com/cvss-score-distribution.php"
            response = requests.get(url)
            soup = bs4(response.content, 'html.parser') 
            table = soup.find('table', {'class': 'grid'}) 
            cvss_scores = []
            no_of_vulns = []
            percentage = []
            if table:
                rows = table.find_all('tr')
                for row in rows[1:]:
                    header = row.find('th')
                    cells = row.find_all('td')
                    if len(cells) > 1:
                        cvss_scores.append(header.text.strip())     
                        no_of_vulns.append(cells[0].text.strip())
                        percentage.append(cells[1].text.strip())
                df = pd.DataFrame({'CVSS Score': cvss_scores, 'No. of Vulns': no_of_vulns, 'Percentage': percentage})
                  
            return df
        
        @st.cache_data
        def colors_4_cvss_score(score):
            if "0-1" in score:
                return 'background-color: #00C400'
            elif "1-2" in score:
                return 'background-color: #00E020'
            elif "2-3" in score:
                return 'background-color: #00F000'
            elif "3-4" in score:
                return 'background-color: #d1ff00'
            elif "4-5" in score:
                return 'background-color: #ffe000'
            elif "5-6" in score:
                return 'background-color: #ffcc00'
            elif "6-7" in score:
                return 'background-color: #ffbc10'
            elif "7-8" in score:
                return 'background-color: #ff9c20'
            elif "8-9" in score:
                return 'background-color: #ff8000'
            elif "9-10" in score:
                return 'background-color: #ff0000'
            else:
                return 'background-color: #EEEEEE'
            
        df = get_cve_score_distrbution()
        styled_df = df.style.applymap(colors_4_cvss_score, subset=['CVSS Score'])   # apply the colors_4_cvss_score function to the CVSS Score column
        
        tableCol, barCol = st.columns([1, 1])
        with tableCol:
            st.subheader("Table of CVSS Score Distribution")
            st.markdown("""
                Source: [CVE Details](https://www.cvedetails.com/cvss-score-distribution.php)
                """)
            st.dataframe(styled_df, height=350, width=1000)
        with barCol:
            st.subheader("Bar Chart of CVSS Score Distribution")
            barChart = px.bar(
                df.loc[1:9],    # df.loc[1:9] is used to remove the last row (Total)
                x='CVSS Score', 
                y='No. of Vulns',
                hover_data=['Percentage'],
                color='CVSS Score',     # differentiate color based on CVSS Score
                color_discrete_map={    # map the colors to the CVSS Score
                    "0-1": "#00C400",
                    "1-2": "#00E020",
                    "2-3": "#00F000",
                    "3-4": "#d1ff00",
                    "4-5": "#ffe000",
                    "5-6": "#ffcc00",
                    "6-7": "#ffbc10",
                    "7-8": "#ff9c20",
                    "8-9": "#ff8000",
                    "9-10": "#ff0000"
                })
            barChart.update_layout(uniformtext_minsize=12)
            st.plotly_chart(barChart, use_container_width=True)


    with tab3:
        st.subheader("CVEs by Type / Year")
    
    with tab4:
        def get_weeknesses():
            url = "https://cwe.mitre.org/data/definitions/677.html"
            response = requests.get(url)
            soup = bs4(response.content, 'html.parser')
            table = soup.find('table', {'id': 'Detail'})
            cve_nature = []
            cve_type = []
            cve_id = []
            cve_name = []
            print(table)
            if table:
                rows = table.find_all('tr')
                if rows:
                    for row in rows[1:]:
                        cells = row.find_all('td')
                        if len(cells) > 1:
                            cve_nature.append(cells[0].text.strip())
                            cve_type.append(cells[1].text.strip())
                            cve_id.append(cells[2].text.strip())
                            cve_name.append(cells[3].text.strip())
                    df = pd.DataFrame({'Nature': cve_nature, 'Type': cve_type, 'ID': cve_id, 'Name': cve_name})
                    df = df.set_index('ID')
            return df
                
        df = get_weeknesses()
        
        common_weakness = st.expander("What is *Common Weakness Enumeration (CWE)*?", expanded = False)
        common_weakness.write("""
            **_Common Weakness Enumeration (CWE)_** is a list of software and hardware weaknesses. It serves as a common language, a measuring stick for security tools,
            and as a baseline for weakness identification, mitigation, and prevention efforts. CWE consists of: 1) a community-developed dictionary of common
            software and hardware weaknesses; 2) a formal modeling concept that describes the relationships between weaknesses and other factors; and 3) a
            language-independent software assurance activity specification that can be used to perform software vulnerability detection, mitigation, and prevention.
            Visit [cwe.mitre.org](https://cwe.mitre.org/about/index.html) for more information.
            """)
        
        base_type = st.expander("What is *Base* weekeness type?", expanded = False)
        base_type.write("""
            Base is a weakness type that is still mostly independent of a resource or technology, but with sufficient details to provide specific methods for 
            detection and prevention. Base level weaknesses typically describe issues in terms of 2 or 3 of the following dimensions: behavior, property, technology,
            language, and resource. For example, a weakness that describes a property of a resource, such as a file permission error, is a Base weakness. Visit 
            [cwe.mitre.org](https://cwe.mitre.org/documents/glossary/index.html#Base%20Weakness) for more information.
            """)
        
        st.subheader("CWE Types")
        st.markdown("""
            Source: [cwe.mitre.org](https://cwe.mitre.org/data/definitions/677.html)
            """)
        st.dataframe(df, height=350, width=1000)
    
    with tab5:
        capec_explenation = st.expander("What is a CAPEC?")
        capec_explenation.write("""
        The Common Attack Pattern Enumeration and Classification (CAPEC™) is publicly available catalog of
        common attack patterns that helps users understand how adversaries exploit weaknesses in applications
        and other cyber-enabled capabilities. CAPEC is maintained by the MITRE Corporation and sponsored by
        the Department of Homeland Security (DHS) Cybersecurity and Infrastructure Security Agency (CISA).
        Visit the [CAPEC Website](https://capec.mitre.org/about/index.html) to learn more.""")
        
        st.subheader("CAPECs: ATT&CK Patterns")
        

if selected_page == "About":
    st.title("About")
    st.write("This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future.")

if selected_page == "Contact":
    st.title("Contact")
    st.write("If you have any questions or suggestions, you can contact me at [LinkedIn](https://www.linkedin.com/in/marcinrusiecki/).")