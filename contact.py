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

st.write(
    "If you have any questions or suggestions, you can contact me at [LinkedIn](https://www.linkedin.com/in/marcinrusiecki/)."
)
