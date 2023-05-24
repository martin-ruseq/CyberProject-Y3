# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import streamlit as st

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
st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)

st.write("If you have any questions or suggestions, feel free to contact me via email or social media. I will try to respond as soon as possible. Thank you for your interest in my project!")

st.write("Here are my social media links and email:")
st.markdown("""
        <a href = "https://www.linkedin.com/in/marcinrusiecki/" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="40" height="40">
        </a>
        &nbsp; 
        <a href = "https://www.instagram.com/cyberuseq" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" width="40" height="40">
        &nbsp; 
        <a href = "https://www.github.com/martin-ruseq" target="_blank">
        <img src="https://cdn-icons-png.flaticon.com/512/3291/3291667.png" width="40" height="40">
        &nbsp; 
        </a>
        <a href = mailto:marcin.rusiecki@protonmail.com>
        <img src="https://cdn-icons-png.flaticon.com/512/10186/10186030.png" width="42" height="42">
        </a>
        
        """, unsafe_allow_html=True)

st.markdown(
    '<hr style = "border-top: 4px solid #FCCA3A; border-radius: 5px">',
    unsafe_allow_html=True,
)
