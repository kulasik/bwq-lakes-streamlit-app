import pandas as pd
import streamlit as st
import kaggle
import plotly.express as px


@st.cache_data(ttl=3600, show_spinner=False)
def load_lakes() -> pd.DataFrame:
    kaggle.api.dataset_download_file(
        dataset="krzysztofkulasik/daily-temperatures-of-lakes-in-poland",
        file_name="lakes_temp.csv",
        path="../lakes_streamlit/data/"
    )
    data = pd.read_csv("../lakes_streamlit/data/lakes_temp.csv")
    data = data.replace(
        {
            "Temperatura wody[°C]": "brak danych"
        },
        0
    )
    data = data.rename(columns={"Temperatura wody[°C]": "Temperatura wody"})
    data = data.astype({
        "Data": "datetime64[ns]",
        "Nazwa stacji": "string",
        "Lokalizacja": "string",
        "Województwo": "category",
        "Temperatura wody": "float32"
    })
    data['Data'] = data['Data'].apply(lambda x: x.date())
    return data


st.title("Temperatura jezior w Polsce")

with st.container():
    df = load_lakes()

    selected_region = st.multiselect(
        label="Nazwa województwa",
        placeholder="Wybierz lub wpisz nazwę województwa",
        options=df['Województwo'].unique()
    )
    selected_lake = st.multiselect(
        label="Nazwa stacji",
        placeholder="Wybierz lub wpisz nazwę stacji",
        options=df.loc[df["Województwo"].isin(selected_region), "Nazwa stacji"].unique() if len(selected_region) > 0
        else df["Nazwa stacji"].unique()
    )

    if len(selected_lake) == 0:
        st.info("Wybierz województwo albo stację ")

    else:
        dates = df.loc[df["Nazwa stacji"].isin(selected_lake), "Data"]

        selected_date = st.date_input(
            "Podaj datę dla pomiaru temperatury",
            value=[
                dates.min(),
                dates.max()
            ],
            min_value=dates.min(),
            max_value=dates.max(),
            format="YYYY-MM-DD"
        )

        if len(selected_date) != 2:
            st.error("Podaj cały zakres dat")

        else:
            start_date, end_date = selected_date

            selected_data = df[(df['Data'] >= start_date) &
                               (df['Data'] <= end_date) &
                               (df['Nazwa stacji'].isin(selected_lake))
                               ]

            st.dataframe(
                selected_data
            )

            st.plotly_chart(
                px.line(
                    selected_data,
                    x="Data",
                    y="Temperatura wody",
                    color="Nazwa stacji",
                    markers=True
                )
            )
