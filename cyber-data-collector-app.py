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
import lxml

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
            "Home",
            "Cyber Statistics",
            "CVE Data",
            "About",
            "Contact",
        ],  # List of options in the menu
        icons=[
            "house",
            "bi-bar-chart-line",
            "bi-shield-exclamation",
            "info-square",
            "envelope",
        ],
        default_index = 0,  # Index of the default option ("Home" in this case)
    )

    custom_footer = """
    <footer style = "font-family: 'Segoe UI'; font-size: 14px; color: #6C757D; text-align: center; padding: 125px 0px 10px 0px;"><img src="https://cdn-icons-png.flaticon.com/512/4486/4486819.png" width="16" height="16">&nbsp;&nbsp;with ❤️ by 
    <a href = "https://github.com/martin-ruseq" target = "_blank">Marcin Rusiecki</a>"""
    st.markdown(custom_footer, unsafe_allow_html = True)

# ------------------------------------------------ START OF HOME PAGE ------------------------------------------ #
if selected_page == "Home":
    st.title("Welcome to the CyberHub :wave:")
    st.subheader("*Your cyber statistics in one place* :bar_chart:")
    
    st.markdown("""
            <style>
            #welcome-to-the-cyberhub {
                text-align: center;
                color: #0062AF;
                font-size: 50px;
                font-family: 'Segoe UI';
                }
            #your-cyber-statistics-in-one-place {
                text-align: center;
                color: #6C757D;
                font-size: 20px;
                font-family: 'Segoe UI';
                }
            </style>
            """, unsafe_allow_html = True)
    
    st.warning(
        "The app is still in development and more features will be added in the future :wrench: \n\nPlease check back later for updates :new: \n\nThank you for your patience :pray: "
    )
    def get_news():
        # RSS Feed with the latest cyber news using bs4 and requests libraries
        url = "https://feeds.feedburner.com/TheHackersNews"
        response = requests.get(url)
        rss_feed = bs4(response.content, features = "xml")
        items = rss_feed.find_all("item")
        
        # Create empty lists to store the data
        titles = []
        links = []
        descriptions = []
        dates = []
        
        # Loop through the items and extract the data
        for item in items:
            title = item.find("title").text
            link = item.find("link").text
            description = item.find("description").text
            date = item.find("pubDate").text
            enclosure = item.find("enclosure")["url"]
            titles.append(title)
            links.append(link)
            descriptions.append(description)
            dates.append(date)
            
        df = pd.DataFrame(
            {
                "title": titles,
                "link": links,
                "description": descriptions,
                "date": dates,
            }
        )    
            
        for i in range(len(df)):
            st.markdown(
                f'<h3 style = "text-align: left; color: #0062AF;">{df["title"][i]}</h3>',
                unsafe_allow_html = True,
            )
            st.markdown(
                f'<p style = "text-align: left; color: #6C757D;">{df["description"][i]}</p>',
                unsafe_allow_html = True,
            )
            
            st.markdown(
                f'<p style = "text-align: left; color: #6C757D;"><a href = "{df["link"][i]}" target = "_blank">Read more</a></p>',
                unsafe_allow_html = True,
            )
            
            st.markdown(
                f'<p style = "text-align: right; color: #6C757D;">Published: {df["date"][i][0:-5]}</p>',
                unsafe_allow_html = True,
            )

            st.markdown(
                '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
                unsafe_allow_html = True,
            )
    st.title("Latest Cyber News")
    st.markdown("""
        Source: [The Hacker News](https://thehackernews.com/)
        """)
    st.markdown(
        '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html = True,
    )
            
    get_news()
# ------------------------------------------------ END OF HOME PAGE -------------------------------------------- #


# ----------------------------------------- START OF CYBER STATISTICS PAGE ------------------------------------- #
if selected_page == "Cyber Statistics":
    exec(open("cyber-stats.py").read())
# ---------------------------------------- END OF CYBER STATISTICS PAGE ---------------------------------------- #


# ------------------------------------------- START OF CVE DATA PAGE ------------------------------------------- #
if selected_page == "CVE Data":

    def get_latest_vulns():
        url = "https://nvd.nist.gov/general/nvd-dashboard"
        response = requests.get(url)
        soup = bs4(response.content, "html.parser")
        ul = soup.find("ul", {"id": "latestVulns"})

        if ul is None:
            st.error("Could not find CVE data.")
            return []

        latest_20_vulns = []
        for li in ul.find_all("li"):
            vuln = {
                "CVE ID": li.div.find("a").text.strip(),
                "Description": li.div.find("strong").next_sibling.strip().strip(" - "),
                "Severity": li.select_one("span", {"id": "cvss*"}).text.strip()[5:],
                "Published": li.select_one('strong:contains("Published")').next_sibling.strip().split(";")[0].strip(),  # displays the text until the first semicolon (;)
                "CVE URL": "https://nvd.nist.gov" + li.div.find("a")["href"],
            }
            latest_20_vulns.append(vuln)
            latest_20_vulns_df = pd.DataFrame(latest_20_vulns).set_index("CVE ID")

        return latest_20_vulns_df

    @st.cache_data
    def colors_4_severity_scores(severity):
        if "CRITICAL" in severity:
            return "background-color: black; color: white"
        elif "HIGH" in severity:
            return "background-color: red; color: white"
        elif "MEDIUM" in severity:
            return "background-color: orange; color: black"
        elif "LOW" in severity:
            return "background-color: yellow; color: black"
        else:
            return "background-color: #AAAAAA; color: white"

    latest_20_vulns_df = get_latest_vulns()
    styled_latest_20_vulns_df = latest_20_vulns_df.style.applymap(
        colors_4_severity_scores, subset = ["Severity"]) # apply colors from function to the Severity column

    st.markdown(
        "<h1 style = 'text-align: center; color: #0062AF;'>Common Vulnerabilities and Exposures (CVE) Dashboard</h1>",
        unsafe_allow_html = True,)
    
    st.markdown(
        '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
        unsafe_allow_html = True,)

    cve_explenation = st.expander("What is a CVE?")
    cve_explenation.write(
        """
        Common Vulnerabilities and Exposures (CVE®) is a list of records — each containing an identification number,
        a description, and at least one public reference — for publicly known cybersecurity vulnerabilities. 
        CVE Entries are used in numerous cybersecurity products and services from around the world, including the
        U.S. National Vulnerability Database (NVD).""")

    cve_score_explenation = st.expander("What is a CVSS Score?")
    cve_score_explenation.write(
        """
        The Common Vulnerability Scoring System (CVSS) is a free and open industry standard for assessing the 
        severity of computer system security vulnerabilities. CVSS attempts to assign severity scores to 
        vulnerabilities,allowing responders to prioritize responses and resources according to threat. 
        Scores are calculated based on a formula that depends on several metrics that approximate ease of 
        exploit and the impact of exploit. Scores range from 0 to 10, with 10 being the most severe.
        Visit the [Vulnerability Metrics](https://nvd.nist.gov/vuln-metrics/cvss#) to learn more.""")

    st.subheader("Latest 20 Scored Vulnerabilities")
    st.markdown(
        """
        Source: [National Vulnerability Database (NVD)](https://nvd.nist.gov/)
        """)

    st.dataframe(styled_latest_20_vulns_df, height = 400, width = 1000)

    # Streamlit Tabs for CVE Data Page
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "| Top 50 CVSS by Product |",
            "| CVSS Score Distribution |",
            "| CVEs by Years / Types |",
            "| Weaknesses Types |",
            "| CAPECs: ATT&AT Patters |",
        ])

    # st. markdown is used to diplay text in markdown format, and manipulate the style.
    st.markdown(
        """<style>
                .css-b218v0 p {
                    word-break: break-word;
                    margin-bottom: 0px;
                    font-size: 14px;
                    font-size: large;
                    font-weight: 700;
                    }
                    
                .st-dq {
                    gap: 120px;
                    }
                    
                <style>""",
        unsafe_allow_html = True,)

    # ------------------------------------ START TOP 50 CVSS BY PRODUCT TAB ------------------------------------- #
    with tab1:

        def get_cvss_product_table():
            url = "https://www.cvedetails.com/top-50-product-cvssscore-distribution.php"
            response = requests.get(url)
            soup = bs4(response.content, "html.parser")
            table = soup.find("table", {"class": "grid"})

            if table:
                rows = table.find_all("tr")
                products = []
                vendors = []
                no_of_vulns = []
                average_cvss = []
                for row in rows[1:]:
                    cells = row.find_all("td")
                    if len(cells) > 1:
                        products.append(
                            cells[1].text.strip())  # strip() is used to remove starting and trailing spaces
                        vendors.append(cells[2].text.strip())
                        no_of_vulns.append(cells[3].text.strip())
                        average_cvss.append(cells[14].text.strip())

                df = pd.DataFrame(
                    {
                        "Product": products,
                        "Vendor": vendors,
                        "No. of Vulns": no_of_vulns,
                        "Average CVSS": average_cvss,
                    }
                )
                df = df.set_index("Product")

            return df

        df = get_cvss_product_table()

        tableCol, pieCol = st.columns([1, 1])  # Create two columns for table and pie chart

        with tableCol:
            st.subheader("Table of Top 50 CVSS by Product")
            st.markdown("""
                Source: [CVE Details](https://www.cvedetails.com/top-50-product-cvssscore-distribution.php)""")

            st.dataframe(df, height = 350, width = 1000)

        with pieCol:
            st.subheader("Total No. Of Vulnerabilities By Vendor")

            pieChatr = px.pie(
                df,
                values = "No. of Vulns",
                color_discrete_sequence = px.colors.cyclical.IceFire,
                hole = 0.3,
                names = df.columns[0],
                hover_data = ["Average CVSS"],
            )

            pieChatr.update_traces(
                textposition = "inside",
                textinfo = "label+percent",
                insidetextorientation = "radial",
            )

            pieChatr.update_layout(uniformtext_minsize = 12)

            st.plotly_chart(pieChatr, use_container_width = True)
    # ------------------------------------- END TOP 50 CVSS BY PRODUCT TAB -------------------------------------- #


    # ------------------------------------ START CVSS SCORE DISTRIBUTION TAB ------------------------------------ #
    with tab2:

        def get_cve_score_distrbution():
            url = "https://www.cvedetails.com/cvss-score-distribution.php"
            response = requests.get(url)
            soup = bs4(response.content, "html.parser")
            table = soup.find("table", {"class": "grid"})

            cvss_scores = []
            no_of_vulns = []
            percentage = []

            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    header = row.find("th")
                    cells = row.find_all("td")
                    if len(cells) > 1:
                        cvss_scores.append(header.text.strip())
                        no_of_vulns.append(cells[0].text.strip())
                        percentage.append(cells[1].text.strip())

                df = pd.DataFrame(
                    {
                        "CVSS Score": cvss_scores,
                        "No. of Vulns": no_of_vulns,
                        "Percentage": percentage,
                    }
                )

            return df

        @st.cache_data
        def colors_4_cvss_score(score):
            if "0-1" in score:
                return "background-color: #00C400"
            elif "1-2" in score:
                return "background-color: #00E020"
            elif "2-3" in score:
                return "background-color: #00F000"
            elif "3-4" in score:
                return "background-color: #d1ff00"
            elif "4-5" in score:
                return "background-color: #ffe000"
            elif "5-6" in score:
                return "background-color: #ffcc00"
            elif "6-7" in score:
                return "background-color: #ffbc10"
            elif "7-8" in score:
                return "background-color: #ff9c20"
            elif "8-9" in score:
                return "background-color: #ff8000"
            elif "9-10" in score:
                return "background-color: #ff0000"
            else:
                return "background-color: #EEEEEE"

        df = get_cve_score_distrbution()
        styled_df = df.style.applymap(
            colors_4_cvss_score, subset=["CVSS Score"]
            )  # apply the colors_4_cvss_score function to the CVSS Score column

        tableCol, barCol = st.columns([1, 1])

        with tableCol:
            st.subheader("Table of CVSS Score Distribution")
            st.markdown(
                """
                Source: [CVE Details](https://www.cvedetails.com/cvss-score-distribution.php)
                """
            )

            st.dataframe(
                styled_df,
                height = 350,
                width = 1000,
            )

        with barCol:
            st.subheader("Bar Chart of CVSS Score Distribution")

            barChart = px.bar(
                df.loc[1:9],  # df.loc is used to select the rows from 1 to 9 (excluding 10)
                x = "CVSS Score",
                y = "No. of Vulns",
                hover_data = ["Percentage"],
                color = "CVSS Score",  # differentiate color based on CVSS Score
                color_discrete_map = {  # map the colors to the CVSS Score
                    "0-1": "#00C400",
                    "1-2": "#00E020",
                    "2-3": "#00F000",
                    "3-4": "#d1ff00",
                    "4-5": "#ffe000",
                    "5-6": "#ffcc00",
                    "6-7": "#ffbc10",
                    "7-8": "#ff9c20",
                    "8-9": "#ff8000",
                    "9-10": "#ff0000",
                },
            )

            barChart.update_layout(uniformtext_minsize = 12)

            st.plotly_chart(barChart, use_container_width = True)
    # ------------------------------------- END CVSS SCORE DISTRIBUTION TAB ------------------------------------- #


    # --------------------------------------- START CVE TYPE / YEAR TAB ----------------------------------------- #
    with tab3:

        def get_cves_type_year():
            url = "https://www.cvedetails.com/vulnerabilities-by-types.php"
            response = requests.get(url)
            soup = bs4(response.content, "html.parser")
            table = soup.find("table", {"class": "stats"})

            years = []
            no_of_vulns = []
            dos = []
            exec_code = []
            overflow = []
            mem_corruption = []
            sqli = []
            xss = []
            dir_traversal = []
            http_resp_split = []
            bypass = []
            gain_info = []
            gain_priv = []
            csrf = []
            file_inc = []
            no_of_exploits = []

            if table:
                rows = table.find_all("tr")
                for row in rows[1:-1]:
                    header = row.find("th")
                    cells = row.find_all("td")
                    if len(cells) > 1:
                        years.append(header.text.strip())
                        no_of_vulns.append(cells[0].text.strip())
                        dos.append(cells[1].text.strip())
                        exec_code.append(cells[2].text.strip())
                        overflow.append(cells[3].text.strip())
                        mem_corruption.append(cells[4].text.strip())
                        sqli.append(cells[5].text.strip())
                        xss.append(cells[6].text.strip())
                        dir_traversal.append(cells[7].text.strip())
                        http_resp_split.append(cells[8].text.strip())
                        bypass.append(cells[9].text.strip())
                        gain_info.append(cells[10].text.strip())
                        gain_priv.append(cells[11].text.strip())
                        csrf.append(cells[12].text.strip())
                        file_inc.append(cells[13].text.strip())
                        no_of_exploits.append(cells[14].text.strip())

                df = pd.DataFrame(
                    {
                        "Year": years,
                        "No. of Vulns.": no_of_vulns,
                        "DoS": dos,
                        "Code Exe.": exec_code,
                        "Overflow": overflow,
                        "Mem. Corrupt.": mem_corruption,
                        "SQLi": sqli,
                        "XSS": xss,
                        "Dir. Traversal": dir_traversal,
                        "HTTP Resp. Split": http_resp_split,
                        "Bypass": bypass,
                        "Gain Info.": gain_info,
                        "Gain Priv.": gain_priv,
                        "CSRF": csrf,
                        "File Inc.": file_inc,
                        "No. of Exploits": no_of_exploits,
                    }
                )

                df = df.set_index("Year")

            return df

        tableCol, pieChartCol = st.columns([1, 1])

        with tableCol:
            st.subheader("CVEs by Year / Type")
            st.markdown(
                """
                Source: [CVE Details](https://www.cvedetails.com/vulnerabilities-by-types.php)
                """
            )

            df = get_cves_type_year()

            st.dataframe(df, height = 380, width = 485)

        with pieChartCol:
            st.subheader("Pie Chart of CVEs by Type")

            pieChart = px.pie(
                df,
                values=df.loc["Total"][1:14],   # uses the "Total" row and excludes the first column (which is the "No. of Vulns." column)
                                                # and the last column (which is the "No. of Exploits" column)
                names = df.columns[1:14],
                color_discrete_sequence = px.colors.cyclical.IceFire,
                hole = 0.3,
            )

            pieChart.update_traces(
                textposition = "inside",
                textinfo = "percent+label",
                insidetextorientation = "radial",
            )
            pieChart.update_layout(uniformtext_minsize = 12)

            st.plotly_chart(pieChart, use_container_width = True, width = 200)
    # ---------------------------------------- END CVE TYPE / YEAR TAB ------------------------------------------ #


    # ------------------------------------------ START CWE TAB -------------------------------------------------- #
    with tab4:

        @st.cache_data
        def get_weeknesses():
            url = "https://cwe.mitre.org/data/definitions/677.html"
            response = requests.get(url)
            soup = bs4(response.content, "html.parser")
            table = soup.find("table", {"id": "Detail"})

            cve_type = []
            cve_id = []
            cve_name = []

            if table:
                rows = table.find_all("tr")
                if rows:
                    for row in rows[1:]:
                        cells = row.find_all("td")
                        if len(cells) > 1:
                            cve_type.append(
                                cells[1].text.strip()[:4]
                            )  # only get the first 4 characters of the type (which is "Base")
                            cve_id.append(cells[2].text.strip())
                            cve_name.append(cells[3].text.strip())

                    df = pd.DataFrame({
                        "Type": cve_type,
                        "ID": cve_id,
                        "Name": cve_name
                        })

                    df = df.set_index("ID")

            return df

        common_weakness = st.expander(
            "What is *Common Weakness Enumeration (CWE&#8482;)*?", expanded=False
        )
        common_weakness.write(
            """
            **_Common Weakness Enumeration (CWE&#8482;)_** is a list or dictionary of weaknesses that are often found in software and hardware.
            The list describes the types of weaknesses that can lead to security vulnerabilities and provides guidance on how to identify,
            mitigate, and prevent them. Visit [cwe.mitre.org](https://cwe.mitre.org/about/index.html) for more information.
            """
        )

        base_type = st.expander("What is *Base* weakeness type?", expanded = False)
        base_type.write(
            """
            The **Base** is weakness that is still mostly independent of a resource or technology, but with sufficient details
            to provide specific methods for detection and prevention. Visit [cwe.mitre.org](https://cwe.mitre.org/documents/glossary/index.html#Base%20Weakness) for more information.
            """
        )

        st.subheader("Table of CWE&#8482; Types ")
        st.markdown(
            """
            Source: [cwe.mitre.org](https://cwe.mitre.org/data/definitions/677.html)
            """
        )

        df = get_weeknesses()
        st.dataframe(df, height = 350, width = 1000)
    # ------------------------------------------ END CWE TAB ---------------------------------------------------- #


    # ------------------------------------------ START CAPEC TAB ------------------------------------------------ #
    with tab5:
        def get_capecs():
            url = "https://capec.mitre.org/data/definitions/658.html"
            respones = requests.get(url)
            soup = bs4(respones.content, "html.parser")
            table = soup.find("table", {"id": "Detail"})

            capec_type = []
            capec_id = []
            capec_name = []

            if table:
                rows = table.find_all("tr")
                for row in rows[1:]:
                    cells = row.find_all("td")
                    if len(cells) > 1:
                        capec_type.append(cells[1].text.strip().split("-")[0].strip())  # displays the first part of the text (up to the dash)
                        capec_id.append(cells[2].text.strip())
                        capec_name.append(cells[3].text.strip())

                df = pd.DataFrame({
                    "Type": capec_type,
                    "ID": capec_id,
                    "Name": capec_name
                    })

                df = df.set_index("ID")

            return df

        capec_explenation = st.expander("What is a CAPEC?")
        capec_explenation.write(
            """
        The **Common Attack Pattern Enumeration and Classification (CAPEC™)** is publicly available catalog of
        common attack patterns that helps users understand how adversaries exploit weaknesses in applications
        and other cyber-enabled capabilities. CAPEC is maintained by the MITRE Corporation and sponsored by
        the Department of Homeland Security (DHS) Cybersecurity and Infrastructure Security Agency (CISA).
        Visit the [CAPEC Website](https://capec.mitre.org/about/index.html) to learn more."""
        )

        attack_patterns_types = st.expander("What are the types of attack patterns?")
        attack_patterns_types.write(
            """
            *"An attack pattern is the common approach and attributes related to the exploitation of a weakness 
            in a software, firmware, hardware, or service component"*
            
            There are three types of attack patterns:                 
                                    
            **Standard Attack Patterns** - A standard attack pattern is meant to provide sufficient details to
            understand the specific technique and how it attempts to accomplish a desired goal.
            
            **Meta Attack Patterns**- A meta attack pattern is often void of a specific technology or implementation 
            and is meant to provide an understanding of a high level approach. A meta level attack pattern is a 
            generalization of related group of standard level attack patterns.
            
            **Detailed Attack Patterns** - Detailed attack patterns are more specific than meta attack patterns and 
            standard attack patterns and often require a specific protection mechanism to mitigate actual attacks.
            A detailed level attack pattern often will leverage a number of different standard level attack patterns 
            chained together to accomplish a goal.
            """
        )

        st.subheader("CAPECs: ATT&CK Patterns")
        st.markdown(
            """
            Source: [capec.mitre.org](https://capec.mitre.org/data/definitions/658.html)
            """
        )

        df = get_capecs()
        st.dataframe(df, height = 350, width = 1000)
# ---------------------------------------------------- END OF CVE PAGE ------------------------------------------ #


# ---------------------------------------------------- START OF ABOUT PAGE ------------------------------------- #
if selected_page == "About":
    st.title("About")
    st.markdown("""
        <style>
        #about {
            text-align: center;
            color: #0062AF;
            font-size: 50px;
            font-family: 'Segoe UI';
            }
        </style> """, unsafe_allow_html=True)   
            
    
    st.write(
        "This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future."
    )
# ---------------------------------------------------- END OF ABOUT PAGE --------------------------------------- #


# ---------------------------------------------------- START OF CONTACT PAGE ----------------------------------- #
if selected_page == "Contact":
    st.title("Contact")
    st.markdown("""
        <style>
        #about {
            text-align: center;
            color: #0062AF;
            font-size: 50px;
            font-family: 'Segoe UI';
            }
        </style> """, unsafe_allow_html=True)  
    
    st.write(
        "If you have any questions or suggestions, you can contact me at [LinkedIn](https://www.linkedin.com/in/marcinrusiecki/)."
    )
# ---------------------------------------------------- END OF CONTACT PAGE ------------------------------------- #


