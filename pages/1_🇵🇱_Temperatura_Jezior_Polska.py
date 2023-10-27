import pandas as pd
import streamlit as st
import plotly.express as px
import kaggle


@st.cache_resource(ttl=3600, show_spinner="Pobieranie danych")
def download_dataset() -> None:
    """Download dataset from kaggle """
    kaggle.api.dataset_download_file(
        dataset="krzysztofkulasik/daily-temperatures-of-lakes-in-poland",
        file_name="lakes_temp.csv",
        path="../data/"
    )
    return


@st.cache_data(ttl=3600, show_spinner="Przetwarzanie danych")
def load_lakes() -> pd.DataFrame:
    """
    Load and process dataset (rename columns, assign types to columns).

    Returns:
        data (pd.DataFrame) : DataFrame that contains concatenated files from dataset
    """

    data = pd.read_csv("../data/lakes_temp.csv")
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


st.set_page_config(page_title="Temperatura jezior w Polsce", layout="wide", page_icon="🇵🇱")
st.title("Temperatura jezior w Polsce")

with st.container():
    download_dataset()
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
        else df["Nazwa stacji"].unique(),
        max_selections=3
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

            # To consider
            # st.subheader("Temperatura z ostatniego pomiaru:")
            # day, stat, temp = st.columns(3)
            #
            # for station in selected_lake:
            #     station_row = df.query("`Nazwa stacji` == @station")
            #     last_day = station_row["Data"].max()
            #     last_day_temp = station_row.query("Data == @last_day")['Temperatura wody'].values[0]
            #     day.metric(label="Dzień", value=str(last_day))
            #     stat.metric(label="Stacja", value=station)
            #     temp.metric(label="Temperatura", value=last_day_temp)

            st.plotly_chart(
                px.line(
                    selected_data,
                    x="Data",
                    y="Temperatura wody",
                    color="Nazwa stacji",
                    markers=True
                )
            )

            st.dataframe(
                selected_data
            )
