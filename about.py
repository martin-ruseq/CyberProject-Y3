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
        

st.write(
    "This app was created to collect cyber data from various sources and visualize it in one place. The data is collected using Python and the visualization is done using Streamlit. The app is still in development and more features will be added in the future."
)