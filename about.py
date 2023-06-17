# Author:       Marcin Rusiecki
# Student ID:   C00263263
# Purpose:      About page of the CyberHub app. It contains information about the app and FAQ.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st

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
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.subheader("What is CyberHub?")
st.markdown("""
    CyberHub is a web application that allows you to view and analyze cyber security data.
    The data are collected from various sources and presented in a user-friendly way.
    On this website you can find useful statistics, information reated with cyber security and much more.
    """)
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.subheader("How to use CyberHub?")
st.markdown("""
    To use CyberHub, you need to select one of the options from the sidebar menu located
    on the left side of the screen. The menu contains the following options:
    * **Home** - the main page of the application where you can find the latest cyber news
    * **Cyber Statistics** - a page where you can find various statistics related to cyber security
    * **CVE & Related Data** - a page where you can find information about CVEs, CWEs and CAPECs
    * **About** - a page where you can find information about the application (you are here! :smile:) 
    * **Contact** - a page where you can find information about the author of the application
    """)
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.subheader("What data is used in CyberHub?")
st.markdown("""
    CyberHub uses data from various sources such as:
    * [statista.com](https://www.statista.com/)
    * [nvd.nist.gov](https://nvd.nist.gov/)
    * [cvedetails.com](https://www.cvedetails.com/)
    * [capec.mitre.org](https://capec.mitre.org/) and
    * [thehackernews.com](https://thehackernews.com/)
    
    to provide you with the most up-to-date information.""")
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.subheader("Can I download the data used in CyberHub?")
st.markdown("""
    Yes, some of the data used in CyberHub can be downloaded. Under the graphs you can find a buttons 
    that allows you to download the data in CSV, JSON or HTML format.""")
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.subheader("I can't see the data, what should I do?")
st.markdown("""
    If you can't see the data, it is probably because the application is still loading the data.
    If you see the loading icon like this one:
    """)
st.image("resources/data_loading.png", width=160)
st.markdown("""
    in the top right corner of the screen, it means that the application is still loading the data.
    Please wait a few seconds and the data should appear.""")

st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.subheader("Who is the author of CyberHub?")
st.markdown("""
    CyberHub was created by Marcin Rusiecki, a Cybersecurity student of the South East Technological University in Ireland.
    """)
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)
