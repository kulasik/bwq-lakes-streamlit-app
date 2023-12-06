import pandas as pd
import streamlit as st
import plotly.express as px
import os
import re
import tabula
from os.path import join
import kaggle


@st.cache_resource(ttl=3600, show_spinner="Pobieranie danych")
def download_dataset() -> None:
    """Download dataset from kaggle """
    kaggle.api.dataset_download_files(
        dataset="krzysztofkulasik/daily-temperatures-of-lakes-poland",
        path="../lakes_streamlit/data/lakes/pdf",
        unzip=True
    )
    return


def export_date(filename) -> str:
    """
    Exporting date from filename
    Parameters:
        filename (str) : Filename of the pdf
    Returns:
        date (str) : Date in format "RRRR-MM-DD
    """
    pattern = r'([0-9]{8})'
    matches = re.search(pattern, filename)
    if matches.group(0) is not None:
        match = matches.group(0)
        date = f'{match[:4]}-{match[4:6]}-{match[6:8]}'
        return date


@st.cache_data(ttl=3600, show_spinner="Przetwarzanie danych")
def load_lakes() -> pd.DataFrame:
    """
    Load and process dataset (rename columns, assign types to columns).

    Returns:
        data (pd.DataFrame) : DataFrame that contains concatenated files from dataset
    """

    pdf_dir = "../lakes_streamlit/data/lakes/pdf"
    pdfs = {}
    for root, _, files in os.walk(pdf_dir):
        for filename in files:
            pdfs[export_date(filename)] = join(root, filename)

    concat_pdfs = pd.DataFrame(columns=["Data", "Nazwa stacji", "Lokalizacja", "Województwo", "Temperatura wody"])

    for date, filename in pdfs.items():
        df_pdf = tabula.read_pdf(filename, lattice=True)[0]
        df_pdf.dropna(axis=1, inplace=True)
        df_pdf.drop(columns='Lp.', inplace=True)

        df_pdf.rename(columns={'Temperatura wody\robserwator\r[°C]': 'Temperatura wody'}, inplace=True)
        df_pdf['Data'] = date

        concat_pdfs = pd.concat([concat_pdfs, df_pdf], axis=0)
        concat_pdfs.drop_duplicates(subset=['Data', 'Nazwa stacji', 'Lokalizacja'], keep='first', inplace=True)

    data = concat_pdfs.replace(
        {
            "Temperatura wody": "brak danych"
        },
        0
    )
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
                               ].sort_values(by="Data")

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
