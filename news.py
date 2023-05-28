# Author:       Marcin Rusiecki
# Student ID:   C00263263
# Purpose:      News page of the CyberHub app. It contains the latest cyber news and it is a main page of the app.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4

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
        """, unsafe_allow_html=True)

st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

def get_news():
    # RSS Feed with the latest cyber news using bs4 and requests libraries
    url = "https://feeds.feedburner.com/TheHackersNews"
    response = requests.get(url)
    rss_feed = bs4(response.content, features="xml")
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
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<p style = "text-align: left; color: #6C757D;">{df["description"][i]}</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<p style = "text-align: left; color: #6C757D;"><a href = "{df["link"][i]}" target = "_blank">Read more</a></p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<p style = "text-align: right; color: #6C757D;">Published: {df["date"][i][0:-5]}</p>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
            unsafe_allow_html=True,
        )

st.title("Latest Cyber News")
st.markdown("""
    Source: [The Hacker News](https://thehackernews.com/)
    """)

get_news()
