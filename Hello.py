import streamlit as st
import os

os.environ["KAGGLE_USERNAME"] = st.secrets["K_USER"]
os.environ["KAGGLE_KEY"] = st.secrets["K_KEY"]

import kaggle

st.set_page_config(page_title="Welcome in my streamlit app", layout="centered")
st.title("Welcome in my streamlit app")
tab1, tab2 = st.tabs(["English", "Polish"])

with tab1:
    st.header("Temperatura jezior w Polsce")
    st.markdown(
        "The purpose of this application is to check the temperature of selected bathing waters in Poland, data obtained from IMGW."
        " Currently available data are from May - September of 2023."
    )
    st.header("Bathing Water Quality for EU")
    st.markdown(
        "The purpose of this application is to check the quality of bathing water in the European Union for the years 1990 - 2022."
        "To check details of the point you can use selectbox or map."
    )

with tab2:
    st.header("Temperatura jezior w Polsce")
    st.markdown("Aplikacja służy do sprawdzenia temperatury dla wybranych kąpielisk w Polsce."
                "Dane pochodzą z serwisu IMGW. Aktualnie dostępny jest przedział Maj - Wrzesień dla roku 2023. "
                )
    st.header("Bathing Water Quality for EU (Jakość wód kąpielowych w UE)")
    st.markdown("""Aplikacja służy do sprawdzenia jakości wód kąpielowych w Unii Europejskiej dla lat 1990 - 2022.  
    Aby sprawdzić szczegóły punktu, możemy użyć mapy lub selectbox'ów.
    """)
